package com.alive.{module}.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * JPA 实体
 * 自动生成于 2026-06-28 17:24 | 版本：1.0
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "t_example")
public class ExampleEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

        @Column(name = "name", nullable = false)
        private String name;
        @Column(name = "description", nullable = true)
        private String description;
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}