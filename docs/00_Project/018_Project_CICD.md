# CI/CD 规范

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目的持续集成和持续交付流程标准，确保每次代码变更都经过自动化验证，并以标准化流程发布到目标环境。

## CI/CD 原则

```
1. 自动化优先 — 一切可自动化的步骤不要手动操作
2. 左移质量 — 问题越早发现修复成本越低
3. 不可变制品 — 构建一次，多次部署，不重复构建
4. 环境一致性 — 开发/测试/预发布/生产环境配置分离，运行时一致
5. 渐进式交付 — 灰度发布、金丝雀部署、回滚准备
```

## 流水线结构

### 标准化流水线

```
┌─ 触发 ─┬─ 构建 ─┬─ 质量 ─┬─ 测试 ─┬─ 发布 ┬─ 部署 ─┐
│        │        │        │        │        │        │
│ Push   │ 编译    │ Lint   │ 单元    │ 构建   │ 开发   │
│ MR     │ 依赖    │ SAST   │ 集成    │ 镜像   │ 测试   │
│ Tag    │ 缓存    │ SBOM   │ E2E     │ 签名   │ 预发布 │
│ 定时    │        │        │ 性能    │ 推送   │ 生产   │
└────────┴────────┴────────┴────────┴────────┴────────┘
```

## 阶段定义

### 1. 代码提交 (Trigger)

| 触发条件 | 执行流水线 | 说明 |
|----------|------------|------|
| Push to feature/* | 构建 + 质量 + 单元测试 | 快速反馈 |
| MR to develop | 完整流水线（不含生产部署） | 合入验证 |
| MR to main | 完整流水线 | 发布准备 |
| Tag v* | 完整流水线 + 生产部署 | 版本发布 |
| 定时（每日） | 完整流水线 | 基线验证 |

### 2. 构建 (Build)

```yaml
# 构建阶段必须完成：
- 依赖解析和缓存
- 编译（跳过测试以加速）
- 制品打包（jar/war/dist）
- 制品版本号自动生成（git describe）
- 制品上传至制品仓库（Nexus / Artifactory）
```

### 3. 质量 (Quality)

```yaml
quality:
  lint:
    - "eslint --max-warnings=50"
    - "mvn checkstyle:check"
  saast:
    - "sonar-scanner -Dsonar.qualitygate.wait=true"
  sbom:
    - "cyclonedx-maven:makeBom"
  secrets:
    - "trufflehog --fail-on-verification"
  license:
    - "mvn license:check"
```

质量门禁：

```
❌ 阻止条件：
  ├── SonarQube Quality Gate 失败
  ├── Lint 警告超过 50 个
  ├── 新增代码覆盖率 < 80%
  ├── 存在 Critical/High 漏洞
  └── 存在硬编码密钥
```

### 4. 测试 (Test)

必选测试：

```yaml
tests:
  - "单元测试 (必选)：覆盖率 >= 80%"
  - "集成测试 (必选)：关键路径覆盖"
  - "API 测试 (必选)：所有公开接口"
  - "性能测试 (建议)：核心接口 P95 对比"
  - "E2E 测试 (建议)：核心用户旅程"
```

### 5. 发布 (Release)

```yaml
release:
  versioning: "语义化版本 (SemVer 2.0)"
    - major: 不兼容的 API 变更
    - minor: 向下兼容的新功能
    - patch: 向下兼容的问题修复
  changelog: "自动生成（Conventional Commits）"
  artifact: "构建一次，签名后推送"
  approval: "生产发布需要至少 1 人审批"
```

### 6. 部署 (Deploy)

```yaml
# 部署策略
develop:    "自动部署，直接替换"
staging:    "自动部署，健康检查后切换"
production:
  strategy: "灰度发布，10% → 50% → 100%"
  interval: "每阶段观察 15 分钟"
  rollback: "一键回滚至上个版本（< 5 分钟）"
```

## 分支策略

```yaml
branches:
  main:
    protection: "禁止直接推送，仅 MR 合入"
    lifecycle: "生产版本"
  develop:
    protection: "禁止直接推送"
    lifecycle: "集成测试"
  feature/*:
    protection: "无"
    lifecycle: "开发中"
  release/*:
    protection: "仅 bug 修复"
    lifecycle: "预发布"
  hotfix/*:
    protection: "从 main 拉出，合回 main + develop"
    lifecycle: "紧急修复"
```

## 质量门禁配置

```yaml
quality_gates:
  - gate: "build"
    condition: "编译成功"
    action: "阻止后续阶段"
  - gate: "coverage"
    condition: "新增代码覆盖率 >= 80%"
    action: "阻止合并"
  - gate: "sonar"
    condition: "Quality Gate Passed"
    action: "阻止合并"
  - gate: "test"
    condition: "所有测试通过"
    action: "阻止合并"
  - gate: "approval"
    condition: "至少 1 人 Approve"
    action: "阻止生产发布"
  - gate: "performance"
    condition: "退化 < 5%"
    action: "需架构组审批"
```

## 发布日历

```yaml
release_calendar:
  cadence: "每两周一次常规发布"
  freeze: "重大节假日前 3 天冻结发布"
  hotfix: "P0/P1 问题不受冻结限制"
  schedule:
    - "周一: 代码冻结"
    - "周二: 预发布环境验证"
    - "周三: 生产发布 (10:00-11:00)"
    - "周四: 发布观察期"
    - "周五: 发布总结"
```

## 回滚流程

```yaml
rollback:
  trigger: "发布后 30 分钟内发现问题"
  decision: "架构师 / 值班负责人"
  process:
    1. "执行回滚脚本 (kubectl rollout undo)"
    2. "验证服务恢复"
    3. "通知相关方"
    4. "创建 Bug Issue"
    5. "发布复盘"
  time_target: "< 5 分钟"
```

## 监控与告警

```yaml
monitoring:
  during_release:
    - "错误率监控 (基线对比)"
    - "响应时间监控 (P95/P99)"
    - "服务可用性监控"
    - "业务指标监控"
  alerting:
    - "错误率上升 > 1% → 告警"
    - "P95 增加 > 50% → 告警"
    - "服务下线 → PagerDuty 电话"
```

## 相关文档

- [部署规范](../16_Deploy/16_deploy_部署规范.md)
- [发布规范](./009_Project_Release.md)
- [监控规范](../21_Operation/21_operation_监控告警规范.md)
