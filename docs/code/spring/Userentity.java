package com.alive.user;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "t_user")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;
    
    
    @Column(name = "username", nullable = false)
    private String username;
    
    
    @Column(name = "email", nullable = false)
    private String email;
    
    
    @Column(name = "status")
    private String status;
    
    
    @Column(name = "createdAt")
    private LocalDateTime createdAt;
    
}