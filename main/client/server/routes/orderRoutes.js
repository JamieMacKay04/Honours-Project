const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem');

// Add new stock item or update existing one
router.post('/add-stock', async (req, res) => {
    try {
        const { name, category, unit, quantity } = req.body;

        // Find if the item already exists in stock
        let stockItem = await StockItem.findOne({ name, category, unit });

        if (stockItem) {
            // Update existing stock
            stockItem.quantity += parseInt(quantity);
            await stockItem.save();
        } else {
            // Add new item
            stockItem = new StockItem({ name, category, unit, quantity });
            await stockItem.save();
        }

        res.status(200).json({ message: 'Stock updated successfully', stockItem });
    } catch (error) {
        res.status(500).json({ message: 'Error updating stock', error });
    }
});

module.exports = router;
