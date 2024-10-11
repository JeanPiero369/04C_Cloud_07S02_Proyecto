package com.example.apipoliza.poliza;

import com.example.apipoliza.seguro.Seguro;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Entity
@Data
@Table(name="polizas")
public class Poliza {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @NotNull
    @Column(name = "idcliente")
    private Long idCliente; // Asegúrate de que solo es un identificador y no una relación a otra entidad

    @NotNull
    @Column(name = "idagente")
    private Long idAgente;

    @OneToMany(mappedBy = "poliza", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Seguro> seguros;

    @NotNull
    @Column(name = "fechainicio")
    private LocalDate fechaInicio;

    @NotNull
    @Column(name = "fechafin")
    private LocalDate fechaFin;

    @NotNull
    @Positive
    @Column(name = "prima")
    private BigDecimal prima;
}
