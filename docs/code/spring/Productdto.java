package com.alive.product.dto;

import lombok.Data;

@Data
public class ProductRequest {
    
    private String name;
    
    private BigDecimal price;
    
    private String description;
    
    private String status;
    
}

@Data
public class ProductResponse {
    
    private Long id;
    
    private String name;
    
    private BigDecimal price;
    
    private String description;
    
    private String status;
    
}