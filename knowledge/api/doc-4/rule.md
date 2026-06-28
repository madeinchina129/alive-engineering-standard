# API 文档规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| API-DOC-001 | 所有 API 必须有 OpenAPI 3.0+ 规范文档 | P0 | 是 |
| API-DOC-002 | 每个 API 端点必须包含：描述、请求参数、响应结构、错误码 | P0 | 是 |
| API-DOC-003 | 文档必须包含可运行的示例代码（curl / Python / JS 等） | P0 | 是 |
| API-DOC-004 | 文档必须有 Base URL 和认证方式说明 | P0 | 是 |
| API-DOC-005 | 文档变更随代码变更一起 Code Review | P0 | 是 |
| API-DOC-006 | 文档必须提供 Postman Collection 或 OpenAPI Playground | P1 | 推荐 |

## 详细说明

### API-DOC-001（P0）
所有 API 必须有 OpenAPI 3.0+ 规范文档

### API-DOC-002（P0）
每个 API 端点必须包含：描述、请求参数、响应结构、错误码

### API-DOC-003（P0）
文档必须包含可运行的示例代码（curl / Python / JS 等）

### API-DOC-004（P0）
文档必须有 Base URL 和认证方式说明

### API-DOC-005（P0）
文档变更随代码变更一起 Code Review

### API-DOC-006（P1）
文档必须提供 Postman Collection 或 OpenAPI Playground

