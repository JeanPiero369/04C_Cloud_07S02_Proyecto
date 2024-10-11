const Auto = require('../models/auto');
const Casa = require('../models/casa');
const Laptop = require('../models/laptop');
const Bienes = require('../models/bienes');
const Counter = require('../models/counter');  // Si usas un contador para IDs

// Función para verificar si la API está funcionando
const checkAPI = (req, res) => {
  res.status(200).json({ message: "La API está funcionando correctamente" });
};

// Crear un bien (Casa, Auto, Laptop, etc.) con IDs numéricos
const createGood = async (req, res) => {
  const { tipoBien, ...bienData } = req.body;

  try {
    // Obtener el siguiente número de secuencia para el ID
    const counter = await Counter.findByIdAndUpdate(
      { _id: 'bienes' },   // Nombre del contador
      { $inc: { seq: 1 } }, // Incrementar el valor de la secuencia en 1
      { new: true, upsert: true }  // Si no existe, crear el contador
    );

    let bien;
    const newId = counter.seq;  // Usar el nuevo valor del contador como _id

    // Crear el bien basado en el tipo de bien y asignarle el nuevo _id numérico
    switch (tipoBien) {
      case 'Auto':
        bien = new Auto({ id: newId, ...bienData });
        break;
      case 'Casa':
        bien = new Casa({ id: newId, ...bienData });
        break;
      case 'Laptop':
        bien = new Laptop({ id: newId, ...bienData });
        break;
      default:
        return res.status(400).json({ message: 'Tipo de bien no válido' });
    }

    // Guardar el bien en la base de datos
    await bien.save();
    res.status(201).json(bien);

  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// Obtener un bien por ID numérico
const getGood = async (req, res) => {
    try {
      // Buscar el bien por el campo 'id' (numérico)
      const bien = await Bienes.findOne({ id: req.params.id }).populate('ID_cliente ID_seguro');
      if (!bien) {
        return res.status(404).json({ message: 'Bien no encontrado' });
      }
  
      res.status(200).json(bien);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  };
  

// Actualizar un bien por ID numérico
const updateGood = async (req, res) => {
    const { tipoBien, ...bienData } = req.body;
  
    try {
      let bien;
      // Actualizar según el tipo de bien usando 'id' numérico
      switch (tipoBien) {
        case 'Auto':
          bien = await Auto.findOneAndUpdate({ id: req.params.id }, bienData, { new: true });
          break;
        case 'Casa':
          bien = await Casa.findOneAndUpdate({ id: req.params.id }, bienData, { new: true });
          break;
        case 'Laptop':
          bien = await Laptop.findOneAndUpdate({ id: req.params.id }, bienData, { new: true });
          break;
        default:
          return res.status(400).json({ message: 'Tipo de bien no válido' });
      }
  
      if (!bien) {
        return res.status(404).json({ message: 'Bien no encontrado' });
      }
  
      res.status(200).json(bien);
    } catch (error) {
      res.status(400).json({ message: error.message });
    }
  };
  

// Eliminar un bien por ID numérico
const deleteGood = async (req, res) => {
    try {
      const bien = await Bienes.findOneAndDelete({ id: req.params.id });  // Buscar por 'id' numérico
      if (!bien) {
        return res.status(404).json({ message: 'Bien no encontrado' });
      }
      res.status(204).json({ message: 'Bien eliminado con éxito' });
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  };

// Obtener todos los bienes de tipo Auto
const getAutos = async (req, res) => {
    try {
      const autos = await Auto.find({});
      if (autos.length === 0) {
        return res.status(404).json({ message: 'No se encontraron autos' });
      }
      res.status(200).json(autos);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  };
  
  // Obtener todos los bienes de tipo Casa
const getCasas = async (req, res) => {
    try {
      // Consulta a MongoDB para obtener solo los bienes de tipo Casa
      const casas = await Casa.find({});
      
      if (casas.length === 0) {
        return res.status(404).json({ message: 'No se encontraron casas' });
      }
      
      res.status(200).json(casas);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  };
  
// Obtener todos los bienes de tipo Laptop
const getLaptops = async (req, res) => {
    try {
      const laptops = await Laptop.find({});
      if (laptops.length === 0) {
        return res.status(404).json({ message: 'No se encontraron laptops' });
      }
      res.status(200).json(laptops);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
};

// Obtener todos los bienes (Auto, Casa, Laptop)
const getAllBienes = async (req, res) => {
    try {
      // Obtener todos los bienes (sin discriminar por tipo)
      const bienes = await Bienes.find({});
      
      if (bienes.length === 0) {
        return res.status(404).json({ message: 'No se encontraron bienes' });
      }
      
      res.status(200).json(bienes);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
};

module.exports = {
  checkAPI,
  createGood,
  getGood,
  updateGood,
  deleteGood,
  getAutos,
  getCasas,
  getLaptops,
  getAllBienes
};
