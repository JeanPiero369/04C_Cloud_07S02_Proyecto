const mongoose = require('mongoose');
const Bienes = require('./bienes');

// Discriminador para Casas
const CasaSchema = new mongoose.Schema({
  fechaCompra: { type: Date, required: true },
  cochera: { type: Boolean, required: true },
  valor: { type: Number, required: true },
});

module.exports = Bienes.discriminator('Casa', CasaSchema);
