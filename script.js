'use strict';
const bakeryButton = document.querySelector('.bakery-btn');
bakeryButton.addEventListener('click', () => {
    fetchData('json/bakery.json');
});

const dairyButton = document.querySelector('.dairy-btn');
dairyButton.addEventListener('click', () => {
    fetchData('json/dairy.json');
});

const drinksButton = document.querySelector('.drinks-btn');
drinksButton.addEventListener('click', () => {
    fetchData('json/coffeetea.json');
});

const fruitsButton = document.querySelector('.fruits-btn');
fruitsButton.addEventListener('click', () => {
    fetchData('json/fruits.json');
});

const meatButton = document.querySelector('.meat-btn');
icedButton.addEventListener('click', () => {
    fetchData('json/meat.json');
});

const nonButton = document.querySelector('.non-btn');
nonButton.addEventListener('click', () => {
    fetchData('json/nondairy_meatalt.json');
});

const vegetablesButton = document.querySelector('.vegetables-btn');
vegetablesButton.addEventListener('click', () => {
    fetchData('json/vegetables.json');
});

async function fetchData (fileName) {
    try {
        const response = await fetch(fileName);
        if(!response.ok) {
            throw Error(`Error: ${response.url} ${response.statusText}`)
        }
        const data = await response.json();
        addDrinks(data);
    } catch (error) {
        console.log(error.message);
    }
}