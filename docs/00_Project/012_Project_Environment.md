# 环境搭建规范

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目开发环境的标准化搭建流程，确保所有团队成员在一致的开发环境中工作，减少"我机器上能跑"类问题。

## 最低硬件要求

| 角色 | CPU | 内存 | 磁盘 | 网络 |
|------|-----|------|------|------|
| 后端开发 | 4核+ | 16GB+ | 256GB SSD | >10Mbps |
| 前端开发 | 4核+ | 8GB+ | 128GB SSD | >10Mbps |
| 全栈开发 | 8核+ | 32GB+ | 512GB SSD | >10Mbps |

## 操作系统

### 推荐

- **macOS**: 14.x (Sonoma) 或更高
- **Linux**: Ubuntu 22.04 LTS / 24.04 LTS
- **Windows**: Windows 11 + WSL2 (Ubuntu 22.04)

### 约束

- 不允许在 Windows 原生环境直接开发（路径分隔符、换行符等不一致问题）
- macOS 必须使用 ARM64 原生工具链
- Linux 必须使用 LTS 版本

## 必须安装的工具

### 版本管理

| 工具 | 版本 | 用途 |
|------|------|------|
| Git | 2.40+ | 版本控制 |
| SDKMAN | latest | Java 多版本管理 |
| nvm-windows / nvm | latest | Node.js 版本管理 |
| fvm | 3.x | Flutter 版本管理 |

### 运行时

| 工具 | 版本 | 用途 |
|------|------|------|
| JDK | 17 / 21 | Java 运行环境 |
| Node.js | 20 LTS | JavaScript 运行环境 |
| Dart | 3.x | Dart 运行环境 |
| Python | 3.11+ | 工具脚本 |

### 容器化

| 工具 | 版本 | 用途 |
|------|------|------|
| Docker Desktop | 4.x | 容器运行时 |
| Docker Compose | 2.x | 本地服务编排 |
| Podman (备用) | 4.x | 容器替代方案 |

### 数据库工具

| 工具 | 用途 |
|------|------|
| DBeaver / DataGrip | 数据库客户端 |
| Redis Insight | Redis 管理工具 |
| TablePlus | 轻量级数据库管理 |

## 开发环境检查清单

首次搭建开发环境时，逐项确认：

- [ ] Git 已配置用户名和邮箱
- [ ] SSH Key 已添加到 GitLab
- [ ] JDK 版本确认 (`java -version`)
- [ ] Node.js 版本确认 (`node -v`)
- [ ] Docker 运行正常 (`docker ps`)
- [ ] IDE 已安装推荐的插件扩展包
- [ ] 本地数据库服务启动正常
- [ ] 项目 `make setup` 或初始化脚本执行成功
- [ ] 项目本地构建成功 (`mvn clean install` / `npm run build`)
- [ ] 单元测试全部通过

## IDE 配置

### IntelliJ IDEA (后端)

必须安装的插件：

- SonarLint — 实时代码质量检查
- MapStruct Support — 映射注解支持
- Spring Assistant — Spring 配置提示
- Git ToolBox — Git 增强
- CheckStyle-IDEA — 代码风格检查

### VS Code (前端/全栈)

必须安装的插件：

- ESLint — 代码规范检查
- Prettier — 代码格式化
- Vue Language Features (Volar) — Vue3 支持
- Tailwind CSS IntelliSense — Tailwind 提示
- GitLens — Git 增强

### 通用设置

```yaml
# EditorConfig (.editorconfig)
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.java]
indent_size = 4
```

## 环境验证脚本

每次拉取新代码后，运行：

```bash
# 验证环境一致性
./scripts/verify-env.sh
```

该脚本检查：JDK 版本、Node 版本、Docker 运行状态、关键端口占用、Git 配置。

## 常见问题

### Docker 资源不足

```
解决: Docker Desktop → Settings → Resources
推荐: CPUs 4+, Memory 8GB+, Swap 2GB, Disk 64GB+
```

### Maven 依赖下载慢

```
解决: 配置公司 Nexus 镜像
~/.m2/settings.xml 中的 mirror 指向内部仓库
```

### Node 权限错误

```
解决: 不要使用 sudo npm install
使用 nvm 管理 Node 版本
npm prefix 设置为用户目录
```

## 相关文档

- [技术选型](./011_Project_TechStack.md)
- [工具配置](./020_Project_Tools.md)
- [依赖管理](./013_Project_Dependencies.md)
