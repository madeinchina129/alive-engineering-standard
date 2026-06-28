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
