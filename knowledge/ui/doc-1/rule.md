# 组件库标准 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| UI-CMP-001 | 组件必须使用 PascalCase 命名，文件名与组件名一致 | P0 | 是 |
| UI-CMP-002 | 每个组件必须有类型完备的 Props/Parameters 定义 | P0 | 是 |
| UI-CMP-003 | 组件默认值必须处理 null/undefined 状态 | P0 | 是 |
| UI-CMP-004 | 原子组件（Button/Input/Icon）必须覆盖全部交互状态 | P1 | 是 |
| UI-CMP-005 | 复合组件必须拆分为子组件，每个子组件不超过 200 行 | P1 | 是 |
| UI-CMP-006 | 组件文档必须包含：用途说明、API 文档、使用示例、设计指引 | P1 | 是 |
| UI-CMP-007 | 组件样式必须使用设计令牌（Design Tokens），禁止硬编码色值 | P0 | 是 |
| UI-CMP-008 | 组件必须支持暗黑模式（通过 ThemeProvider 切换） | P1 | 推荐 |
| UI-CMP-009 | 组件包体积应控制在 5KB 以内（gzip 后） | P2 | 否 |

## 详细说明

### UI-CMP-001（P0）
组件必须使用 PascalCase 命名，文件名与组件名一致

### UI-CMP-002（P0）
每个组件必须有类型完备的 Props/Parameters 定义

### UI-CMP-003（P0）
组件默认值必须处理 null/undefined 状态

### UI-CMP-004（P1）
原子组件（Button/Input/Icon）必须覆盖全部交互状态

### UI-CMP-005（P1）
复合组件必须拆分为子组件，每个子组件不超过 200 行

### UI-CMP-006（P1）
组件文档必须包含：用途说明、API 文档、使用示例、设计指引

### UI-CMP-007（P0）
组件样式必须使用设计令牌（Design Tokens），禁止硬编码色值

### UI-CMP-008（P1）
组件必须支持暗黑模式（通过 ThemeProvider 切换）

### UI-CMP-009（P2）
组件包体积应控制在 5KB 以内（gzip 后）

