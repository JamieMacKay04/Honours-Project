require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const path = require('path');
const { exec } = require('child_process'); 
const fs = require('fs');
const multer = require('multer');

const authRoutes = require('./routes/authRoutes');


const app = express();
app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, '../public')));
app.use(express.static(path.join(__dirname, '../client/public')));

// 🔥 Connect to MongoDB
mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/mydatabase', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => console.log('🔥 MongoDB Connected!'))
.catch(err => console.error('❌ MongoDB Connection Error:', err));

// ✅ Serve `signup.html`
app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/signup.html')); // ✅ Correct path
});


// ✅ Serve `login.html`
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/public/login.html'));
});

const orderRoutes = require('./routes/orderRoutes');  // Existing Route
app.use('/api/order', orderRoutes);

const scriptRoutes = require('./routes/scriptRoutes');
app.use('/api/script', scriptRoutes);

const latestWeekRoute = require('./routes/latest-week');
app.use('/api/script', latestWeekRoute); // Available at /api/latest-week

// Route to fetch all stock items
app.get('/api/stockitems', async (req, res) => {
    try {
        const stockItems = await StockItem.find();
        res.json(stockItems);
    } catch (err) {
        console.error(err);
        res.status(500).send('Error fetching stock items');
    }
});

// Route to update a stock item's quantity
app.post('/api/stockitems/update', async (req, res) => {
    const { itemId, quantity } = req.body;

    try {
        const updatedItem = await StockItem.findByIdAndUpdate(itemId, { quantity }, { new: true });
        if (!updatedItem) {
            return res.status(404).send('Item not found');
        }
        res.json(updatedItem);
    } catch (err) {
        console.error(err);
        res.status(500).send('Error updating stock item');
    }
});



// Import Routes
const addStockRoute = require("./routes/addStock");  // Correct import
app.use("/api", addStockRoute);                      // Correct usage

// ✅ Use authentication routes
app.use('/api/auth', authRoutes);

const beerRoutes = require('./routes/beerRoutes');
const wineRoutes = require('./routes/wineRoutes');
const spiritsRoutes = require('./routes/spiritsRoutes');
const softDrinksRoutes = require('./routes/softDrinksRoutes');

app.use('/api/wines', wineRoutes);
app.use('/api/spirits', spiritsRoutes);
app.use('/api/softdrinks', softDrinksRoutes);
app.use('/api', beerRoutes);

const getStockRoutes = require("./routes/getStock"); // Import the route
app.use("/api", getStockRoutes); // Use it under `/api`

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));

const analyticsRoutes = require('./routes/latest-week');
app.use('/', analyticsRoutes);

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, '../ml'); // make sure this folder exists
    },
    filename: (req, file, cb) => {
        cb(null, 'stockOrder.csv');
    }
});

const upload = multer({ storage: storage });

app.post('/upload-endpoint', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded');
    }

    console.log('File uploaded:', req.file.filename);
    res.status(200).json({ message: 'File uploaded successfully', fileName: req.file.filename });
});

// ✅ Route to trigger Python scripts and send the CSV file
app.post('/run-scripts', (req, res) => {
    // Correct the path to the Python scripts
    exec('python ../ml/trainmodel.py && python ../ml/updateDatabase.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send('Error running Python scripts');
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Error running Python scripts');
        }

        // Correct file path for newOrder.csv
        const filePath = path.join(__dirname, 'client/ml/newOrder.csv');

        // Check if the newOrder.csv file exists
        if (fs.existsSync(filePath)) {
            // Send the file as a download response
            res.setHeader('Content-Type', 'text/csv');
            res.setHeader('Content-Disposition', 'attachment; filename=newOrder.csv');
            fs.createReadStream(filePath).pipe(res);  // Stream the CSV file
        } else {
            res.status(404).send('newOrder.csv not found');
        }
    });
});



