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

let cart = [];

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
        price.textContent = "$" + product.price;
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

        /*
        $(button).on('click', function() {
            const productID = $(this).closest(productContent).data(title);
            $ajax({
                url: '/add_to_cart',
                type: 'POST',
                data: {
                    product_id = productID
                },
                success: function(response) {
                    updateCart(response.cart);
                },
                error: function() {
                    alert('Error adding product to cart');
                }
            }
            )
        })
        */
    });
}
