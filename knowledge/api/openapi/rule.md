# GraphQL API 设计规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| API-GQL-001 | 所有 GraphQL API 必须有查询深度限制（默认为 5 层） | P0 | 是 |
| API-GQL-002 | 所有 Mutation 必须是幂等的（可重试安全） | P0 | 是 |
| API-GQL-003 | N+1 查询必须使用 DataLoader 批量加载 | P0 | 是 |
| API-GQL-004 | Schema 类型命名使用 PascalCase，字段使用 camelCase | P0 | 是 |
| API-GQL-005 | 敏感字段（密码、Token）不能暴露在 Schema 中 | P0 | 是 |
| API-GQL-006 | 复杂查询必须做复杂度分析（Complexity Analysis） | P1 | 是 |

## 详细说明

### API-GQL-001（P0）
所有 GraphQL API 必须有查询深度限制（默认为 5 层）

### API-GQL-002（P0）
所有 Mutation 必须是幂等的（可重试安全）

### API-GQL-003（P0）
N+1 查询必须使用 DataLoader 批量加载

### API-GQL-004（P0）
Schema 类型命名使用 PascalCase，字段使用 camelCase

### API-GQL-005（P0）
敏感字段（密码、Token）不能暴露在 Schema 中

### API-GQL-006（P1）
复杂查询必须做复杂度分析（Complexity Analysis）

