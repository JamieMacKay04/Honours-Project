document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/spirits')
    .then(response => response.json())
    .then(spirits => {
        const list = document.getElementById('spiritsList');
        list.innerHTML = '';
        spirits.forEach(spirit => {
            const li = document.createElement('li');
            li.textContent = `${spirit['Item Name']} - Quantity: ${spirit.quantity}`;
            list.appendChild(li);
        });
    })
    .catch(error => console.error('Error loading the spirits:', error));
});
