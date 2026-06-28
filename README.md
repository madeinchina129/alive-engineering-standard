<div align="center">

# Alive Engineering Standard (AES)

**企业级工程标准规范体系**

[![Version](https://img.shields.io/badge/version-v0.1.0--alpha-blue)](CHANGELOG.md)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-green)](https://madeinchina129.github.io/alive-engineering-standard)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

**让工程团队有标准可依，让 AI 编码有上下文可循**

</div>

---

## Introduction

Alive Engineering Standard (AES) 是一套面向现代软件工程团队的**全栈工程标准规范体系**。覆盖从项目立项、产品设计、技术选型、编码实现到部署运维的全生命周期。

与传统的文档规范不同，AES 提供：

- **可执行的模板与检查清单** — 每个规范配套对应的 CheckList
- **AI 友好的上下文文档** — 每个领域都有专属的 Prompt 和 Context
- **自动化文档生成器** — 通过配置文件一键生成规范文档
- **渐进式采纳** — 团队可以逐步引入，无需一次性全盘接受

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Entry Layer                           │
│           README · CHANGELOG · ROADMAP                    │
├──────────────────────────────────────────────────────────┤
│                     Core Layer                            │
│    Project → Product → Domain → Capability → Business    │
├──────────────────────────────────────────────────────────┤
│                   Engineering Layer                       │
│    Flutter · Vue3 · SpringBoot · AI · API · Database     │
├──────────────────────────────────────────────────────────┤
│                   Quality Layer                           │
│    Security · Test · Performance · Compliance             │
├──────────────────────────────────────────────────────────┤
│                   Delivery Layer                          │
│    Deploy · Operation · Analytics                         │
├──────────────────────────────────────────────────────────┤
│                   Asset Layer                             │
│    Template · Prompt · Context · Workflow · Checklist    │
└──────────────────────────────────────────────────────────┘
```

## Directory

```
alive-engineering-standard/
│
├── docs/                          # 文档体系（24 个领域分类）
├── prompts/                       # AI Prompt 模板
├── templates/                     # 文档/代码模板
├── contexts/                      # AI 上下文文档
├── checklists/                    # 检查清单
├── examples/                      # 示例代码
├── generator/                     # 文档生成器
├── standards/                     # 标准规范定义
├── playbooks/                     # 操作手册
├── knowledge/                     # 知识库
├── openapi/                       # API 规范
├── sql/                           # SQL 脚本
├── diagrams/                      # 架构图源文件
├── scripts/                       # 辅助脚本
├── tools/                         # 工具配置
├── assets/                        # 静态资源
├── adr/                           # 架构决策记录
└── .github/                       # GitHub 配置
```

## How to Use

### Quick Start

```bash
# 1. 克隆仓库
git clone https://github.com/madeinchina129/alive-engineering-standard.git
cd alive-engineering-standard

# 2. 安装文档生成器依赖
cd generator && pip install -r requirements.txt && cd ..

# 3. 浏览本地文档
mkdocs serve
# → http://localhost:8000
```

### Read the Docs

| 路径 | 内容 |
|------|------|
| `docs/00_Project/` | 项目基础规范 |
| `docs/01_Product/` | 产品设计规范 |
| `docs/10_Flutter/` | Flutter 开发规范 |
| `docs/11_Vue3/` | Vue3 开发规范 |
| `docs/12_SpringBoot/` | Spring Boot 开发规范 |
| `docs/13_AI/` | AI 开发规范 |

> 完整文档：https://madeinchina129.github.io/alive-engineering-standard

### Use Prompts

```bash
# AI 编码时加载对应上下文
cat contexts/flutter.md    # Flutter 项目上下文
cat prompts/flutter/*.md   # Flutter 相关 Prompt
```

### Use Templates

```
templates/
├── flutter/        # Flutter 项目模板
├── vue/            # Vue3 项目模板
├── spring/         # Spring Boot 项目模板
└── sql/            # SQL 脚本模板
```

### Generate Documentation

```bash
# 自动生成 Project 规范文档
python generator/generate_rule.py --domain project --count 20

# 自动生成 Prompt 文档
python generator/generate_prompt.py --domain flutter --count 50

# 查看所有生成选项
python generator/generate_rule.py --help
```

## Documentation

文档使用 [MkDocs](https://www.mkdocs.org/) + [Material Theme](https://squidfunk.github.io/mkdocs-material/) 构建，部署在 GitHub Pages。

```bash
# 本地预览
mkdocs serve

# 构建静态站点
mkdocs build

# 部署到 GitHub Pages
mkdocs gh-deploy
```

## Prompt

AES 提供了一套完整的 Prompt 体系，用于 AI 辅助编码：

- **领域 Prompt** — Flutter / Vue3 / Spring Boot / AI 等
- **工作流 Prompt** — 编码 / 审查 / 重构 / 调试
- **业务 Prompt** — 业务分析与建模

详见 [`prompts/`](prompts/)

## Template

标准化模板确保所有输出质量一致：

- **项目模板** — Flutter / Vue3 / Spring Boot
- **文档模板** — ADR / PRD / 技术设计
- **代码模板** — Controller / Service / Repository

详见 [`templates/`](templates/)

## Generator

文档生成器是 AES 的核心工程工具，支持从 YAML/JSON 配置自动生成规范文档：

```
generator/
├── generate_rule.py       # 规则文档生成器
├── generate_prompt.py     # Prompt 生成器
├── generate_template.py   # 模板生成器
├── generate_checklist.py  # 检查清单生成器
├── generate_context.py    # 上下文生成器
├── generate_api.py        # API 文档生成器
├── templates/             # Jinja2 模板
└── config/                # YAML 配置
```

详见 [`generator/`](generator/)

## Contribution

我们欢迎所有形式的贡献：

- [提交 Issue](https://github.com/madeinchina129/alive-engineering-standard/issues) — 报告问题或提出建议
- [提交 PR](https://github.com/madeinchina129/alive-engineering-standard/pulls) — 改进标准规范
- [讨论](https://github.com/madeinchina129/alive-engineering-standard/discussions) — 参与技术讨论

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE)。

