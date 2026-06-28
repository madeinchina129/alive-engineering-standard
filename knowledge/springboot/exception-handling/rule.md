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
