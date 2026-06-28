# SQL 优化指南 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DB-SQL-001 | 生产环境禁止使用 SELECT *，必须明确列出查询列 | P0 | 是 |
| DB-SQL-002 | WHERE 条件中的索引列禁止使用函数包裹（如 WHERE YEAR(date) = 2024） | P0 | 是 |
| DB-SQL-003 | JOIN 条件中的列必须在两边都建索引 | P0 | 是 |
| DB-SQL-004 | 分页查询禁止使用 OFFSET 大偏移量，使用游标分页（WHERE id > last_id） | P0 | 是 |
| DB-SQL-005 | 慢查询阈值设置为 200ms，超过的必须优化 | P0 | 是 |
| DB-SQL-006 | IN 子查询尽量改为 JOIN 或 EXISTS | P1 | 是 |

## 详细说明

### DB-SQL-001（P0）
生产环境禁止使用 SELECT *，必须明确列出查询列

### DB-SQL-002（P0）
WHERE 条件中的索引列禁止使用函数包裹（如 WHERE YEAR(date) = 2024）

### DB-SQL-003（P0）
JOIN 条件中的列必须在两边都建索引

### DB-SQL-004（P0）
分页查询禁止使用 OFFSET 大偏移量，使用游标分页（WHERE id > last_id）

### DB-SQL-005（P0）
慢查询阈值设置为 200ms，超过的必须优化

### DB-SQL-006（P1）
IN 子查询尽量改为 JOIN 或 EXISTS

