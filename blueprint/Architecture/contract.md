# 仓间契约

> 定义 blueprint → standard → generator → app 之间的数据结构与接口。
> 版本：1.0 | 最后更新：2026-06-28

---

## 1. 契约总览

```
┌─────────────────────────────────────────────────────────────────┐
│                  Blueprint（设计层）                               │
│  ┌──────────┐  ┌────────────┐  ┌───────────┐                    │
│  │ Roadmap/ │  │ Architecture│  │ Specification/                 │
│  │ 规划. md  │  │ 架构. md    │  │ 实体规格.md │                    │
│  └────┬─────┘  └─────┬──────┘  └─────┬─────┘                    │
│       │              │               │                           │
│       ▼              ▼               ▼                           │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              Blueprint → Standard 契约                │        │
│  │  格式: YAML (DomainConfig)                           │        │
│  │  描述: 领域定义、实体结构、API 端点、字段清单              │        │
│  └─────────────────────┬───────────────────────────────┘        │
├────────────────────────┼────────────────────────────────────────┤
│                  Standard（规则层）◄──────────────────────┘       │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  generator/models.py: Pydantic 模型                  │        │
│  │  generator/config/base.yaml: 领域配置                 │        │
│  └─────────────────────┬───────────────────────────────┘        │
│                        │                                        │
│  ┌─────────────────────▼───────────────────────────────┐        │
│  │              Standard → Generator 契约                │        │
│  │  格式: RenderedContext (dict)                        │        │
│  │  描述: 经 Standard 处理后的渲染上下文，供 Jinja2 模板使用 │        │
│  └─────────────────────┬───────────────────────────────┘        │
├────────────────────────┼────────────────────────────────────────┤
│                  Generator（生成层）◄──────────────────────┘      │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  模板引擎: Jinja2                                    │        │
│  │  模板: templates/ + templates/code/                  │        │
│  │  生成器: generators/*.py                              │        │
│  └─────────────────────┬───────────────────────────────┘        │
│                        │                                        │
│  ┌─────────────────────▼───────────────────────────────┐        │
│  │              Generator → App 契约                    │        │
│  │  格式: 源码文件 (.md / .dart / .java / .vue)         │        │
│  │  描述: 可编译/可运行的源代码文件                        │        │
│  └─────────────────────┬───────────────────────────────┘        │
├────────────────────────┼────────────────────────────────────────┤
│                  App（应用层）◄───────────────────────────┘      │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  docs/          — MkDocs 文档站点                     │        │
│  │  apps/mobile-flutter — Flutter 应用                  │        │
│  │  backend/       — Spring Boot 微服务                 │        │
│  │  apps/admin-vue3 — 管理后台                          │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 契约分层定义

### 2.1 Blueprint → Standard 契约

**输入**：Blueprint 目录下的 Markdown 文档（人类可读的设计规格）。

**输出**：`generator/config/` 下的 YAML 配置文件（机器可读）。

**领域配置 schema**（定义在 `generator/models.py` 的 `DomainConfig`）：

```yaml
# generator/config/domains/alive-mood.yaml
domain: alive-mood
version: "1.0"
title: "情感记录"
description: "用户每日情绪记录与分析"
entities:
  - name: MoodRecord
    module: mood
    display_name: "情绪记录"
    fields:
      - name: id
        type: uuid
        required: true
        primary_key: true
      - name: user_id
        type: uuid
        required: true
        fk: User.id
      - name: mood_score
        type: integer
        required: true
        min: 1
        max: 5
      - name: note
        type: text
        required: false
        max_length: 500
      - name: emoji
        type: string
        required: false
      - name: record_date
        type: date
        required: true
      - name: created_at
        type: datetime
        auto: true
api_endpoints:
  - path: /api/v1/mood
    method: POST
    operation: create
  - path: /api/v1/mood
    method: GET
    operation: list
  - path: /api/v1/mood/{id}
    method: GET
    operation: detail
  - path: /api/v1/mood/{id}
    method: PUT
    operation: update
  - path: /api/v1/mood/{id}
    method: DELETE
    operation: delete
```

**Pydantic 模型（合同校验）**：

| 模型 | 文件 | 用途 |
|------|------|------|
| `DomainConfig` | `models.py` | 顶层领域配置 |
| `EntityConfig` | `models.py` | 实体定义（字段、关系） |
| `FieldConfig` | `models.py` | 字段定义（类型、约束） |
| `ApiEndpoint` | `models.py` | API 端点定义 |

### 2.2 Standard → Generator 契约

**输入**：经过 Standard 处理后的结构化上下文（Python `dict`）。

**处理流程**：

```
DomainConfig (YAML)
    ↓ Pydantic 校验
