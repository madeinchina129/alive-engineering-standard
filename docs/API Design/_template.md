# API 设计：[模块名称]

> 版本：1.0 | OpenAPI：3.0.3 | 最后更新：YYYY-MM-DD

---

## 1. API 总览

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/{resource}` | 资源列表 | JWT |
| POST | `/api/v1/{resource}` | 创建资源 | JWT |
| GET | `/api/v1/{resource}/{id}` | 资源详情 | JWT |
| PUT | `/api/v1/{resource}/{id}` | 更新资源 | JWT |
| DELETE | `/api/v1/{resource}/{id}` | 删除资源 | JWT |

## 2. 请求/响应格式

### 2.1 通用请求头
| 头 | 类型 | 必填 | 说明 |
|----|------|------|------|
| `Authorization` | `Bearer {token}` | 是 | JWT Token |
| `Content-Type` | `application/json` | 是 | 请求体格式 |
| `X-Request-Id` | UUID | 否 | 链路追踪 ID |

### 2.2 通用响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100
  }
}
```

### 2.3 错误响应格式
```json
{
  "code": 40001,
  "message": "参数错误",
  "detail": "field 'name' is required",
  "request_id": "xxx"
}
```

## 3. 接口详情

### 3.1 [端点名称]

`GET /api/v1/{resource}`

**Query 参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `page` | integer | 否 | 1 | 页码 |
| `page_size` | integer | 否 | 20 | 每页条数 |
| `sort` | string | 否 | -created_at | 排序 |

**响应示例**：
```json
{
  "code": 0,
  "data": [
    {
      "id": "uuid",
      "name": "string"
    }
  ],
  "meta": { "page": 1, "page_size": 20, "total": 50 }
}
```

### 3.2 [端点名称]

`POST /api/v1/{resource}`

**请求体**：
```json
{
  "name": "string (必填)",
  "description": "string (可选)"
}
```

## 4. 错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| 0 | 200 | 成功 |
| 40001 | 400 | 参数错误 |
| 40101 | 401 | 未认证 |
| 40301 | 403 | 无权限 |
| 40401 | 404 | 资源不存在 |
| 50001 | 500 | 服务器内部错误 |

## 5. 附录

- OpenAPI YAML：[链接]
- Postman Collection：[链接]
