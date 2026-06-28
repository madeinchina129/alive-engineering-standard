# 事件契约标准 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| EDA-CTG-001 | 所有业务事件必须使用 Avro/Protobuf/JSON Schema 定义格式 | P0 | 是 |
| EDA-CTG-002 | 事件字段只允许新增，不允许修改或删除已有字段 | P0 | 是 |
| EDA-CTG-003 | 新增字段必须标记为 optional，且提供默认值 | P0 | 是 |
| EDA-CTG-004 | Schema 变更必须通过兼容性校验（向后兼容） | P0 | 是 |
| EDA-CTG-005 | 每个事件必须包含 event_schema_version 字段 | P1 | 推荐 |

## 详细说明

### EDA-CTG-001（P0）
所有业务事件必须使用 Avro/Protobuf/JSON Schema 定义格式

### EDA-CTG-002（P0）
事件字段只允许新增，不允许修改或删除已有字段

### EDA-CTG-003（P0）
新增字段必须标记为 optional，且提供默认值

### EDA-CTG-004（P0）
Schema 变更必须通过兼容性校验（向后兼容）

### EDA-CTG-005（P1）
每个事件必须包含 event_schema_version 字段

