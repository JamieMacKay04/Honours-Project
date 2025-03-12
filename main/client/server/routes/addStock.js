const express = require("express");
const router = express.Router();
const Stock = require("../models/Stock");

// POST route for adding stock
router.post("/add-stock", async (req, res) => {
    try {
        let { name, category, unit, quantity } = req.body;

        // Input validation
        if (!name || !category || !unit || !quantity) {
            return res.status(400).json({ message: "All fields are required." });
        }

        // ✅ Clean up data (remove spaces, normalize casing)
        name = name.trim();
        category = category.trim().toLowerCase();
        unit = unit;
        const numericQuantity = parseInt(quantity);

        if (isNaN(numericQuantity) || numericQuantity <= 0) {
            return res.status(400).json({ message: "Quantity must be a valid number." });
        }

        // ✅ Improved Matching Logic — Matches 'name', 'category', and 'unit'
        const result = await Stock.updateOne(
            { 
                name: name, 
                category: category, 
                unit: unit
            },
            { 
                $inc: { quantity: numericQuantity }  // ✅ Increment existing quantity
            },
            { upsert: true }  // ✅ Create a new entry if no match found
        );

        // Confirmation message for better debugging
        if (result.matchedCount > 0) {
            res.status(200).json({ message: `✅ Quantity updated for "${name}"` });
        } else {
            res.status(201).json({ message: `✅ New stock added: "${name}"` });
        }

    } catch (error) {
        console.error("❌ Error adding stock:", error);
        res.status(500).json({ message: "Server Error" });
    }
});

module.exports = router;
