---
id: springboot.exception_handling
priority: P1
owner: Java Team
version: 1.0
generated: 2026-06-28
---

# 统一异常处理规范

> **领域**: Spring Boot 开发规范 | **优先级**: P1 | **版本**: 1.0
> 
> 全局异常处理标准，@ControllerAdvice 使用，错误响应格式

> **关联规范**: [Layered Architecture 分层规范](../20_SpringBoot/2001_LayeredArchitecture.md)
[REST API 设计规范](../20_SpringBoot/2002_RestApi.md)


---

---

# 统一异常处理方案

## 为什么需要统一异常处理

### 集中管理错误逻辑

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(404, ex.getMessage()));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleValidation(MethodArgumentNotValidException ex) {
        List<FieldError> errors = ex.getBindingResult().getFieldErrors().stream()
                .map(e -> new FieldError(e.getField(), e.getDefaultMessage()))
                .toList();
        return ResponseEntity.badRequest()
                .body(ApiResponse.error(400, "Validation failed", errors));
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleGeneral(Exception ex) {
        log.error("Unexpected error", ex);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ApiResponse.error(500, "服务器内部错误"));
    }
}
```

### 业务异常 vs 系统异常

| 异常类型 | 示例 | HTTP 状态码 | 错误消息 |
|---------|------|-------------|---------|
| 业务异常 | 用户不存在 | 404 | 用户友好 |
| 参数异常 | 邮箱格式错误 | 400 | 具体错误 |
| 权限异常 | 无权限访问 | 403 | 通用 |
| 系统异常 | 数据库连接失败 | 500 | 不暴露 |

---

## 对比其他方案

| 维度 | @ControllerAdvice | ExceptionHandler 在 Controller | 手动 try-catch |
|------|-------------------|-------------------------------|----------------|
| 代码重复 | 无 | 每个 Controller 重复 | 最多 |
| 一致性 | ✅ 自动统一 | ❌ 容易遗漏 | ❌ 最差 |
| 粒度控制 | 全局 + 覆盖 | Controller 级 | 方法级 |
| 维护成本 | 低 | 中 | 高 |

---

## 适用范围

- **强制使用**：所有 Spring Boot 项目
- **全局异常处理**：统一拦截和格式化错误响应
- **业务异常**：继承自定义 RuntimeException


---

# 统一异常处理规范

## 异常类定义

### 自定义业务异常

```java
public abstract class BusinessException extends RuntimeException {
    private final int code;
    
    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }
    
    public int getCode() { return code; }
}

// 常见业务异常
public class ResourceNotFoundException extends BusinessException {
    public ResourceNotFoundException(String message) {
        super(404, message);
    }
}

public class DuplicateResourceException extends BusinessException {
    public DuplicateResourceException(String message) {
        super(409, message);
    }
}

public class UnauthorizedException extends BusinessException {
    public UnauthorizedException(String message) {
        super(401, message);
    }
}

public class ForbiddenException extends BusinessException {
    public ForbiddenException(String message) {
        super(403, message);
    }
}
```

## 强制规则 (MUST)

### 1. 全局异常处理器单一职责

```java
// ✅ 正确：一个全局 @ControllerAdvice 处理所有异常
@RestControllerAdvice
public class GlobalExceptionHandler {
    // 所有异常处理方法集中在此
}

// ❌ 错误：多个 @ControllerAdvice 分散处理
```

### 2. 业务异常在 Service 层抛出

```java
@Service
public class UserService {
    public UserResponse findById(Long id) {
        return userRepository.findById(id)
                .map(UserResponse::from)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + id));
        // ✅ 异常在 Service 层使用 Optional.orElseThrow 抛出
    }
}
```

### 3. Controller 层不 catch 业务异常

```java
// ✅ 正确：Controller 不 try-catch
@GetMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> findById(@PathVariable Long id) {
    return ResponseEntity.ok(ApiResponse.ok(userService.findById(id)));
}

// ❌ 错误：Controller 捕获异常
@GetMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> findById(@PathVariable Long id) {
    try {
        return ResponseEntity.ok(ApiResponse.ok(userService.findById(id)));
    } catch (ResourceNotFoundException e) {
        return ResponseEntity.status(404).body(ApiResponse.error(404, e.getMessage()));
    }
}
```

### 4. 区分业务异常和系统异常

```java
@ExceptionHandler(BusinessException.class)
public ResponseEntity<ApiResponse<Void>> handleBusiness(BusinessException ex) {
    log.warn("Business exception: code={}, message={}", ex.getCode(), ex.getMessage());
    return ResponseEntity.status(ex.getCode())
            .body(ApiResponse.error(ex.getCode(), ex.getMessage()));
}

