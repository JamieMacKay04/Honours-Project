document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/beers')
    .then(response => response.json())
    .then(beers => {
        const list = document.getElementById('beerList');
        beers.forEach(beer => {
            const li = document.createElement('li');
            li.textContent = `${beer['Item Name']} - Quantity: ${beer.quantity}`;
            list.appendChild(li);
        });
    })
    .catch(error => console.error('Error loading the beers:', error));
});
