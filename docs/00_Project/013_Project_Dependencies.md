# 依赖管理策略

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目依赖的引入、更新、审计和移除全生命周期管理规范，确保依赖安全性和可维护性。

## 依赖引入原则

### 1. 最小依赖原则

- 每一个依赖必须有明确的不可替代的价值
- 能用标准库实现的，不引入第三方库
- 引入前确认是否已有项目内部工具类覆盖
- 优先选择无传递依赖或传递依赖少的库

### 2. 单一职责

- 一个库只做一件事并做好
- 避免"瑞士军刀"式的大而全依赖（如 commons-lang3 的过度使用）
- 功能耦合度低的依赖分别管理

### 3. 许可证合规

```yaml
# 许可证接受矩阵
MIT:        ✅ 无条件接受
Apache 2.0: ✅ 无条件接受
BSD:        ✅ 无条件接受
LGPL:       ⚠️ 需法务审核使用范围
GPL:        ❌ 禁止引入（传染性许可）
AGPL:       ❌ 禁止引入
SSPL:       ❌ 禁止引入
```

## 依赖版本管理

### Maven (后端)

```xml
<!-- 统一版本管理，禁止在子模块硬编码版本号 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

规则：
- 所有版本号集中在根 `pom.xml` 的 `<properties>` 中
- 子模块 `<dependencies>` 不允许出现 `<version>`
- BOM（Bill of Materials）优先于手动指定版本

### npm / pnpm (前端)

```json
{
  "dependencies": {
    "vue": "workspace:^",
    "pinia": "~2.1.0"
  },
  "packageManager": "pnpm@9.1.0"
}
```

规则：
- 使用 `pnpm` 锁定版本（替代 npm）
- `dependencies` 使用 `^` 允许次版本升级
- `devDependencies` 使用 `~` 仅允许补丁升级
- 禁止使用 `*` 通配版本

## 安全审计

### 自动化检查

```bash
# 后端
mvn ossindex:audit          # OSS Index 安全审计
mvn dependency-check:check  # OWASP Dependency Check

# 前端
pnpm audit                  # npm 安全审计
pnpm audit --fix            # 自动修复可修复的漏洞
```

### 安全门槛

- 允许 0 个 Critical 漏洞
- 允许 0 个 High 漏洞（超过 30 天未修复必须上报）
- Medium 漏洞需在 90 天内评估
- Low 漏洞在版本升级时附带修复

### 告警响应

| 等级 | 响应时限 | 措施 |
|------|----------|------|
| Critical | 24小时 | 立即升级或移除 |
| High | 7天 | 制定升级计划 |
| Medium | 90天 | 在下个版本修复 |
| Low | 下次发布 | 附带修复 |

## 依赖升级策略

### 自动升级

配置 Renovate / Dependabot 自动提 PR：

```json
{
  "extends": ["config:base"],
  "schedule": ["before 9am on Monday"],
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["minor"],
      "automerge": false
    }
  ]
}
```

### 升级审查

- Patch 版本：自动合并，无需审查
- Minor 版本：人工审查，需 1 人 Approve
- Major 版本：需架构组评审 + 迁移计划

## 依赖移除

以下情况必须移除依赖：

1. 依赖的 API 在项目代码中被替换/删除
2. 依赖版本超过 2 个大版本未升级
3. 依赖已有 6 个月未收到安全更新
4. 依赖与新的技术栈冲突

### 移除流程

```
标记 deprecated → 通知团队(1周缓冲期) → 移除代码依赖
  ↓                                                      
  清理 pom.xml / package.json → 验证构建通过 → 删除遗留注释
```

## 依赖可视化

```bash
# Maven 依赖树
mvn dependency:tree -DoutputType=graphml

# npm 依赖分析
pnpm ls --depth=10

# 定期生成依赖报告，检查循环依赖
mvn dependency:analyze
```

## 禁止行为

- ❌ 在代码中直接硬编码第三方库的内部类
- ❌ 在非 dev 依赖中使用 SNAPSHOT 版本
- ❌ 私有化公共库（fork 后闭源修改）
- ❌ 在 CI 中关闭安全审计检查

## 相关文档

- [技术选型](./011_Project_TechStack.md)
- [环境搭建](./012_Project_Environment.md)
- [CI/CD 规范](./018_Project_CICD.md)
