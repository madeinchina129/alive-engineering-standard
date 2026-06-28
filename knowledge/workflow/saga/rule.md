# Saga 分布式事务 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| WF-SAGA-001 | Saga 中的每一步必须有对应的补偿操作（Compensation） | P0 | 是 |
| WF-SAGA-002 | Saga 执行必须记录执行状态和执行历史 | P0 | 是 |
| WF-SAGA-003 | Saga 失败后必须执行完整的补偿流程（逆向回滚） | P0 | 是 |
| WF-SAGA-004 | Saga 编排推荐使用编排模式（Orchestration）而非舞蹈模式（Choreography） | P0 | 是 |
| WF-SAGA-005 | Saga 协调器必须做好容错和幂等处理 | P1 | 推荐 |

## 详细说明

### WF-SAGA-001（P0）
Saga 中的每一步必须有对应的补偿操作（Compensation）

### WF-SAGA-002（P0）
Saga 执行必须记录执行状态和执行历史

### WF-SAGA-003（P0）
Saga 失败后必须执行完整的补偿流程（逆向回滚）

### WF-SAGA-004（P0）
Saga 编排推荐使用编排模式（Orchestration）而非舞蹈模式（Choreography）

### WF-SAGA-005（P1）
Saga 协调器必须做好容错和幂等处理

