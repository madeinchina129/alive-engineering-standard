package com.alive.user.dto;

import lombok.Data;

@Data
public class UserRequest {
    
    private String username;
    
    private String email;
    
    private String status;
    
    private LocalDateTime createdAt;
    
}

@Data
public class UserResponse {
    
    private Long id;
    
    private String username;
    
    private String email;
    
    private String status;
    
    private LocalDateTime createdAt;
    
}