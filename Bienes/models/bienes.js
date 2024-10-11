const mongoose = require('mongoose');

// Esquema base para Bienes
const BienesSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },  // Definir el ID como número y asegurarlo único
  ID_cliente: { type: Number, required: true },
  ID_seguro: { type: Number, required: true }
}, {
  discriminatorKey: 'tipoBien',  // Discriminador para identificar el tipo de bien
  versionKey: false,  // Deshabilitar el campo __v
  toJSON: {
    virtuals: true,
    transform: function (doc, ret) {
      delete ret._id;  // Ocultar el campo _id en las respuestas JSON
      delete ret.__v;  // Ocultar el campo __v en las respuestas JSON
    }
  }
});

// Exportar el modelo base Bienes
module.exports = mongoose.model('Bienes', BienesSchema);
