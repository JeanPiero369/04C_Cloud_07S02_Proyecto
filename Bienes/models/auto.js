const mongoose = require('mongoose');
const Bienes = require('./bienes');

// Discriminador para Autos con ID numérico
const AutoSchema = new mongoose.Schema({
  placa: { type: String, required: true },
  marca: { type: String, required: true },
  fechaCompra: { type: Date, required: true },
  valor: { type: Number, required: true },
});

module.exports = Bienes.discriminator('Auto', AutoSchema);