@ExceptionHandler(Exception.class)
public ResponseEntity<ApiResponse<Void>> handleUnexpected(Exception ex) {
    log.error("Unexpected error", ex);  // 系统异常完整打印堆栈
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(ApiResponse.error(500, "服务器内部错误，请稍后重试"));
    // 不向客户端暴露堆栈信息
}
```

### 5. 参数校验异常返回字段级错误

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ApiResponse<Void>> handleValidation(MethodArgumentNotValidException ex) {
    List<FieldError> errors = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> new FieldError(e.getField(), e.getDefaultMessage()))
            .toList();
    return ResponseEntity.badRequest()
            .body(ApiResponse.error(400, "参数校验失败", errors));
}
```

## 推荐实践 (SHOULD)

### 1. 使用错误码枚举

```java
@Getter
public enum ErrorCode {
    RESOURCE_NOT_FOUND(404001, "资源不存在"),
    DUPLICATE_RESOURCE(409001, "资源已存在"),
    INVALID_PARAMETER(400001, "参数校验失败"),
    UNAUTHORIZED(401001, "未认证"),
    FORBIDDEN(403001, "无权限"),
    INTERNAL_ERROR(500001, "服务器内部错误");
    
    private final int code;
    private final String message;
}
```

### 2. 404 vs 空列表

```java
// GET /api/v1/users/{id}
// 用户不存在 → 404 ResourceNotFoundException

// GET /api/v1/users?status=inactive
// 没有非活跃用户 → 200 空列表
```

## 禁止行为 (MUST NOT)

- ❌ 在 Controller 中 try-catch 业务异常
- ❌ 向客户端暴露堆栈信息
- ❌ 空的 catch 块
- ❌ 使用 Exception 作为业务异常基类
- ❌ 在全局处理器中遗忘 `@ExceptionHandler` 的异常类型


---

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


---

# 统一异常处理 Code Review Checklist

## 异常类定义
- [ ] 是否有自定义业务异常基类？（BusinessException）
- [ ] 业务异常是否继承 BusinessException？
- [ ] 异常是否包含错误码？
- [ ] 是否定义了完善的 ErrorCode 枚举？

## 全局处理器
- [ ] 是否使用 @RestControllerAdvice？
- [ ] 是否覆盖了常见异常类型？（NotFound/Validation/Auth/Permission/General）
- [ ] 是否区分了业务异常和系统异常的日志级别？（warn vs error）
- [ ] 系统异常是否不暴露堆栈信息？
- [ ] 参数校验异常是否返回字段级错误详情？

## Service 层
- [ ] 业务异常是否在 Service 层抛出？
- [ ] 是否使用 Optional.orElseThrow 而非 if-null-check？
- [ ] 是否避免在 Service 层 catch 后吞掉异常？

## Controller 层
- [ ] Controller 是否没有 try-catch 业务异常？
- [ ] Controller 是否没有手动构建错误响应？
- [ ] 是否使用了 @Valid/@Validated 进行参数校验？

## 安全
- [ ] 500 错误是否不暴露内部细节？
- [ ] 错误日志是否包含请求追踪 ID？
- [ ] 是否记录完整堆栈用于排错？
- [ ] 敏感业务是否有审计日志？

## 边界情况
- [ ] Feign/RestTemplate 调用异常是否处理？
- [ ] 异步方法异常是否处理？
- [ ] 文件上传异常是否处理？
- [ ] 类型转换异常是否处理？


---

你是一个 Spring Boot 异常处理专家。请根据以下规范回答问题。

## 核心规范

### 异常层次
```
RuntimeException
  └── BusinessException (abstract)
       ├── ResourceNotFoundException (404)
       ├── DuplicateResourceException (409)
       ├── UnauthorizedException (401)
       └── ForbiddenException (403)
```

### 全局异常处理
- 使用 @RestControllerAdvice 集中处理所有异常
- 业务异常 → log.warn, 用户友好消息
- 系统异常 → log.error, 不暴露堆栈
- 参数校验异常 → 字段级错误详情

### 强制规则
1. 业务异常在 Service 抛出（Optional.orElseThrow）
2. Controller 不 try-catch 业务异常
3. 区分日志级别：业务异常 warn，系统异常 error
4. 不向客户端暴露堆栈信息
5. 空 catch 块禁止
6. 使用错误码枚举 ErrorCode

### 数据流
Controller (无 try-catch) → Service (抛 BusinessException) → GlobalExceptionHandler (统一处理)

## 代码审查检查
审查时检查：异常层次、全局处理器覆盖、Service 层抛出时机、Controller 不 catch、日志级别区分、安全。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/springboot/exception-handling/`*
