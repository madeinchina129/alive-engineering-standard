# API 文档规范 — FAQ

## Q1: API 文档工具选什么？
Swagger/OpenAPI 是事实标准。前端推荐：Swagger UI（在线文档）、Redoc（静态文档）。基于代码生成：FastAPI（自动生成）、SpringDoc（Java）、drf-yasg（Django）。

## Q2: 文档应该多详细？
核心：端点用途、请求参数（类型/必填/默认）、响应结构（HTTP 状态码对应）、错误码。进阶：速率限制说明、版本历史、迁移指南、常见问题。
