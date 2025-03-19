const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem');

router.get('/', async (req, res) => {
    try {
        const wines = await StockItem.find({ Category: 'wine' }); // Ensure 'wine' matches MongoDB data exactly
        res.json(wines);
    } catch (error) {
        console.error('Error fetching wines:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
