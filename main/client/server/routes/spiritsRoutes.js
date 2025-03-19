const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem');

router.get('/', async (req, res) => {
    const spirits = await StockItem.find({ Category: 'spirits' });
    res.json(spirits);
});

module.exports = router;