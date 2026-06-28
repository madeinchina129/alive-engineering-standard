# 测试驱动开发方法论 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| TST-TDD-001 | 遵循红-绿-重构三步循环：Red（失败测试）→ Green（通过）→ Refactor（重构） | P0 | 是 |
| TST-TDD-002 | 每个 TDD 循环不超过 10 分钟 | P0 | 是 |
| TST-TDD-003 | TDD 过程中所有已有测试必须保持通过 | P0 | 是 |
| TST-TDD-004 | 先写功能测试再写单元测试（Outside-In TDD 或 Inside-Out TDD） | P1 | 推荐 |
| TST-TDD-005 | 重构步骤不允许新增功能，只能改善设计 | P0 | 是 |

## 详细说明

### TST-TDD-001（P0）
遵循红-绿-重构三步循环：Red（失败测试）→ Green（通过）→ Refactor（重构）

### TST-TDD-002（P0）
每个 TDD 循环不超过 10 分钟

### TST-TDD-003（P0）
TDD 过程中所有已有测试必须保持通过

### TST-TDD-004（P1）
先写功能测试再写单元测试（Outside-In TDD 或 Inside-Out TDD）

### TST-TDD-005（P0）
重构步骤不允许新增功能，只能改善设计

