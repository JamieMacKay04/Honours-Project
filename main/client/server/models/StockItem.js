const mongoose = require('mongoose');

const StockItemSchema = new mongoose.Schema({
    name: { type: String, required: true },
    category: { type: String, enum: ['beer', 'wine', 'spirits', 'soft drinks'], required: true },
    unit: { type: String, enum: ['bottle', 'mL', 'keg'], required: true }, 
    quantity: { type: Number, required: true, min: 0 }
}, { timestamps: false });  // ✅ Prevents 'createdAt' & 'updatedAt'

StockItemSchema.set("versionKey", false);  // ✅ Prevents '__v'

module.exports = mongoose.model('StockItem', StockItemSchema, "stockitems");  // ✅ Ensure "stockitems" is specified
