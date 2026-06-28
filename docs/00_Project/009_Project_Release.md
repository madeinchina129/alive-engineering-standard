# Release Management

## 版本号规范

遵循 Semantic Versioning (SemVer 2.0)：

```
主版本.次版本.补丁
  ↑      ↑      ↑
  │      │      └── 向后兼容的问题修复
  │      └───────── 向后兼容的新功能
  └─────────────── 不兼容的 API 变更
```

### 版本生命周期

| 阶段 | 标签 | 说明 |
|------|------|------|
| 开发中 | `-alpha` | 功能未冻结，可变更 |
| 内测 | `-beta` | 功能冻结，修复 bug |
| 候选 | `-rc.N` | 发布候选，第 N 版 |
| 正式 | 无后缀 | 正式发布 |
| 补丁 | 递增 patch | 紧急修复 |

示例：`v0.1.0-alpha` → `v0.1.0-beta` → `v0.1.0-rc.1` → `v0.1.0`

## 发布流程

```
1. 从 develop 创建 release/vX.Y.Z 分支
2. 在 release 分支上只修 bug，不增功能
3. 更新 CHANGELOG.md
4. 创建 Git Tag
5. 合并到 main（merge commit）
6. 合并回 develop
7. GitHub Release 发布
```

## CHANGELOG 规范

每个版本按以下格式记录：

```markdown
## [v0.1.0] - 2026-06-28

### Added
- 新功能 A
- 新功能 B

### Changed
- 变更 C

### Fixed
- 修复 D

### Removed
- 移除 E
```

## 标签规范

```
v<主版本>.<次版本>.<补丁>[-<预发布>]
```

示例：

```
v0.1.0-alpha
v0.1.0-beta
v0.1.0-rc.1
v0.1.0
v0.1.1
```

---

> **文档状态**: 初稿  
> **维护人**: 项目发起人  
> **最后更新**: 2026-06-28
