---
id: springboot.rest_api
priority: P0
owner: Java Team
version: 1.0
generated: 2026-06-28
---

# REST API 设计规范

> **领域**: Spring Boot 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> RESTful API 设计标准，URL 命名、HTTP 方法、状态码、响应格式

> **关联规范**: [Layered Architecture 分层规范](../20_SpringBoot/2001_LayeredArchitecture.md)


---

---

# REST API 设计规范

## 为什么需要 REST API 规范

统一的 API 设计让前端、后端、第三方开发者都能快速理解和使用 API。

### URL 命名规范

```
/api/v1/users              # 用户集合
/api/v1/users/123          # 单个用户
/api/v1/users/123/orders   # 用户的订单
/api/v1/products?page=1&size=20  # 分页查询
```

### HTTP 方法与语义

| 方法 | 操作 | 幂等 | 安全 | 响应码 |
|------|------|------|------|--------|
| GET | 查询资源 | ✅ | ✅ | 200 OK |
| POST | 创建资源 | ❌ | ❌ | 201 Created |
| PUT | 完全替换 | ✅ | ❌ | 200 OK |
| PATCH | 部分更新 | ❌ | ❌ | 200 OK |
| DELETE | 删除资源 | ✅ | ❌ | 204 No Content |

### 统一响应格式

```json
// 成功响应
{
  "code": 200,
  "message": "success",
  "data": { "id": 1, "name": "Alice" },
  "timestamp": "2026-06-28T12:00:00Z"
}

// 分页响应
{
  "code": 200,
  "message": "success",
  "data": {
    "content": [...],
    "page": 1,
    "size": 20,
    "totalElements": 100,
    "totalPages": 5
  }
}

// 错误响应
{
  "code": 400,
  "message": "Validation failed",
  "errors": [
    { "field": "email", "message": "邮箱格式不正确" }
  ],
  "timestamp": "2026-06-28T12:00:00Z"
}
```

---

## 对比其他设计风格

| 维度 | REST | GraphQL | gRPC |
|------|------|---------|------|
| 数据获取 | 固定结构 | 客户端按需 | protobuf |
| 缓存 | HTTP 缓存 | 需额外配置 | 需代理 |
| 学习成本 | 低 | 中 | 高 |
| 类型安全 | 无 | Schema | protobuf |
| 适用场景 | 标准 CRUD | 复杂数据需求 | 微服务通信 |

---

## 适用范围

- **强制使用**：所有对外 REST API
- **内部服务**：优先 REST，微服务间可选 gRPC

## 与项目其他部分的集成

- **Spring Boot**: Controller 层实现 REST 端点
- **Exception Handling**: 全局异常处理拦截错误并返回统一格式
- **JPA**: Repository 层向下提供数据访问


---

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


---

# REST API FAQ

## Q: 为什么用 ApiResponse 统一包装而不是直接返回实体？

A: 统一包装提供：
1. **一致性**：前端不需要为每个接口单独解析响应
2. **错误信息**：统一 error 字段传递错误详情
3. **元数据**：code/timestamp 提供请求追踪信息

## Q: PUT 和 PATCH 如何选择？

- **PUT**：替换整个资源（客户端发送完整对象）
- **PATCH**：部分更新（客户端只发送变更字段）

```java
// PUT: 必须提供所有字段
@PutMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> replace(
        @PathVariable Long id,
        @Valid @RequestBody UserReplaceRequest request) { // 所有必填字段
    return ResponseEntity.ok(ApiResponse.ok(userService.replace(id, request)));
}

// PATCH: 只提供要修改的字段
@PatchMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> update(
        @PathVariable Long id,
        @RequestBody UserUpdateRequest request) { // 只有可选字段
    return ResponseEntity.ok(ApiResponse.ok(userService.update(id, request)));
}
```

## Q: 如何处理批量操作？

A: 推荐使用 POST 传递操作类型：

