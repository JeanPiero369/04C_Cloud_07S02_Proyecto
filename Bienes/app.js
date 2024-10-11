const express = require('express');
const dotenv = require('dotenv');
const connectDB = require('./config/db');  // Conexión a la base de datos
const bienesRoutes = require('./routes/bienesRoutes');  // Importar las rutas de bienes

// Cargar variables de entorno
dotenv.config();

// Conectar a la base de datos
connectDB();

const app = express();
app.use(express.json());  // Middleware para manejar JSON

// Conectar las rutas
app.use('/api', bienesRoutes);  // Conectar las rutas de bienes

// Configurar el puerto desde las variables de entorno o usar el puerto 3000 por defecto
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
