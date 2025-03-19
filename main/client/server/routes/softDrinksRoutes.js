const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem');

router.get('/', async (req, res) => {
    try {
        const softDrinks = await StockItem.find({ Category: 'soft drinks' }); // Corrected to 'Soft drinks'
        res.json(softDrinks);
    } catch (error) {
        console.error('Error fetching soft drinks:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;