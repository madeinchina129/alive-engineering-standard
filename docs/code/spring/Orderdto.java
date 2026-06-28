package com.alive.order.dto;

import lombok.Data;

@Data
public class OrderRequest {
    
    private Long userId;
    
    private BigDecimal totalAmount;
    
    private String status;
    
}

@Data
public class OrderResponse {
    
    private Long id;
    
    private Long userId;
    
    private BigDecimal totalAmount;
    
    private String status;
    
}