# API 安全规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| API-SEC-001 | 所有 API 必须使用 HTTPS/TLS 传输，禁止 HTTP | P0 | 是 |
| API-SEC-002 | 敏感 API 必须使用 OAuth 2.0 / JWT 认证 | P0 | 是 |
| API-SEC-003 | 所有用户输入必须进行参数校验和注入防护（SQL/XSS/命令注入） | P0 | 是 |
| API-SEC-004 | API 必须实施速率限制（Rate Limiting），防止滥用 | P0 | 是 |
| API-SEC-005 | API 响应中不能泄露敏感信息（堆栈跟踪、SQL 语句、内部 IP） | P0 | 是 |
| API-SEC-006 | 所有 API 操作必须记录审计日志（谁、什么时间、做了什么） | P0 | 是 |
| API-SEC-007 | API Key/Token 必须支持轮换和撤销 | P1 | 是 |

## 详细说明

### API-SEC-001（P0）
所有 API 必须使用 HTTPS/TLS 传输，禁止 HTTP

### API-SEC-002（P0）
敏感 API 必须使用 OAuth 2.0 / JWT 认证

### API-SEC-003（P0）
所有用户输入必须进行参数校验和注入防护（SQL/XSS/命令注入）

### API-SEC-004（P0）
API 必须实施速率限制（Rate Limiting），防止滥用

### API-SEC-005（P0）
API 响应中不能泄露敏感信息（堆栈跟踪、SQL 语句、内部 IP）

### API-SEC-006（P0）
所有 API 操作必须记录审计日志（谁、什么时间、做了什么）

### API-SEC-007（P1）
API Key/Token 必须支持轮换和撤销

