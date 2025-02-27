const express = require("express");
const router = express.Router();
const Stock = require("../models/Stock"); // MongoDB Model

router.post("/add-stock", async (req, res) => {
    try {
        const { name, category, unit, quantity } = req.body;
        if (!name || !category || !unit || !quantity) {
            return res.status(400).json({ message: "All fields are required." });
        }

        const newStock = new Stock({ name, category, unit, quantity });
        await newStock.save();
        res.status(201).json({ message: "Stock added successfully!" });
    } catch (error) {
        console.error("Error adding stock:", error);
        res.status(500).json({ message: "Server Error" });
    }

    
});



module.exports = router;
