# Project Directory Structure

## 仓库顶层结构

```
<repository-root>/
│
├── docs/                          # 文档目录（MkDocs）
│   ├── 00_Project/                # 项目基础文档
│   ├── 01_Product/                # 产品设计文档
│   ├── 02_Domain/                 # 领域模型文档
│   └── ...
│
├── prompts/                       # AI Prompt 模板
│
├── templates/                     # 各类模板（PRD, ADR, Issue 等）
│
├── contexts/                      # 上下文文档（供 AI 理解项目）
│
├── checklists/                    # 检查清单
│
├── examples/                      # 示例代码 / 示例文档
│
├── generator/                     # 代码生成器 / 脚手架
│
├── standards/                     # 标准规范详细文档
│
├── playbooks/                     # 运维手册 / 操作手册
│
├── knowledge/                     # 知识库
│
├── openapi/                       # OpenAPI 规范文件
│
├── sql/                           # SQL 脚本
│
├── diagrams/                      # 架构图源文件
│
├── scripts/                       # 辅助脚本
│
├── tools/                         # 工具配置
│
├── .github/                       # GitHub 配置（Actions, Issues 模板）
│
├── README.md                      # 项目说明
├── LICENSE                        # 许可证
├── CHANGELOG.md                   # 变更日志
├── ROADMAP.md                     # 路线图
├── CONTRIBUTING.md                # 贡献指南
├── SECURITY.md                    # 安全政策
├── CODE_OF_CONDUCT.md             # 行为准则
├── mkdocs.yml                     # MkDocs 配置
├── .gitignore                     # Git 忽略规则
└── .editorconfig                  # 编辑器配置
```

## 文档目录规范

```
docs/
├── 00_Project/          # 项目基础（概览、原则、命名、目录等）
├── 01_Product/          # 产品设计（PRD、用户故事、体验标准）
├── 02_Domain/           # 领域建模（实体、值对象、领域事件）
├── 03_Architecture/     # 架构设计（分层、模块、接口契约）
├── 04_Development/      # 开发规范（编码、测试、代码评审）
├── 05_DevOps/           # DevOps（CI/CD、部署、监控）
├── 06_Security/         # 安全规范
├── 07_Operations/       # 运维规范
├── 08_Compliance/       # 合规要求
└── 09_Appendices/       # 附录（术语表、参考资料）
```

## 文件编号规范

```
<序号>-<英文短描述>.md
```

- 序号：3 位数字，从 001 开始
- 描述：kebab-case 英文
- 示例：`001-project-overview.md`

## 模板目录规范

```
templates/
├── issue/               # Issue 模板
│   ├── bug-report.md
│   └── feature-request.md
├── pr/                  # Pull Request 模板
├── doc/                 # 文档模板
├── adr/                 # ADR 模板
│   └── adr-template.md
└── code/                # 代码模板
```

## Contexts 目录规范

```
contexts/
├── project-context.md   # 项目全局上下文
├── tech-stack.md        # 技术栈说明
└── team-roster.md       # 团队信息
```

---

> **文档状态**: 初稿  
> **维护人**: 项目发起人  
> **最后更新**: 2026-06-28
