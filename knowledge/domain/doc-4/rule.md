# 领域事件规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DDD-EVT-001 | 事件命名使用过去时态（如 OrderSubmitted, PaymentReceived） | P0 | 是 |
| DDD-EVT-002 | 事件必须包含：event_id、event_type、timestamp、aggregate_id、payload | P0 | 是 |
| DDD-EVT-003 | 事件发布必须在聚合根的方法中完成，确保事务一致性 | P0 | 是 |
| DDD-EVT-004 | 事件消费方必须实现幂等处理 | P0 | 是 |

## 详细说明

### DDD-EVT-001（P0）
事件命名使用过去时态（如 OrderSubmitted, PaymentReceived）

### DDD-EVT-002（P0）
事件必须包含：event_id、event_type、timestamp、aggregate_id、payload

### DDD-EVT-003（P0）
事件发布必须在聚合根的方法中完成，确保事务一致性

### DDD-EVT-004（P0）
事件消费方必须实现幂等处理

