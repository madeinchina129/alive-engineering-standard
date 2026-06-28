# 技术选型标准

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目技术选型的评估框架、审批流程和已批准的技术栈。所有新技术的引入必须经过本规范的评估流程。

## 选型原则

### 1. 成熟度优先

优先选择经过大规模生产验证的技术。评估维度：

- 社区活跃度：GitHub Stars > 5K，最近 3 个月有 releases
- 生产验证：至少有 10 个已知生产案例
- 版本稳定性：主版本号 >= 1.x (非 beta/alpha)
- 维护者背景：有商业公司赞助或核心团队稳定

### 2. 团队匹配

选型必须考虑团队实际能力：

- 团队中至少 2 人熟悉该技术，或愿意承担学习成本
- 学习曲线不能超过 2 周（从引入到稳定产出）
- 中文文档和社区资源充足

### 3. 生态互通

新技术必须能与现有技术栈集成：

- 与已选框架无冲突
- 构建工具链兼容
- 监控和日志体系可接入

### 4. 长期可维护

- 技术生命周期预期 > 3 年
- 迁移成本可控
- 人才市场供应充足

## 已批准技术栈

### 后端

| 技术 | 版本 | 用途 | 状态 |
|------|------|------|------|
| Java | 17+ | 主开发语言 | baseline |
| Spring Boot | 3.x | 应用框架 | baseline |
| Maven/Gradle | - | 构建工具 | baseline |
| PostgreSQL | 15+ | 主数据库 | baseline |
| Redis | 7.x | 缓存 | baseline |
| RabbitMQ | 3.x | 消息队列 | approved |
| Docker | 24+ | 容器化 | baseline |

### 前端

| 技术 | 版本 | 用途 | 状态 |
|------|------|------|------|
| TypeScript | 5.x | 主开发语言 | baseline |
| Vue 3 | 3.x | 前端框架 | baseline |
| Pinia | 2.x | 状态管理 | baseline |
| Vite | 5.x | 构建工具 | baseline |
| Vitest | 1.x | 单元测试 | baseline |
| TailwindCSS | 3.x | 样式框架 | baseline |
| Element Plus | 2.x | UI 组件库 | approved |

### 移动端 (Flutter)

| 技术 | 版本 | 用途 | 状态 |
|------|------|------|------|
| Dart | 3.x | 开发语言 | baseline |
| Flutter | 3.x | 框架 | baseline |
| Riverpod | 2.x | 状态管理 | baseline |
| GoRouter | 14.x | 路由 | baseline |
| Dio | 5.x | HTTP | baseline |

### DevOps

| 技术 | 版本 | 用途 | 状态 |
|------|------|------|------|
| GitLab CI | - | CI/CD | baseline |
| SonarQube | 10.x | 代码质量 | baseline |
| Nexus | 3.x | 制品管理 | baseline |
| ELK | 8.x | 日志 | approved |

## 选型流程

```
需求提出 → 技术调研(3天) → 方案评审 → 概念验证(5天)
  ↓                                       ↓
  否决                                   提交 POC 报告
  ↑                                       ↓
  └──── 重新调研 ← 否决 ← 架构组审批 ←┘
```

### 流程角色

- **发起人**: 提出技术需求和调研结果
- **架构组**: 审批最终方案，至少 3 人参与评审
- **CTO**: 重大技术栈变更的最终决策人

### 审批标准

1. POC 必须覆盖核心功能场景
2. 必须提供性能基准对比数据
3. 必须评估安全风险
4. 必须有明确的回退方案

## 禁用技术

以下技术因维护成本、安全风险或淘汰原因，禁止引入：

- Java 8 (已结束商业支持)
- Spring Boot 1.x / 2.x (过渡版本)
- jQuery (不再作为项目依赖)
- Lombok @Data (团队格式争议，使用 record 替代)

## 技术债务管理

- 每个项目维护 tech-debt.md
- 季度性技术评估会议
- 技术债务利率按季度计算（每季度债务增长 10%）

## 版本更新策略

- 补丁版本：自动升级（Dependabot / Renovate）
- 次版本：评估后 2 周内采纳
- 主版本：评估后 1 个月内制定迁移计划

## 相关文档

- [项目原则](./002_Project_Principles.md)
- [依赖管理](./013_Project_Dependencies.md)
- [工具配置](./020_Project_Tools.md)
