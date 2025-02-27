require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const path = require('path');

const authRoutes = require('./routes/authRoutes');

const app = express();
app.use(cors());
app.use(express.json());

// ✅ Serve Static Files from `client/public/`
app.use(express.static(path.join(__dirname, '../public')));

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

const orderRoutes = require('./routes/orderRoutes');
app.use('/api/order', orderRoutes);

// Import Routes
const addStockRoute = require("./routes/addStock");
app.use("/api", addStockRoute);

// ✅ Use authentication routes
app.use('/api/auth', authRoutes);

const getStockRoutes = require("./routes/getStock"); // Import the route
app.use("/api", getStockRoutes); // Use it under `/api`

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));



