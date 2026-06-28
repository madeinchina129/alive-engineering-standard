package com.alive.product;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "t_product")
public class Product {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;
    
    
    @Column(name = "name", nullable = false)
    private String name;
    
    
    @Column(name = "price", nullable = false)
    private BigDecimal price;
    
    
    @Column(name = "description")
    private String description;
    
    
    @Column(name = "status")
    private String status;
    
}