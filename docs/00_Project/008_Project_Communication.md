# Project Communication Standards

## 沟通原则

1. **异步优先** — 能用文档说的不开会，能用 IM 说的不等会议
2. **公开透明** — 默认公开讨论，仅在必要时私聊
3. **记录留存** — 所有重要决策必须文档化（ADR / Issue）
4. **及时响应** — Issue 和 PR 在 48 小时内应有回复

## Issue 规范

### Issue 类型

| 类型 | 标签 | 说明 |
|------|------|------|
| Bug | `bug` | 缺陷报告 |
| Feature | `enhancement` | 功能请求 |
| Documentation | `documentation` | 文档改进 |
| Discussion | `discussion` | 技术讨论 |
| Question | `question` | 问题咨询 |

### Issue 标题规范

```
<type>: <简短描述>
```

示例：

```
bug: 用户登录后 token 未正确刷新
feature: 添加批量导出功能
docs: 更新 API 文档中的参数说明
```

### Issue 内容模板

Bug 报告需包含：

1. 环境信息（OS、浏览器、版本）
2. 复现步骤
3. 期望行为
4. 实际行为
5. 截图 / 日志（如有）

功能请求需包含：

1. 动机 / 使用场景
2. 期望行为
3. 备选方案（如有）
4. 验收标准

## 文档沟通

| 沟通类型 | 工具 | 保存位置 |
|----------|------|----------|
| 技术设计 | ADR | `adr/` |
| API 变更 | OpenAPI | `openapi/` |
| 架构讨论 | Issue + Diagram | `diagrams/` |
| 日常同步 | Issue Comment | GitHub |
| 紧急联络 | IM / 飞书/钉钉 | 即时通讯 |

---

> **文档状态**: 初稿  
> **维护人**: 项目发起人  
> **最后更新**: 2026-06-28
