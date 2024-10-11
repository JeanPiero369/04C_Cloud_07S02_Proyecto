const mongoose = require('mongoose');

// Esquema para manejar un contador de secuencias de IDs
const CounterSchema = new mongoose.Schema({
  _id: { type: String, required: true },
  seq: { type: Number, default: 0 }
});

module.exports = mongoose.model('Counter', CounterSchema);
