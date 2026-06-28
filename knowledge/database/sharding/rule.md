# NoSQL 数据库设计 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DB-NS-001 | 选择 NoSQL 前必须评估是否真的需要 NoSQL（关系型优先） | P0 | 是 |
| DB-NS-002 | MongoDB 文档嵌套层级不超过 3 层 | P0 | 是 |
| DB-NS-003 | Redis key 命名使用 业务:实体:ID 格式（如 user:1001:profile） | P0 | 是 |
| DB-NS-004 | Redis 缓存必须设置 TTL，不允许永久缓存 | P0 | 是 |
| DB-NS-005 | MongoDB 必须为查询模式设计复合索引，不能有无索引查询 | P0 | 是 |
| DB-NS-006 | Cassandra/宽表数据库须按查询模式设计主键，不做全表扫描 | P0 | 是 |

## 详细说明

### DB-NS-001（P0）
选择 NoSQL 前必须评估是否真的需要 NoSQL（关系型优先）

### DB-NS-002（P0）
MongoDB 文档嵌套层级不超过 3 层

### DB-NS-003（P0）
Redis key 命名使用 业务:实体:ID 格式（如 user:1001:profile）

### DB-NS-004（P0）
Redis 缓存必须设置 TTL，不允许永久缓存

### DB-NS-005（P0）
MongoDB 必须为查询模式设计复合索引，不能有无索引查询

### DB-NS-006（P0）
Cassandra/宽表数据库须按查询模式设计主键，不做全表扫描

