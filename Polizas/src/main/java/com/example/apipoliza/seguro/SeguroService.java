package com.example.apipoliza.seguro;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SeguroService {

    @Autowired
    private SeguroRepository seguroRepository;

    // Obtener todos los seguros
    public List<Seguro> getAllSeguros() {
        return seguroRepository.findAll();
    }

    // Obtener un seguro por su ID
    public Optional<Seguro> getSeguroById(Long id) {
        return seguroRepository.findById(id);
    }

    // Guardar o actualizar un seguro
    public Seguro saveSeguro(Seguro seguro) {
        return seguroRepository.save(seguro);
    }

    // Eliminar un seguro por su ID
    public void deleteSeguro(Long id) {
        seguroRepository.deleteById(id);
    }
}
