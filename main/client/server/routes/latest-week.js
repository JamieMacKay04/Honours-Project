const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

router.get('/latest-week', (req, res) => {
  const results = [];
  const csvPath = path.join(__dirname, '../../client/ml/stockOrders.csv');

  fs.createReadStream(csvPath)
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      const weekNumbers = results.map(row => parseInt(row['Week']));
      const latestWeek = Math.max(...weekNumbers);
      res.json({ week: latestWeek });
    })
    .on('error', (err) => {
      console.error('CSV read error:', err);
      res.status(500).json({ error: 'Failed to read CSV' });
    });
});

module.exports = router;
