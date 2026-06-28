---
# 基础布局模板 — 所有文档类型继承此模板
# 包含文档头/尾的通用结构
---

> **Alive Engineering Standard** — 自动生成文档
> 版本：1.0 | 生成器版本：1.0.0 | 生成日期：2026-06-28

---

# 完整域间关系图谱

> 自动生成于 2026-06-28 | 版本：1.0

---

## 域间关系图

```mermaid
graph LR
    project["项目基础规范"]
    product["产品设计规范"]
    domain["领域设计规范"]
    capability["能力映射规范"]
    business["业务逻辑规范"]
    workflow["工作流规范"]
    event["事件驱动规范"]
    ui["UI/UX 规范"]
    api["API 设计规范"]
    database["数据库规范"]
    flutter["Flutter 开发规范"]
    vue3["Vue3 开发规范"]
    springboot["Spring Boot 开发规范"]
    ai["AI 开发规范"]
    security["安全规范"]
    test["测试规范"]
    deploy["部署规范"]
    template["模板规范"]
    prompt["Prompt 规范"]
    checklist["检查清单规范"]
    context["上下文规范"]
    operation["运维规范"]
    analytics["数据分析规范"]
    performance["性能规范"]
    compliance["合规规范"]
    product-.-->domain
    domain-->capability
    capability-.-->business
    business-->workflow
    workflow-.-->event
    event-.-->api
    ui==>api
    api-.-->database
    domain-.-->database
    project-.-->test
    test-.-->deploy
    security-.-->api
    security-.-->deploy
    deploy-.-->operation
    operation-.-->analytics
    analytics-.-->product
    performance-.-->deploy
    flutter-->ui
    vue3-->ui
    springboot-->api
    template-.-->checklist
    prompt-.-->context
    compliance-.-->security

    %% 图例
    %% -->  extends
    %% -.-->  references
    %% ==>  depends_on
```

## 关系说明

| 源域 | 关系 | 目标域 | 说明 |
|------|------|--------|------|
| product | 引用 | domain | 产品设计驱动领域建模 |
| domain | 扩展 | capability | 领域模型映射到业务能力 |
| capability | 引用 | business | 业务能力落地为业务逻辑 |
| business | 扩展 | workflow | 业务逻辑编排为工作流 |
| workflow | 引用 | event | 工作流触发领域事件 |
| event | 引用 | api | 事件驱动 API 设计 |
| ui | 依赖 | api | UI 层依赖 API 接口 |
| api | 引用 | database | API 实现依赖数据存储 |
| domain | 引用 | database | 领域模型映射为数据模型 |
| project | 引用 | test | 项目规范指导测试策略 |
| test | 引用 | deploy | 测试通过进入部署 |
| security | 引用 | api | API 需要安全防护 |
| security | 引用 | deploy | 部署需要安全配置 |
| deploy | 引用 | operation | 部署产物进入运维 |
| operation | 引用 | analytics | 运维数据驱动分析 |
| analytics | 引用 | product | 分析结果反馈产品优化 |
| performance | 引用 | deploy | 性能指标影响部署策略 |
| flutter | 扩展 | ui | Flutter 实现 UI 规范 |
| vue3 | 扩展 | ui | Vue3 实现 UI 规范 |
| springboot | 扩展 | api | Spring Boot 实现 API 规范 |
| template | 引用 | checklist | 模板规范定义检查清单格式 |
| prompt | 引用 | context | Prompt 依赖上下文规范 |
| compliance | 引用 | security | 合规要求驱动安全策略 |

## 统计

- 域数量：25
- 文档数量：118
- 关系数量：23

---

---
> 本文档由 AES 文档生成器自动生成
> 最后更新：2026-06-28 | 版本：1.0
