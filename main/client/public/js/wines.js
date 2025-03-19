document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/wines')
        .then(response => response.json())
        .then(wines => {
            const list = document.getElementById('wineList');
            list.innerHTML = ''; // Clear any previous data
            wines.forEach(wine => {
                const li = document.createElement('li');
                li.textContent = `${wine['Item Name']} - Quantity: ${wine.quantity}`;
                list.appendChild(li);
            });
        })
        .catch(error => console.error('Error loading wines:', error));
});
