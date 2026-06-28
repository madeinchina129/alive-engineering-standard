# REST API 设计规范

## URL 命名规则

### 资源命名

```
/users          # 用户资源（复数名词）
/users/123      # 单个用户（路径参数）
/users/123/orders  # 子资源
```

```java
// ✅ 正确
@RestController
@RequestMapping("/api/v1/users")
public class UserController { }

// ❌ 错误：动词式 URL
@RequestMapping("/api/v1/getUser")
@RequestMapping("/api/v1/createUser")
@RequestMapping("/api/v1/deleteUserById")
```

### 版本管理

```java
// 通过 URL 路径版本
@RequestMapping("/api/v1/users")   // v1
@RequestMapping("/api/v2/users")   // v2

// 版本控制策略：
// - 向后兼容的变更 → 无需升级版本
// - 破坏性变更 → 升级版本号
// - 每个版本独立 Controller 类
```

### 查询参数规范

```java
// 分页
GET /api/v1/users?page=1&size=20&sort=createdAt,desc

// 过滤
GET /api/v1/users?status=active&role=admin

// 搜索
GET /api/v1/users?search=alice

// 字段选择
GET /api/v1/users?fields=id,name,email
```

## 强制规则 (MUST)

### 1. 统一响应体

```java
public record ApiResponse<T>(
    @JsonInclude(Include.NON_NULL) int code,
    String message,
    @JsonInclude(Include.NON_NULL) T data,
    @JsonInclude(Include.NON_NULL) List<FieldError> errors,
    String timestamp
) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(200, "success", data, null, now());
    }

    public static <T> ApiResponse<T> created(T data) {
        return new ApiResponse<>(201, "created", data, null, now());
    }

    public static <T> ApiResponse<T> error(int code, String message) {
        return new ApiResponse<>(code, message, null, null, now());
    }

    private static String now() {
        return Instant.now().toString();
    }

    public record FieldError(String field, String message) {}
}
```

### 2. 使用 @Valid 校验请求体

```java
@PostMapping
public ResponseEntity<ApiResponse<UserResponse>> create(
        @Valid @RequestBody UserCreateRequest request) {
    return ResponseEntity.status(201)
            .body(ApiResponse.created(userService.create(request)));
}

// Request DTO
public record UserCreateRequest(
    @NotBlank String name,
    @Email @NotBlank String email,
    @Size(min = 8, max = 20) String password
) {}
```

### 3. 正确使用 HTTP 状态码

```java
@GetMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> findById(@PathVariable Long id) {
    return ResponseEntity.ok(ApiResponse.ok(userService.findById(id)));
    // 200 OK
}

@PostMapping
public ResponseEntity<ApiResponse<UserResponse>> create(@Valid @RequestBody UserCreateRequest req) {
    return ResponseEntity.status(HttpStatus.CREATED)
            .body(ApiResponse.created(userService.create(req)));
    // 201 Created
}

@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable Long id) {
    userService.delete(id);
    return ResponseEntity.noContent().build();
    // 204 No Content
}
```

### 4. 分页接口统一返回 Page 对象

```java
@GetMapping
public ResponseEntity<ApiResponse<PageDto<UserResponse>>> findAll(
        @PageableDefault(page = 0, size = 20) Pageable pageable) {
    Page<UserResponse> page = userService.findAll(pageable);
    return ResponseEntity.ok(ApiResponse.ok(PageDto.from(page)));
}

// Page DTO
public record PageDto<T>(
    List<T> content,
    int page,
    int size,
    long totalElements,
    int totalPages
) {
    public static <T> PageDto<T> from(Page<T> page) {
        return new PageDto<>(
            page.getContent(),
            page.getNumber(),
            page.getSize(),
            page.getTotalElements(),
            page.getTotalPages()
        );
    }
}
```

### 5. 敏感操作记录审计日志

```java
@PostMapping
@AuditLog(action = "CREATE_USER")
public ResponseEntity<ApiResponse<UserResponse>> create(@Valid @RequestBody ...) {
    // ...
}
```

## 推荐实践 (SHOULD)

### 1. 使用统一异常处理（见 Exception Handling 规范）

### 2. 避免多级嵌套资源 URL（超过 3 级）

```java
// ✅ 好: /api/v1/users/123/orders
// ❌ 不好: /api/v1/users/123/orders/456/items/789
```

### 3. 枚举参数使用 String 而非 Index

```java
// ✅
GET /api/v1/users?status=ACTIVE

// ❌
GET /api/v1/users?status=0
```

## 禁止行为 (MUST NOT)

- ❌ 在 URL 中使用动词（`/getUser`, `/createUser`）
- ❌ 返回未包装的原始数据（必须使用 ApiResponse 包装）
- ❌ 暴露内部 ID 格式（如自增 ID）
- ❌ GET 接口修改数据
- ❌ 返回密码等敏感字段
- ❌ 使用 HTTP 状态码传达业务错误（使用统一错误码）
