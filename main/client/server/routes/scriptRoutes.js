const express = require('express');
const router = express.Router(); 
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const filePath = path.join(__dirname, '../ml/newOrder.csv');
console.log(`Looking for newOrder.csv at: ${filePath}`); 


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

router.post('/run-update', (req, res) => {
    const scriptPath = path.join(__dirname, '../../ml/updateDatabase.py');
    exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
      if (error) {
        console.error('Update script error:', error.message);
        return res.status(500).send('Failed to update database');
      }
      if (stderr) {
        console.error('Update stderr:', stderr);
      }
      console.log('Update stdout:', stdout);
      res.status(200).send('Database update completed.');
    });
  });
  

module.exports = router;
