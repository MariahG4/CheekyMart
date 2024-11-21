'use strict';

const bakeryButton = document.querySelector('.bakery-btn');
bakeryButton.addEventListener('click', () => {
    fetchData('static/json/bakery.json');
});

const dairyButton = document.querySelector('.dairy-btn');
dairyButton.addEventListener('click', () => {
    fetchData('static/json/dairy.json');
});

const drinksButton = document.querySelector('.drinks-btn');
drinksButton.addEventListener('click', () => {
    fetchData('static/json/coffeetea.json');
});

const fruitsButton = document.querySelector('.fruits-btn');
fruitsButton.addEventListener('click', () => {
    fetchData('static/json/fruits.json');
});

const meatButton = document.querySelector('.meat-btn');
meatButton.addEventListener('click', () => {
    fetchData('static/json/meat.json');
});

const nonButton = document.querySelector('.non-btn');
nonButton.addEventListener('click', () => {
    fetchData('static/json/nondairy_meatalt.json');
});

const vegetablesButton = document.querySelector('.vegetables-btn');
vegetablesButton.addEventListener('click', () => {
    fetchData('static/json/vegetables.json');
});
/*
const searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', () => {
    fetchData2('static/json/Products.json');
});
*/

async function fetchData(fileName) {
    try {
        const response = await fetch(fileName);
        if(!response.ok) {
            throw Error(`Error: ${response.url} ${response.statusText}`)
        }
        const data = await response.json();
        addProducts(data);
    } catch (error) {
        console.log(error.message);
    }
}
/*
async function fetchData2(fileName) {
    try {
        const response = await fetch(fileName);
        if(!response.ok) {
            throw Error(`Error: ${response.url} ${response.statusText}`)
        }
        const data = await response.json();
        searchProduct(data);
    } catch (error) {
        console.log(error.message);
    }
}
*/
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');

    if (category) {
        loadProductsByCategory(category); // Automatically load products for the selected category
    }
});

// Function to load products based on category
function loadProductsByCategory(category) {
    const categoryToFileMap = {
        'Bakery': 'static/json/bakery.json',
        'Dairy': 'static/json/dairy.json',
        'Fruits': 'static/json/fruits.json',
        'Vegetables': 'static/json/vegetables.json',
        'Drinks': 'static/json/coffeetea.json',
        'Meat': 'static/json/meat.json',
        'Non-Dairy': 'static/json/nondairy_meatalt.json',
    };

    const fileName = categoryToFileMap[category];
    if (fileName) {
        fetchData(fileName);
    } else {
        console.error('Invalid category:', category);
    }
}

function addProducts(products) {
    const container = document.querySelector('.products-container');
    container.innerHTML = '';

    products.forEach((product) => {
        const article = document.createElement('article');
        article.classList.add('card');

        const img = document.createElement('img');
        img.src = product.image; // image source
        img.alt = product.name; // if image doesn't show up
        article.appendChild(img);

        const productContent = document.createElement('div');
        productContent.classList.add('content');

        const title = document.createElement('h3');
        title.textContent = product.name;

        const price = document.createElement('p');
        price.textContent = "$" + product.price.toFixed(2);
        price.style.textAlign = "center";

        const category = document.createElement('p');
        category.textContent = product.category;
        category.style.textAlign = "center";

        const button = document.createElement('button');
        button.textContent = "Add to cart";
        button.style.backgroundColor = "green";
        button.style.color = "white";
        button.style.borderRadius = "10px 10px 10px 10px";
        


        article.appendChild(productContent);
        productContent.appendChild(title);
        productContent.appendChild(price);
        productContent.appendChild(category);
        productContent.appendChild(button);
        container.appendChild(article);
        button.onclick = () => addToCart(product.name, product.price);
    });
}

function addToCart(name, price) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const product = cart.find(product => product.name === name);
    if (product) {
        product.quantity++;
    } else {
        cart.push({name, price, quantity: 1});
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${name} added to your cart!`);
}


document.getElementById('payment-form').onsubmit = function(event) {
    //no default
    event.preventDefault();

    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    console.log('Cart data before submission:', cart);


    if (cart.length === 0) {
        alert('Your cart is empty.');
        return false;
    }


    document.getElementById('cart-data').value = JSON.stringify(cart);
    console.log('Hidden input set with cart data:', document.getElementById('cart-data').value);


    this.submit();
};

function displayProducts(filteredProducts) {
    const productList = document.getElementById('product-list');
    productList.innerHTML = ''; // Clear current list
    
    // If no products match, show a message
    if (filteredProducts.length === 0) {
        productList.innerHTML = '<p>No products found.</p>';
        return;
    }
    
    // Create a product element for each item in the filtered list
    filteredProducts.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.textContent = product.name + " $" + product.price + " ";
        const button = document.createElement('button');
        button.textContent = "Add to cart";
        button.style.backgroundColor = "green";
        button.style.color = "white";
        button.style.borderRadius = "10px 10px 10px 10px";
        button.style.padding = "3px 3px 3px 3px"
        productDiv.appendChild(button);
        productList.appendChild(productDiv);
        button.onclick = () => addToCart(product.name, product.price);
    });
}

// Function to search for a product (triggered by button click)
function searchProduct(products) {
    const query = document.getElementById('search-bar').value.toLowerCase();
    
    // Filter products based on the search query
    const filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(query)
    );
    
    // Display the filtered products
    displayProducts(filteredProducts);
}

// Initial display of all products
displayProducts(products);

