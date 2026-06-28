# RESTful API 设计规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| API-REST-001 | URI 使用名词复数形式，如 /api/v1/users，不使用动词 | P0 | 是 |
| API-REST-002 | 使用标准 HTTP 方法：GET 查询、POST 创建、PUT 全量更新、PATCH 部分更新、DELETE 删除 | P0 | 是 |
| API-REST-003 | 使用正确 HTTP 状态码：200 成功、201 创建、400 参数错误、401 未认证、403 无权限、404 不存在、500 服务端错误 | P0 | 是 |
| API-REST-004 | 分页 API 必须返回 total/page/page_size/page_data 结构 | P0 | 是 |
| API-REST-005 | 错误响应必须包含 code / message / detail 三个字段 | P0 | 是 |
| API-REST-006 | 所有 API 必须有统一的请求 ID（X-Request-ID） | P0 | 是 |
| API-REST-007 | 响应体使用 JSON 格式，字段使用 camelCase | P0 | 是 |

## 详细说明

### API-REST-001（P0）
URI 使用名词复数形式，如 /api/v1/users，不使用动词

### API-REST-002（P0）
使用标准 HTTP 方法：GET 查询、POST 创建、PUT 全量更新、PATCH 部分更新、DELETE 删除

### API-REST-003（P0）
使用正确 HTTP 状态码：200 成功、201 创建、400 参数错误、401 未认证、403 无权限、404 不存在、500 服务端错误

### API-REST-004（P0）
分页 API 必须返回 total/page/page_size/page_data 结构

### API-REST-005（P0）
错误响应必须包含 code / message / detail 三个字段

### API-REST-006（P0）
所有 API 必须有统一的请求 ID（X-Request-ID）

### API-REST-007（P0）
响应体使用 JSON 格式，字段使用 camelCase

