from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    return render_template('homepage.html')

# Login/Signup Page
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == "POST":
        # Process login form data
#        pass
#    else:
#       return render_template('login.html')

# Products Page
@app.route('/search')
def search():
    return render_template('search.html')
    
@app.route('/account')
def profile():
    return render_template('account.html')

# Shopping Cart Page
@app.route('/cart')
def shopping_cart():
    return render_template('cart.html')

# Products Page
@app.route('/products')
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)