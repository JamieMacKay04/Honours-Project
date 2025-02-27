document.addEventListener("DOMContentLoaded", async () => {
    const itemList = document.getElementById("item-list"); // The list container

    async function fetchStockItems() {
        try {
            const response = await fetch("/api/get-stock"); // Fetch from backend
            const stockItems = await response.json(); // Convert response to JSON

            itemList.innerHTML = ""; // Clear existing list

            if (stockItems.length === 0) {
                itemList.innerHTML = "<li>No items available</li>";
                return;
            }

            // Loop through merged stock items
            stockItems.forEach(item => {
                const listItem = document.createElement("li");
                listItem.textContent = `${item._id.name} (${item._id.category}) - ${item.totalQuantity} ${item._id.unit}`;
                itemList.appendChild(listItem);
            });

        } catch (error) {
            console.error("Error fetching stock items:", error);
            itemList.innerHTML = "<li>Error loading items</li>";
        }
    }

    await fetchStockItems(); // Call the function when the page loads
});
