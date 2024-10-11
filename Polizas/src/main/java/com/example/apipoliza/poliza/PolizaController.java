package com.example.apipoliza.poliza;

import com.example.apipoliza.seguro.Seguro;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/polizas")
@Validated
public class PolizaController {

    @Autowired
    private PolizaService polizaService;

    // Obtener todas las pólizas
    @GetMapping
    public List<Poliza> getAllPolizas() {
        return polizaService.getAllPolizas();
    }

    // Obtener una póliza por ID
    @GetMapping("/{id}")
    public ResponseEntity<Poliza> getPolizaById(@PathVariable Long id) {
        Optional<Poliza> poliza = polizaService.getPolizaById(id);
        if (poliza.isPresent()) {
            return new ResponseEntity<>(poliza.get(), HttpStatus.OK);
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    // Crear una nueva póliza
    @PostMapping
    public ResponseEntity<String> createPoliza(@Valid @RequestBody Poliza poliza) {
        List<Poliza> existingPolizaList = polizaService.getPolizasByCliente(poliza.getIdCliente());
        if (!existingPolizaList.isEmpty()) {
            return new ResponseEntity<>("El cliente ya tiene una póliza existente. No se puede crear otra.", HttpStatus.BAD_REQUEST);
        }

        Poliza newPoliza = polizaService.savePoliza(poliza);
        return new ResponseEntity<>("Poliza creada correctamente.", HttpStatus.CREATED);
    }

    // Actualizar una póliza existente
    @PutMapping("/{id}")
    public ResponseEntity<Poliza> updatePoliza(@PathVariable Long id, @Valid @RequestBody Poliza polizaDetails) {
        Optional<Poliza> poliza = polizaService.getPolizaById(id);
        if (poliza.isPresent()) {
            Poliza existingPoliza = poliza.get();
            existingPoliza.setIdCliente(polizaDetails.getIdCliente());
            existingPoliza.setIdAgente(polizaDetails.getIdAgente());
            existingPoliza.setFechaInicio(polizaDetails.getFechaInicio());
            existingPoliza.setFechaFin(polizaDetails.getFechaFin());
            existingPoliza.setPrima(polizaDetails.getPrima());

            if (polizaDetails.getSeguros() != null) {
                for (Seguro seguro : polizaDetails.getSeguros()) {
                    seguro.setPoliza(existingPoliza); // Vincula cada seguro a la póliza actualizada
                }
                existingPoliza.setSeguros(polizaDetails.getSeguros());
            }

            Poliza updatedPoliza = polizaService.savePoliza(existingPoliza);
            return new ResponseEntity<>(updatedPoliza, HttpStatus.OK);
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    // Eliminar una póliza
    @DeleteMapping("/{id}")
    public ResponseEntity<HttpStatus> deletePoliza(@PathVariable Long id) {
        polizaService.deletePoliza(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    // Obtener pólizas por ID de cliente
    @GetMapping("/cliente/{idCliente}")
    public List<Poliza> getPolizasByCliente(@PathVariable Long idCliente) {
        return polizaService.getPolizasByCliente(idCliente);
    }
}
