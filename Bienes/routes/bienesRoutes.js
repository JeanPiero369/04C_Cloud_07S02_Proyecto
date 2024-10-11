const express = require('express');
const router = express.Router();
const {
  createGood,
  getGood,
  updateGood,
  deleteGood,
  checkAPI,
  getAutos,    // Obtener todos los Autos
  getCasas,    // Obtener todas las Casas
  getLaptops,   // Obtener todas las Laptops
  getAllBienes  // Obtener todos los bienes
} = require('../controllers/bienesController');

// Rutas para manejar bienes

// Rutas para obtener bienes por tipo (GET) - DEFINIR ESTAS PRIMERO
router.get('/bienes/autos', getAutos);      // Ruta para obtener autos
router.get('/bienes/casas', getCasas);      // Ruta para obtener casas
router.get('/bienes/laptops', getLaptops);  // Ruta para obtener laptops
router.get('/bienes/all', getAllBienes);  // Ruta para obtener todos los bienes

// Crear un bien (POST)
router.post('/bienes', createGood);

// Obtener un bien por ID (GET) - DEFINIR ESTO DESPUÉS
router.get('/bienes/:id', getGood);

// Actualizar un bien por ID (PUT)
router.put('/bienes/:id', updateGood);

// Eliminar un bien por ID (DELETE)
router.delete('/bienes/:id', deleteGood);

// Ruta para verificar si la API está funcionando (GET)
router.get('/check_api', checkAPI);

module.exports = router;
