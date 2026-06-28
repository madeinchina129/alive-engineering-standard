---
id: project.naming
priority: P0
owner: Project Team
version: 1.0
generated: 2026-06-28
---

# 命名规范与目录约定

> **领域**: 项目规范 | **优先级**: P0 | **版本**: 1.0
> 
> 文件、变量、模块的命名标准和目录命名约定



---




# 命名规范与目录约定

## 概述
统一的命名规范是代码可读性的第一道保障。

## 核心原则
1. 表达意图：名称清晰表达用途而非实现
2. ['一致性：全项目统一命名风格']
3. ['避免缩写：除非是行业通用缩写']

## 适用范围
适用于本项目中所有相关场景。





---

## 使用规范

# 命名规范与目录约定 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| NN-001 | 类名使用 PascalCase：UserService | P0 | 是 |
| NN-002 | 方法名使用 camelCase：getUserById() | P0 | 是 |
| NN-003 | 常量名使用 UPPER_SNAKE_CASE | P1 | 是 |

## 详细说明

### NN-001（P0）
类名使用 PascalCase：UserService

### NN-002（P0）
方法名使用 camelCase：getUserById()

### NN-003（P1）
常量名使用 UPPER_SNAKE_CASE





---

// 正确
class UserService {}
void getUserById() {}
const MAX_RETRY_COUNT = 3;

// 错误
class userservice {}  // 应为 UserService
void getuserbyid() {}  // 应为 getUserById





---

## 常见问题

# 命名规范与目录约定 — FAQ

## Q1: 目录名怎么命名？
kebab-case（my-feature）或 snake_case（my_feature），项目统一。

## Q2: 文件名和类名关系？
一个文件一个类，文件名与类名相同。





---

## 检查清单

# 命名规范与目录约定 — 检查清单

- [ ] 命名风格统一
- [ ] 无拼音命名
- [ ] 无含义不明的缩写





---

## AI Prompt

# 命名规范与目录约定 — AI Prompt

## System Prompt
```
你是一个代码规范专家，需要制定命名规范。
```

## User Prompt 模板
```
请审查以下命名是否合规：{names}
```




---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/project/naming/`*