```java
POST /api/v1/users/batch
{
  "operation": "DELETE",
  "ids": [1, 2, 3]
}
```

## Q: 是否应该支持 JSON Patch？

A: 只有在需要精细化部分更新的场景（如协同编辑），才引入 JSON Patch (RFC 6902)。

## Q: 大文件上传怎么设计？

```java
@PostMapping("/upload")
public ResponseEntity<ApiResponse<FileResponse>> upload(
        @RequestParam("file") MultipartFile file) {
    // 返回文件 ID，后续通过 GET /api/v1/files/{id} 访问
}
```

## Q: 如何设计 HATEOAS 链接？

A: 简单场景建议在响应体中包含 link 字段：

```java
public record ApiResponse<T>(
    int code, String message, T data,
    List<Link> links  // HATEOAS 链接
) {
    public record Link(String rel, String href, String method) {}
}
```

```json
{
  "data": { "id": 1, "name": "Alice" },
  "links": [
    { "rel": "self", "href": "/api/v1/users/1", "method": "GET" },
    { "rel": "orders", "href": "/api/v1/users/1/orders", "method": "GET" }
  ]
}
```


---

# REST API Code Review Checklist

## URL 设计
- [ ] 路径是否使用复数名词？（`/users` 而非 `/user`）
- [ ] 是否避免动词式 URL？（`/getUser` → `/users/{id}`）
- [ ] 是否使用 kebab-case？
- [ ] 版本是否在 URL 中？（`/api/v1/`）
- [ ] 嵌套层级是否不超过 3 级？

## HTTP 方法
- [ ] GET 是否不修改数据？
- [ ] POST 是否用于创建？
- [ ] PUT 是否幂等？
- [ ] DELETE 是否返回 204？
- [ ] 是否正确使用状态码？（200/201/204/400/404/500）

## 请求校验
- [ ] POST/PUT 是否使用 @Valid 校验？
- [ ] 校验错误是否有统一处理？
- [ ] 是否限制了请求体大小？
- [ ] 路径参数是否有基础校验？（@Positive, @Min)

## 响应格式
- [ ] 是否使用统一 ApiResponse 包装？
- [ ] 分页是否使用统一的 PageDto？
- [ ] 是否没有返回密码等敏感字段？
- [ ] 枚举是否返回字符串而非 index？

## 错误处理
- [ ] 是否使用全局 @ControllerAdvice？
- [ ] 错误消息是否用户友好？
- [ ] 是否包含错误码和字段级错误详情？
- [ ] 是否记录了审计日志？


---

你是一个 REST API 设计专家，精通 Spring Boot 后端开发。请根据以下规范回答问题。

## 核心规范

### URL 设计
```
/api/v1/users          # 集合（复数名词）
/api/v1/users/{id}     # 单个资源
/api/v1/users/{id}/orders  # 子资源（不超过3层）
```

- 使用复数名词，kebab-case
- 动词不在 URL 中（通过 HTTP 方法表达）
- 版本在 URL 中: `/api/v1/`, `/api/v2/`

### HTTP 方法
| 方法 | 用途 | 状态码 |
| GET | 查询 | 200 |
| POST | 创建 | 201 |
| PUT | 全量替换 | 200 |
| PATCH | 部分更新 | 200 |
| DELETE | 删除 | 204 |

### 统一响应格式
```json
{ "code": 200, "message": "success", "data": {}, "timestamp": "..." }
```

### 强制规则
1. 统一 ApiResponse 包装响应体
2. 使用 @Valid 校验请求体
3. 正确使用 HTTP 状态码
4. 分页接口返回统一格式 PageDto
5. 敏感操作记录审计日志
6. 不暴露密码等敏感字段
7. GET 接口不修改数据
8. 全局 @ControllerAdvice 处理异常

## 代码审查检查
审查时检查：URL 命名、HTTP 方法选择、响应包装、参数校验、状态码正确性、错误处理。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/springboot/rest-api/`*
