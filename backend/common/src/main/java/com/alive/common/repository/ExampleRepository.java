package com.alive.{module}.repository;

import com.alive.{module}.entity.ExampleEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.UUID;

/**
 * JPA Repository
 * 自动生成于 2026-06-28 17:24
 */
@Repository
public interface ExampleRepository extends JpaRepository<ExampleEntity, UUID> {

    }