package com.alive.{module}.service;

import com.alive.{module}.entity.ExampleEntity;
import com.alive.{module}.repository.ExampleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

/**
 * 业务服务
 * 自动生成于 2026-06-28 17:24
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ExampleService {

    private final ExampleRepository exampleRepository;

    public List<ExampleEntity> findAll() {
        return exampleRepository.findAll();
    }

    public ExampleEntity findById(UUID id) {
        return exampleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("ExampleEntity not found: " + id));
    }

    @Transactional
    public ExampleEntity create(ExampleEntity entity) {
        log.info("Creating ExampleEntity: {}", entity);
        return exampleRepository.save(entity);
    }

    @Transactional
    public ExampleEntity update(UUID id, ExampleEntity updates) {
        var entity = findById(id);
        // TODO: apply updates
        log.info("Updating ExampleEntity: {}", id);
        return exampleRepository.save(entity);
    }

    @Transactional
    public void delete(UUID id) {
        log.info("Deleting ExampleEntity: {}", id);
        exampleRepository.deleteById(id);
    }
}