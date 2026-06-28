# Project Workflow

## 开发工作流（Git Flow）

本仓库采用标准 Git Flow 作为分支策略。

### 分支结构

```
main          ─── 发布版本（只接受 develop 合并）
  ↑
develop       ─── 开发主线（所有 feature 合并于此）
  ↑
feature/*     ─── 特性分支（从 develop 拉出，合回 develop）
hotfix/*      ─── 热修复分支（从 main 拉出，合回 main 和 develop）
release/*     ─── 发布候选分支（从 develop 拉出，合回 main）
```

### 日常开发流程

```
1. git checkout develop
2. git pull origin develop
3. git checkout -b feature/my-feature
   ... 开发、提交 ...
4. git push -u origin feature/my-feature
5. 创建 PR → develop
6. 代码评审通过 → 合入 develop
7. 发布时 develop → main
```

### PR 规范

每个 PR 必须包含：

- **标题**：遵循 Conventional Commits
- **描述**：变更内容、动机、测试说明
- **关联 Issue**：`Closes #123`
- **检查清单**：确认已完成自测、文档更新等

### 合并策略

| 合入方向 | 策略 | 说明 |
|----------|------|------|
| feature → develop | Squash merge | 一个特性一个提交，保持历史清晰 |
| develop → main | Merge commit | 保留合并轨迹，便于回溯 |
| hotfix → main | Squash merge | 快速修复，直接合入 |
| main ← develop | Merge commit | 发布时保留完整历史 |

---

> **文档状态**: 初稿  
> **维护人**: 项目发起人  
> **最后更新**: 2026-06-28
