document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/softdrinks')
        .then(response => response.json())
        .then(softDrinks => {
            const list = document.getElementById('softList');
            list.innerHTML = '';
            softDrinks.forEach(drink => {
                const li = document.createElement('li');
                li.textContent = `${drink['Item Name']} - Quantity: ${drink.quantity}`;
                list.appendChild(li);
            });
        })
        .catch(error => console.error('Error loading soft drinks:', error));
});
