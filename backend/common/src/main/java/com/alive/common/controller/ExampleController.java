package com.alive.{module}.controller;

import com.alive.{module}.entity.ExampleEntity;
import com.alive.{module}.service.ExampleService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.UUID;

/**
 * REST 控制器
 * 自动生成于 2026-06-28 17:24
 */
@RestController
@RequestMapping("/api/v1/examples")
@RequiredArgsConstructor
public class ExampleController {

    private final ExampleService exampleService;

    @GetMapping
    public Page<ExampleEntity> list(Pageable pageable) {
        // TODO: implement paginated list
        return Page.empty();
    }

    @GetMapping("/{id}")
    public ExampleEntity get(@PathVariable UUID id) {
        return exampleService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ExampleEntity create(@Valid @RequestBody ExampleEntity entity) {
        return exampleService.create(entity);
    }

    @PutMapping("/{id}")
    public ExampleEntity update(@PathVariable UUID id, @Valid @RequestBody ExampleEntity entity) {
        return exampleService.update(id, entity);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable UUID id) {
        exampleService.delete(id);
    }
}