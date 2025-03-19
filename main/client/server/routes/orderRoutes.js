const express = require('express');
const router = express.Router();
const StockItem = require('../models/StockItem');
const { exec } = require('child_process');


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

// Route to run the Python script for generating orders
router.post('/run-scripts', (req, res) => {
    exec('python3 ./client/ml/trainmodel.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(`Failed to run scripts: ${error.message}`);
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        console.log(`stdout: ${stdout}`);
        res.download('/path/to/your/newOrder.csv', 'newOrder.csv', (err) => {
            if (err) {
                console.error(`File send error: ${err}`);
                return res.status(500).send('Failed to send file');
            }
        });
    });
});

module.exports = router;
