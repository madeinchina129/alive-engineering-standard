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
