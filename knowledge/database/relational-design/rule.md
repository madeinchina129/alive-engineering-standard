# 关系型数据库设计规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DB-RD-001 | 每张表必须有主键（自增 BIGINT 或 UUID v4） | P0 | 是 |
| DB-RD-002 | 字段必须定义 NOT NULL 和有意义的 DEFAULT 值 | P0 | 是 |
| DB-RD-003 | 所有表必须有 created_at 和 updated_at 时间戳字段 | P0 | 是 |
| DB-RD-004 | 表名使用业务领域名_实体名（复数）格式如 order_item | P0 | 是 |
| DB-RD-005 | 字段名使用小写蛇形（snake_case） | P0 | 是 |
| DB-RD-006 | 外键必须建索引，且 ON DELETE 行为需明确指定 | P1 | 是 |
| DB-RD-007 | 超过 1000 万行的表必须考虑分表或分区 | P1 | 推荐 |

## 详细说明

### DB-RD-001（P0）
每张表必须有主键（自增 BIGINT 或 UUID v4）

### DB-RD-002（P0）
字段必须定义 NOT NULL 和有意义的 DEFAULT 值

### DB-RD-003（P0）
所有表必须有 created_at 和 updated_at 时间戳字段

### DB-RD-004（P0）
表名使用业务领域名_实体名（复数）格式如 order_item

### DB-RD-005（P0）
字段名使用小写蛇形（snake_case）

### DB-RD-006（P1）
外键必须建索引，且 ON DELETE 行为需明确指定

### DB-RD-007（P1）
超过 1000 万行的表必须考虑分表或分区

