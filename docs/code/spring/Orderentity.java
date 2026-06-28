package com.alive.order;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "t_order")
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;
    
    
    @Column(name = "userId", nullable = false)
    private Long userId;
    
    
    @Column(name = "totalAmount", nullable = false)
    private BigDecimal totalAmount;
    
    
    @Column(name = "status")
    private String status;
    
}