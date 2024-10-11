const mongoose = require('mongoose');
const Bienes = require('./bienes');

// Discriminador para Laptops
const LaptopSchema = new mongoose.Schema({
  fechaCompra: { type: Date, required: true },
  marca: { type: String, required: true },
  modelo: { type: String, required: true },
  valor: { type: Number, required: true }
});

module.exports = Bienes.discriminator('Laptop', LaptopSchema);