Validated DomainConfig
    ↓ Config 扩充（注入默认值、拆解实体关系）
Expanded Context (dict)
    ↓ 分发到具体生成器
```

**输出上下文 schema**：

```python
{
    "domain": "alive-mood",          # 领域名称
    "version": "1.0",                # 版本
    "entities": [                     # 实体列表
        {
            "name": "MoodRecord",
            "fields": [...],
            "pk_field": "id",
            "fk_fields": ["user_id"],
        }
    ],
    "api_endpoints": [...],          # API 端点
    "date": "2026-06-28 17:30",      # 生成时间戳
    "generator_type": "code",        # 生成器类型
    "language": "spring",            # 目标语言
    "template_type": "controller",   # 模板类型
}
```

**关键接口** (`engine.py`)：

```python
class GenerationEngine:
    def run(self, generator_type: str, ...) -> list[str]:
        # 1. 加载 DomainConfig
        # 2. Pydantic 校验
        # 3. 构建渲染上下文
        # 4. 创建生成器实例
        # 5. 调用 generate()
```

### 2.3 Generator → App 契约

**输入**：渲染上下文 + Jinja2 模板。

**输出**：完整源代码文件。

**生成器注册表**：

| 生成器 | 类 | 输出目录 | 模板 |
|--------|-----|---------|------|
| RuleGenerator | `generators/rule.py` | `docs/` | `templates/*.j2` |
| PromptGenerator | `generators/prompt.py` | `docs/` | `templates/prompt/*.j2` |
| BlueprintGenerator | `generators/blueprint.py` | `docs/blueprint/` | `templates/blueprint/*.j2` |
| CodeGenerator | `generators/code.py` | `apps/` `backend/` | `templates/code/**/*.j2` |

**文件输出约定**：

```
生成器输出                   →  App 目录
templates/code/flutter/*    →  apps/mobile-flutter/lib/
templates/code/spring/*     →  backend/{module}/src/main/java/
templates/code/vue3/*       →  apps/admin-vue3/src/
```

## 3. 端到端流程示例

以"创建一个情绪记录模块"为例，展示完整链路：

### Step 1: Blueprint（设计层）

在 `blueprint/Roadmap/mvp-plan.md` 中定义实体关系（详见 ER 图）。

### Step 2: 创建领域配置

```bash
# 在 generator/config/domains/ 下创建域配置
cat > generator/config/domains/alive-mood.yaml << 'EOF'
domain: alive-mood
entities:
  - name: MoodRecord
    fields:
      - name: id
        type: uuid
        required: true
      - name: mood_score
        type: integer
        required: true
      ...
EOF
```

### Step 3: 生成文档规则

```bash
# 生成规则文档 + 代码
python -m generator --type rule      --domain mood
python -m generator --type prompt    --domain mood
python -m generator --type checklist --domain mood
```

### Step 4: 生成源代码

```bash
# 生成 Spring Boot CRUD + Flutter Service
python -m generator --type code --domain flutter --count 1
python -m generator --type code --domain spring --count 1
```

### Step 5: App 集成

```
backend/alive-mood/src/main/java/com/alive/mood/
├── controller/MoodController.java    ← 自动生成
├── service/MoodService.java          ← 自动生成
├── domain/MoodRecord.java            ← 自动生成
└── repository/MoodRepository.java    ← 自动生成
```

Flutter 端：

```
apps/mobile-flutter/lib/features/mood/
├── models/mood_record.dart           ← 自动生成
└── services/mood_service.dart        ← 自动生成
```

## 4. 契约变更流程

1. **Blueprint 变更** → 更新 `*.md` 设计文档 → 更新 `DomainConfig`
2. **DomainConfig 变更** → 调整 `models.py` Pydantic schema → 版本号变更
3. **模板变更** → 更新 `*.j2` → 重新生成
4. **生成器变更** → 新建 `generators/xxx.py` → 注册到 `_init_generators()`
5. **App 层变更** → 改手动代码 → 同步回 DomainConfig

---

> **原则**：契约向上抽象，向下收敛。每一层只依赖前一层明确定义的输出格式。
