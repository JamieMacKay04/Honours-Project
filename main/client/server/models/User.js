const mongoose = require('mongoose');
const { v4: uuidv4 } = require('uuid'); // Import UUID generator

const UserSchema = new mongoose.Schema({
    userId: { type: String, default: uuidv4, unique: true }, // Custom ID for FK usage
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true }
}, { timestamps: true });

module.exports = mongoose.model('User', UserSchema);
