# Project Naming Convention

## 命名总则

所有命名应遵循以下原则：

- **自解释**：名称本身能表达含义，不需要额外注释
- **一致性**：同类事物用同一种命名风格
- **简洁性**：在表达清晰的前提下尽可能短
- **避免缩写**：除非是行业通用缩写（API, UI, DB 等）

## 命名风格对照

| 风格 | 示例 | 适用场景 |
|------|------|----------|
| `kebab-case` | `project-overview.md` | 文件名、URL 路径 |
| `snake_case` | `user_profile` | 数据库表名、字段名、Python 变量 |
| `PascalCase` | `UserProfile` | 类名、类型名、组件名 |
| `camelCase` | `userProfile` | JavaScript/TypeScript 变量、函数名 |
| `SCREAMING_SNAKE_CASE` | `MAX_RETRY_COUNT` | 常量、环境变量名 |

## 项目命名规范

### 仓库命名

```
<ecosystem>-<project>-<component>
```

示例：

| 仓库 | 说明 |
|------|------|
| `alive-engineering-standard` | 工程标准规范总库 |
| `alive-user-service` | 用户服务 |
| `alive-frontend-web` | Web 前端 |

### 目录命名

使用 `kebab-case`：

```
docs/
  00-project/
  01-product/
  02-domain/
```

序号前缀用于控制排序（两位数字 + 下划线）。

### 文件命名

使用 `kebab-case` 或序号前缀：

```
001-project-overview.md
002-project-principles.md
```

### 分支命名

```
<type>/<scope>-<description>
```

示例：

| 分支 | 说明 |
|------|------|
| `feature/project-rule` | 新功能：项目规范 |
| `fix/typo-readme` | 修复 README 拼写 |
| `docs/api-usage` | 文档更新 |
| `release/v0.1.0` | 发布版本 |

### 提交信息（Commit Message）

遵循 Conventional Commits：

```
<type>(<scope>): <description>
```

| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 |
| `docs` | 文档 |
| `chore` | 工程化 |
| `refactor` | 重构 |
| `test` | 测试 |
| `ci` | CI/CD |
| `style` | 代码风格 |

示例：

```
docs(project): add project overview and principles
feat(api): add user login endpoint
fix(auth): resolve token refresh race condition
```

---

> **文档状态**: 初稿  
> **维护人**: 项目发起人  
> **最后更新**: 2026-06-28
