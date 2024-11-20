from flask import Flask, render_template, url_for, request, session, request, jsonify, redirect, flash
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
mongo_uri = os.getenv('MONGO_URI')

# Initialize flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    try:
        # Convert user_id to ObjectId before querying the database
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(str(user_data['_id']))  # Ensure `id` is a string
    except Exception as e:
        print(f"Error loading user: {e}")
    return None


# Initialize OAuth and configure app
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'email profile',
    },
)


# MongoDB setup
try:
    client = MongoClient(mongo_uri)
    db = client.get_database('CheekyMart')
    print("Connected to MongoDB! Collections:", db.list_collection_names())
except Exception as e:
    print("Error connecting to MongoDB:", e)


# Home Page
@app.route('/home')
def index():
    return render_template('homepage.html')


# Login/Signup Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from database
        user_data = db.users.find_one({'email': email})
        if user_data and check_password_hash(user_data['password'], password):
            # Log the user in
            login_user(User(str(user_data['_id'])))
            return redirect(url_for('account'))

        return "Invalid email or password", 401

    # If GET request, render the login page
    return render_template('login.html')


# Register User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Reference the users collection in the correct database
        users_collection = db['users']

        # Check if the email already exists
        if users_collection.find_one({'email': email}):
            return "Email already registered. Please log in.", 400

        # Insert the new user
        users_collection.insert_one({
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': hashed_password
        })

        return redirect(url_for('login'))  # Redirect to login page after successful registration

    # If GET request, render the register.html page
    return render_template('register.html')


# Google login
@app.route('/google-login')
def google_login():
    redirect_uri = url_for('google_auth', _external=True)  # Redirect URI after successful login
    print(f"Redirect URI: {redirect_uri}")
    return google.authorize_redirect(redirect_uri)


# Google Authentication
@app.route('/google/auth')
def google_auth():
    try:
        # Get user information from Google
        token = google.authorize_access_token()
        user_info = google.get('userinfo').json()

        # Check if the user exists in the database
        user = db.users.find_one({'email': user_info['email']})

        if user:
            # If user exists, log them in
            login_user(User(str(user['_id'])))
        else:
            # If user does not exist, register them
            new_user = {
                'username': user_info.get('name', '').replace(' ', '_').lower(),
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'email': user_info['email'],
                'google_id': user_info['id'],  # Save the Google ID
                'password': None,  # No password for Google-authenticated users
            }
            result = db.users.insert_one(new_user)
            login_user(User(str(result.inserted_id)))

        # Redirect to the account page
        return redirect(url_for('account'))

    except Exception as e:
        print(f"Error during Google login: {e}")
        flash('An error occurred during Google login. Please try again.', 'danger')
        return redirect(url_for('login'))


# Products Page
@app.route('/search')
def search():
    return render_template('search.html')

orders_collection = db['Orders']

# Account Page
@app.route('/account')
@login_required
def account():
    # Fetch the current user's ID
    user_id = current_user.id

    # finding order data based off user id
    orderData = orders_collection.find({"user_id": ObjectId(user_id)})
    orders = list(orderData)

    # Query the database for user details
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return "User not found", 404

    # Pass user information to the template
    return render_template('account.html', user=user_data, orders=orders)


# Shopping Cart Page
@app.route('/cart')
@login_required
def view_cart():
    user_id = current_user.id
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return "User not found", 404
    return render_template('cart.html', user=user_data)


# Products Page
@app.route('/products')
def products():
    return render_template('products.html')

# Account update
@app.route('/update', methods=['POST'])
@login_required
def update_account():
    user_id = current_user.id

    updated_data = {
        'username': request.form.get('username'),
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone')
    }

    if updated_data['phone']:
        updated_data['phone'] = ''.join(filter(str.isdigit, updated_data['phone']))

    updated_data = {k: v for k, v in updated_data.items() if v}

    result = db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_data})
    
    return redirect(url_for('account'))

def logged_in():
    return session.get('user') is not None

orderID = 0

#place order
@app.route('/place-order', methods=['POST'])
@login_required
def place_order():
    user_id = current_user.id
    cart = request.form.get('cart')

    # Debugging: Check if form data is received
    print("Received form data:")
    print("Card Number:", request.form.get('card-number'))
    print("Security Code:", request.form.get('security-code'))
    print("Expiration Date:", request.form.get('expiration-date'))
    print("Cart:", cart)

    if not (request.form.get('card-number') and request.form.get('security-code') and request.form.get('expiration-date')):
        flash('Please fill in all payment fields.', 'warning')
        return redirect(url_for('view_cart'))

    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('view_cart'))

    try:
        cart_data = json.loads(cart)
        print("Parsed cart data:", cart_data)
    except (TypeError, ValueError) as e:
        flash('Invalid cart data.', 'danger')
        return redirect(url_for('view_cart'))

    # check to make sure the amount in cart isnt greater than amount in stock 
    insufficient_stock_items = []
    for item in cart_data:
        product = db.Products.find_one({'name': item['name']})
        if product:
            if product['quantity'] < item['quantity']:
                insufficient_stock_items.append(item['name'])
    # if the user has items in the cart that would put the stock, alert them and say what is the issue and please remove it 
    if insufficient_stock_items:
        alert_message = f"The following items are out of stock or have insufficient stock: {', '.join(insufficient_stock_items)}. Please remove them from your cart to continue."
        print("Insufficient stock for items:", insufficient_stock_items)
        return f"<script>alert('{alert_message}'); window.location.href = '{url_for('view_cart')}';</script>"

    order = {
        'user_id': ObjectId(user_id),
        'items': cart_data,
        'status': 'Pending'
    }

    try:
        db.Orders.insert_one(order)
        flash('Order placed successfully!', 'success')
        print("Order inserted successfully:", order)

        # update stock
        for item in cart_data:
            db.Products.update_one(
                {'name': item['name']},
                {'$inc': {'quantity': -item['quantity']}}
            )
            print(f"Updated {item['name']} stock.")

    except Exception as e:
        flash('Error placing order. Please try again.', 'danger')
        print(f"Error inserting order or updating stock in MongoDB: {e}")

    return redirect(url_for('view_cart'))


# User logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logs the user out
    return redirect(url_for('login'))  # Redirect to the login page


if __name__ == '__main__':
    app.run(debug=True)