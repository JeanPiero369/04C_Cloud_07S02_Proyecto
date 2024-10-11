package com.example.apipoliza.poliza;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PolizaService {

    @Autowired
    private PolizaRepository polizaRepository;

    // Obtener todas las pólizas
    public List<Poliza> getAllPolizas() {
        return polizaRepository.findAll();
    }

    // Obtener una póliza por su ID
    public Optional<Poliza> getPolizaById(Long id) {
        return polizaRepository.findById(id);
    }

    // Guardar o actualizar una póliza
    public Poliza savePoliza(Poliza poliza) {
        return polizaRepository.save(poliza);
    }

    // Eliminar una póliza por su ID
    public void deletePoliza(Long id) {
        polizaRepository.deleteById(id);
    }

    // Obtener pólizas por id_cliente (consulta personalizada)
    public List<Poliza> getPolizasByCliente(Long idCliente) {
        return polizaRepository.findByIdCliente(idCliente);
    }
}