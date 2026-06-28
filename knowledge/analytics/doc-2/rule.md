# 事件追踪标准 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| ANL-EVT-001 | 事件名采用 对象:动作 格式（如 user:login, order:create） | P0 | 是 |
| ANL-EVT-002 | 每个事件必须包含：event_id、user_id、timestamp、device_id | P0 | 是 |
| ANL-EVT-003 | 所有事件的属性结构必须预定义并版本化管理 | P0 | 是 |
| ANL-EVT-004 | 关键漏斗事件（注册/下单/支付）必须全量采集 | P0 | 是 |
| ANL-EVT-005 | 事件数据延迟超过 1 小时的数据需标记为延迟数据 | P1 | 推荐 |

## 详细说明

### ANL-EVT-001（P0）
事件名采用 对象:动作 格式（如 user:login, order:create）

### ANL-EVT-002（P0）
每个事件必须包含：event_id、user_id、timestamp、device_id

### ANL-EVT-003（P0）
所有事件的属性结构必须预定义并版本化管理

### ANL-EVT-004（P0）
关键漏斗事件（注册/下单/支付）必须全量采集

### ANL-EVT-005（P1）
事件数据延迟超过 1 小时的数据需标记为延迟数据

