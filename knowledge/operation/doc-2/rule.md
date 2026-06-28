# 日志管理规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| OPS-LOG-001 | 所有应用日志必须使用结构化格式（JSON），包含：timestamp、level、logger、message、trace_id | P0 | 是 |
| OPS-LOG-002 | 日志级别分五级：TRACE < DEBUG < INFO < WARN < ERROR | P0 | 是 |
| OPS-LOG-003 | 生产环境日志级别默认为 INFO，DEBUG 级别需动态开启 | P0 | 是 |
| OPS-LOG-004 | 日志中禁止记录密码、Token、身份证号等敏感信息 | P0 | 是 |
| OPS-LOG-005 | 日志存储周期：ERROR 日志 30 天，INFO 日志 15 天，DEBUG 日志 7 天 | P1 | 推荐 |

## 详细说明

### OPS-LOG-001（P0）
所有应用日志必须使用结构化格式（JSON），包含：timestamp、level、logger、message、trace_id

### OPS-LOG-002（P0）
日志级别分五级：TRACE < DEBUG < INFO < WARN < ERROR

### OPS-LOG-003（P0）
生产环境日志级别默认为 INFO，DEBUG 级别需动态开启

### OPS-LOG-004（P0）
日志中禁止记录密码、Token、身份证号等敏感信息

### OPS-LOG-005（P1）
日志存储周期：ERROR 日志 30 天，INFO 日志 15 天，DEBUG 日志 7 天

