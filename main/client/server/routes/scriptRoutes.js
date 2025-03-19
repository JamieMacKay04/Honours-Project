const express = require('express');
const router = express.Router();  //  This line is missing!
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const filePath = path.join(__dirname, '../ml/newOrder.csv');
console.log(`Looking for newOrder.csv at: ${filePath}`); // Debugging Step


// Route to run Python scripts and send the CSV file as a download
router.post('/run-scripts', (req, res) => {
    exec('python ../ml/trainmodel.py && python ../ml/updateDatabase.py', (error, stdout, stderr) => {
        if (error) {
            console.error(` Error: ${error.message}`);
            return res.status(500).send('Error running Python scripts');
        }

        if (stderr) {
            console.error(` stderr: ${stderr}`);
        }

        console.log(`✅ Python Script Output:\n${stdout}`);

        const filePath = path.join(__dirname, '../../ml/newOrder.csv');

        // Add delay to ensure Python finishes writing the file
        setTimeout(() => {
            if (fs.existsSync(filePath)) {
                console.log('newOrder.csv found - Sending file for download.');
                res.download(filePath, 'newOrder.csv', (err) => {
                    if (err) {
                        console.error(` Error sending file: ${err}`);
                        res.status(500).send('Failed to send file');
                    }
                });
            } else {
                console.error(' Error: newOrder.csv not found');
                res.status(404).send('newOrder.csv not found');
            }
        }, 3000); // Delay to allow Python to finish writing the file
    });
});

module.exports = router;
