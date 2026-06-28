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
