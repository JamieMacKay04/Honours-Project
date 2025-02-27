document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".order-form");
    
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent page reload

        const name = form.querySelector("input[placeholder='Name']").value;
        const category = form.querySelector("input[name='category']:checked")?.value;
        const unit = form.querySelector("input[name='unit']:checked")?.value;
        const quantity = form.querySelector("input[placeholder='Quantity']").value;

        if (!name || !category || !unit || !quantity) {
            alert("Please fill out all fields!");
            return;
        }

        // Send data to server
        const response = await fetch("/api/add-stock", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, category, unit, quantity }),
        });

        const data = await response.json();
        if (response.ok) {
            form.reset();
            location.reload(); // ✅ Refresh the page after submission
        
        
        } else {
            alert(`Error: ${data.message}`);
        }
    });
});
