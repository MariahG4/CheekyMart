from flask import Flask, render_template, url_for, request, session, request, jsonify, redirect
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash
import os

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
    user_data = db.users.find_one({'_id': user_id})
    if user_data:
        return User(user_id)
    return None


# Initialize OAUth and configure app
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
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
    db = client.get_database()

    # Test connection
    print("Connected to MongoDB! Databases:", client.list_database_names())
except Exception as e:
    print("Error connecting to MongoDB:", e)


# Home Page
@app.route('/home')
def index():
    return render_template('homepage.html')


# Login/Signup Page
@app.route('/') #methods=['GET', 'POST'])
def login():
    #if request.method == "POST":
        # Process login from data
    #    pass
    #else:
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
            'password': hashed_password
        })

        return redirect(url_for('login'))  # Redirect to login page after successful registration

    # If GET request, render the register.html page
    return render_template('register.html')


# Google login
@app.route('/google-login')
def google_login():
    # Logic for Google login
    return "Google Login Page"


# Products Page
@app.route('/search')
def search():
    return render_template('search.html')

    
# Account Page
@app.route('/account')
def profile():
    return render_template('account.html')


# Shopping Cart Page
@app.route('/cart')
def view_cart():
    return render_template('cart.html')


# Products Page
@app.route('/products')
def products():
    return render_template('products.html')

# Functions
#@app.route('/cart/add', methods=['POST'])
#def add_to_cart():
    #cart = ShoppingCart.add(product=request.form['product'], quantity=int(request.form['quantity']))
    #return jsonify(cart)

if __name__ == '__main__':
    app.run(debug=True)