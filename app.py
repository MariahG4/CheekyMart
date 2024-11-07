from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Home Page
@app.route('/home')
def index():
    return render_template('homepage.html')

# Login/Signup Page
@app.route('/')#methods=['GET', 'POST'])
def login():
    #if request.method == "POST":
        # Process login from data
    #    pass
    #else:
       return render_template('login.html')

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