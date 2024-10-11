package com.example.apipoliza.seguro;

import com.example.apipoliza.poliza.Poliza;
import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.math.BigDecimal;

@Entity
@Data
@Table(name="seguros")
public class Seguro {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @NotNull
    @Column(name = "nombreseguro")
    private String nombreSeguro;

    @Column(name = "descripcion")
    private String descripcion;

    @Enumerated(EnumType.STRING)
    @Column(name = "tiposeguro")
    private TipoSeguros tipoSeguro;

    @ManyToOne
    @JoinColumn(name = "idpoliza", nullable = true)
    @JsonBackReference
    private Poliza poliza;

    @NotNull
    @Column(name = "monto")
    private BigDecimal monto;
}
