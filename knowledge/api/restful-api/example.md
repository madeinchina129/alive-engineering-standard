```json
// 请求: GET /api/v1/users?page=1&page_size=20&status=active
// 响应: 200 OK
{
  "code": 0,
  "message": "success",
  "data": {
    "page": 1,
    "page_size": 20,
    "total": 156,
    "items": [
      {
        "id": 1001,
        "name": "张三",
        "email": "zhang@example.com",
        "status": "active",
        "created_at": "2024-01-15T08:00:00Z"
      }
    ]
  },
  "request_id": "req-abc123"
}

// 请求: POST /api/v1/users
// Body:
{
  "name": "张三",
  "email": "zhang@example.com",
  "phone": "13800138000"
}
// 响应: 201 Created

// 请求: GET /api/v1/users/1001
// 响应: 200 OK

// 请求: GET /api/v1/users/9999
// 响应: 404 Not Found
{
  "code": 40401,
  "message": "resource_not_found",
  "detail": "用户 9999 不存在",
  "request_id": "req-def456"
}

// 请求: GET /api/v1/users/1001/orders?page=1&page_size=10
// 子资源嵌套
{
  "code": 0,
  "data": {
    "page": 1,
    "page_size": 10,
    "total": 5,
    "items": [...]
  }
}
```