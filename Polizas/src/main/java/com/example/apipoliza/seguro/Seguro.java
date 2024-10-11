package com.example.apipoliza.seguro;

import com.example.apipoliza.poliza.Poliza;
import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.math.BigDecimal;

@Entity
@Data
public class Seguro {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long idSeguro;

    @NotNull
    private String nombreSeguro;

    private String descripcion;

    @Enumerated(EnumType.STRING)
    private TipoSeguros tipoSeguro;

    @ManyToOne
    @JoinColumn(name = "poliza_id", nullable = true)
    @JsonBackReference
    private Poliza poliza;

    @NotNull
    private BigDecimal monto;
}
