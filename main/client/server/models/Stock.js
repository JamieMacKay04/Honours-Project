const mongoose = require("mongoose");

const StockSchema = new mongoose.Schema({
    name: { type: String, required: true },
    category: { type: String, required: true },
    unit: { type: String, required: true },
    quantity: { type: Number, required: true },
}, { timestamps: true });

module.exports = mongoose.model("Stock", StockSchema);
