# 统一异常处理 FAQ

## Q: 全局异常处理器和 Controller 级异常处理怎么共存？

A: Controller 级 `@ExceptionHandler` 优先级高于全局处理器。可以在 Controller 中处理特定异常覆盖全局行为。

```java
@RestController
@RequestMapping("/api/v1/special")
public class SpecialController {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(ResourceNotFoundException ex) {
        // 覆盖全局处理，返回自定义格式
        return ResponseEntity.status(404)
                .body(ApiResponse.error(404, "Custom: " + ex.getMessage()));
    }
}
```

## Q: @ControllerAdvice 和 @RestControllerAdvice 的区别？

A: `@RestControllerAdvice = @ControllerAdvice + @ResponseBody`。如果使用 `@RestController`，必须使用 `@RestControllerAdvice`，否则错误响应不会被序列化为 JSON。

## Q: 如何记录请求追踪 ID 到错误日志？

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ApiResponse<Void>> handleUnexpected(Exception ex, WebRequest request) {
    String requestId = request.getHeader("X-Request-Id");
    log.error("Unexpected error [requestId={}]", requestId, ex);
    return ResponseEntity.status(500)
            .body(ApiResponse.error(500, "服务器内部错误，请联系管理员。RequestId: " + requestId));
}
```

## Q: 如何处理异步方法中的异常？

```java
@Async
public CompletableFuture<UserResponse> findByIdAsync(Long id) {
    // 异步方法中的异常会被包装在 CompletableFuture 中
    // 调用方通过 exceptionally 或 handle 处理
}
```

## Q: 如何处理 Feign 调用异常？

```java
// 在 Feign 配置中处理
@Bean
public ErrorDecoder errorDecoder() {
    return (methodKey, response) -> {
        if (response.status() == 404) {
            return new ResourceNotFoundException("Remote resource not found");
        }
        return new ServiceException("Remote service error");
    };
}
```

## Q: @Validated 分组校验怎么和异常处理配合？

```java
// 不同分组触发不同校验规则
@PostMapping("/create")
public ResponseEntity<?> create(@Validated(CreateGroup.class) @RequestBody UserCreateRequest req) { }

@PutMapping("/update")
public ResponseEntity<?> update(@Validated(UpdateGroup.class) @RequestBody UserUpdateRequest req) { }

// 全局异常处理器对 MethodArgumentNotValidException 统一处理，所有分组校验错误都走到同一个 handler
```
