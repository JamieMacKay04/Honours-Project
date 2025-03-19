const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem'); // Assuming you have a Mongoose model for StockItems

router.get('/beers', async (req, res) => {
    try {
        const beers = await StockItem.find({ Category: 'beer' });
        res.json(beers);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;
