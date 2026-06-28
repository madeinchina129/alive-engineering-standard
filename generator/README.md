# Alive Generator

企业级工程知识库文档生成器。

## 安装

```bash
pip install -e generator/
```

## 用法

```bash
# 生成全部文档
python -m generator generate all

# 生成指定领域文档
python -m generator generate flutter
python -m generator generate spring   # 自动映射到 springboot
python -m generator generate vue      # 自动映射到 vue3

# 单类型生成（保留原 CLI）
python -m generator --domain flutter --type rule
python -m generator --domain flutter --type prompt
python -m generator --domain flutter --type checklist
python -m generator --domain flutter --type context

# 列出所有领域
python -m generator --list

# JSON 输出
python -m generator --domain flutter --format json
```

## 架构

```
generator/
├── cli.py                # 命令行入口
├── engine.py             # 生成引擎
├── config.py             # YAML 配置加载
├── models.py             # Pydantic 数据模型
├── utils.py              # 工具函数
├── config/
│   └── domain.yaml       # 24 领域 × 160+ 文档定义
├── templates/            # Jinja2 模板
│   ├── layout.md.j2      # 基础布局
│   ├── rule.md.j2        # 规范文档 (373 行)
│   ├── prompt.md.j2      # Prompt 文档 (186 行)
│   ├── checklist.md.j2   # 检查清单 (110 行)
│   ├── context.md.j2     # AI 上下文 (115 行)
│   ├── graph.md.j2       # 域间关系图
│   └── code/             # 代码生成模板
├── generators/           # 生成器实现
│   ├── rule.py
│   ├── prompt.py
│   ├── checklist.py
│   ├── context.py
│   ├── graph.py
│   └── code.py
├── tests/
├── pyproject.toml
└── README.md
```

## 生成产物

| 目录 | 领域 | 文件数 |
|------|------|--------|
| `docs/00_Project` | 项目基础 | 10 |
| `docs/10_Flutter` | Flutter | 28 |
| `docs/12_SpringBoot` | Spring Boot | 28 |
| `docs/11_Vue3` | Vue3 | 24 |
| ... | 共 24 领域 | 472+ |

每个文档包含：规范规则 + 代码示例 + 检查清单 + AI Prompt + 上下文文档。

## 自定义

编辑 `config/domain.yaml` 添加或修改文档定义。编辑 `templates/*.md.j2` 修改输出格式。
