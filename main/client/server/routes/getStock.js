const express = require("express");
const router = express.Router();
const Stock = require("../models/Stock"); // Import the Stock model

// GET all stock items (group by name & sum quantity)
router.get("/get-stock", async (req, res) => {
    try {
        const stockItems = await Stock.aggregate([
            {
                $group: {
                    _id: { name: "$name", category: "$category", unit: "$unit" }, // Group by name, category, and unit
                    totalQuantity: { $sum: "$quantity" } // Sum the quantity
                }
            },
            { $sort: { "_id.name": 1 } } // Sort alphabetically by name
        ]);

        res.status(200).json(stockItems);
    } catch (error) {
        console.error("Error fetching stock:", error);
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
