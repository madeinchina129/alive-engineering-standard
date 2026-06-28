# 内容注入 Phase 2 — 通用规范知识库填充计划

> **战略顾问**: Prometheus  
> **创建日期**: 2026-06-28  
> **状态**: 待执行  
> **预估工作量**: ~900+ 文件新增或修改  
> （~672 knowledge + ~80 代码模板 + ~150 prompt 模板 + 修改 6 standards + 新建 1 standard）

---

## 0. 概述

### 目标
为 alive-engineering-standard 的 16 个域创建通用规范内容，使用 "还活着™" 两份设计文档（Grok 251KB + ChatGPT 22KB）作为**参考素材**确定主题范围，但内容保持完全通用。

### 确认的决策
- ✅ **全部三项**: 扩展 standards → 创建 knowledge/ → 运行 generator
- ✅ **内容完全通用**: 所有新内容为通用最佳实践，不绑定具体项目
- ✅ **扩展 standards+内容**: 先在新版 standards 中添加 doc slots，再创建 knowledge 内容
- ✅ **设计文档用途**: 作为"灵感参考"确定覆盖哪些主题（而非直接复制内容）

### 目标文件数计算

| 域 | 目标(文件) | 当前(knowledge) | 需新增 | 需 doc slots | 当前 doc slots | 需新增 slots |
|----|-----------|----------------|--------|-------------|---------------|------------|
| Project | 20 | 0 (无standard) | 20 | ~4 | 0 | +4 (新建) |
| Product | 40 | 0 | 40 | ~7 | 5 | +2 |
| UI | 50 | 0 | 50 | ~9 | 5 | +4 |
| Flutter | 80 | 30 | 50 | ~14 | 5 | +9 |
| Vue3 | 70 | 12 | 58 | ~12 | 2 | +10 |
| SpringBoot | 100 | 24 | 76 | ~17 | 4 | +13 |
| Database | 40 | 0 | 40 | ~7 | 5 | +2 |
| AI | 50 | 0 | 50 | ~9 | 5 | +4 |
| API | 30 | 0 | 30 | 5 | 5 | 0 |
| Test | 30 | 0 | 30 | 5 | 6 | 0 |
| Deploy | 30 | 0 | 30 | 5 | 6 | 0 |
| Template | 100+ | 21 (templates/code/) | 80+ | N/A | N/A | 代码模板 |
| Prompt | 150+ | 0 | 150+ | N/A | N/A | 独立 Prompt |
| Checklist | 40 | 0 | 40 | ~7 | 4 | +3 |
| Business | 60 | 0 | 60 | ~10 | 4 | +6 |
| Context | 10+ | 0 | 10+ | ~2 | 4 | 0 |

**总计新增**: ~672 knowledge 文件（16域） + ~80+ 代码模板 + ~150+ prompt 模板 + ~7 standards 修改/新建

> 计算公式: 每 doc slot × 6 文件（overview.md + rule.md + example.* + faq.md + checklist.md + prompt.md）
> 非代码域（product/ui/api/database/ai/test/deploy/business/checklist/context/template/prompt/project）从 0 开始
> 技术域（flutter/vue3/springboot）已有部分内容，补充到目标数

### 关于未列出的域
以下 8 个域存在于 `domain.yaml` 但用户未列出，**本次不处理**（保持空白）：
`analytics`, `capability`, `compliance`, `event`, `operation`, `performance`, `security`, `workflow`

### 关于 template 与 prompt 标准
- `standards/template.yaml` 定义了 3 个 doc slots（模板编写/文档模板/版本管理）——这些属于**标准文档**，与 `templates/code/` 中的**代码模板文件**是两回事。两者都需要生成。
- `standards/prompt.yaml` 定义了 3 个 doc slots（结构标准/场景分类/测试验证）——这些属于**标准文档**，与 `prompts/` 中的**独立 prompt 模板**是两回事。两者都需要生成。

---

### 注意：现有基础设施确认
- ✅ `generator/config/domain.yaml` 已包含全部 25 个域，包括 `project`
- ✅ `mkdocs.yml` 已有 Project 导航项（10 个条目）
- ❌ `standards/project.yaml` 不存在（需新建）
- ✅ 其余 15 个域的 standards 均存在
- 现有 mkdocs.yml LSP 错误（YAML tag 解析）和 generator 导入错误是**预先存在的**，不影响功能

---

## 1. 实现策略

由于 subagent 不可用（缺少 API 密钥），采用 **Python 脚本批量生成** 策略。

### 核心思路
1. **扩展 standards**: 直接编辑 6 个 YAML 文件 + 新建 1 个
2. **批量生成 knowledge**: Python 脚本读取 standards → 生成 6 文件/doc（overview.md, rule.md, example.*, faq.md, checklist.md, prompt.md）
3. **批量生成 templates**: Python 脚本为 7 种语言生成代码模板
4. **批量生成 prompts**: Python 脚本生成独立 prompt 模板文件
5. **运行 generator**: 现有 engine.py 读取 knowledge/ → 输出 docs/

### 内容来源
- 两份设计文档 → 提取关键主题列表（需要覆盖哪些主题方向）
- 通用最佳实践 → 通过 Python 脚本中的内容字典直接输出（我们的知识深度足够）
- 对于 flutter/vue3/springboot 等技术的通用规范 → 基于现有知识积累

---

## 2. 详细步骤

### Phase A: 扩展 Standards 定义

#### A1: 新建 standards/project.yaml
创建 4 个 doc slots:
| id | title | knowledge_dir |
|----|-------|-------------|
| project.structure | 项目结构规范 | project/structure/ |
| project.naming | 命名规范与目录约定 | project/naming/ |
| project.workflow | 开发工作流规范 | project/workflow/ |
| project.quality | 代码质量管理 | project/quality/ |

#### A2: 修改 standards/product.yaml（当前5→7 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| product.design_review | 设计评审流程 | product/design-review/ |
| product.goal_metric | 产品目标与指标定义 | product/goal-metric/ |

#### A3: 修改 standards/ui.yaml（当前5→9 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| ui.motion | 动效设计规范 | ui/motion/ |
| ui.layout | 布局系统规范 | ui/layout/ |
| ui.design_system | 设计系统管理 | ui/design-system/ |
| ui.accessibility_ext | 无障碍扩展实践 | ui/accessibility-ext/ |

#### A4: 修改 standards/flutter.yaml（当前5→14 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| flutter.project_structure | 项目结构规范 | flutter/project-structure/ |
| flutter.hive | Hive 本地存储规范 | flutter/hive/ |
| flutter.flame | Flame 游戏引擎规范 | flutter/flame/ |
| flutter.testing | Flutter 测试规范 | flutter/testing/ |
| flutter.localization | 国际化规范 | flutter/localization/ |
| flutter.widget | Widget 组件规范 | flutter/widget/ |
| flutter.animation | 动画规范 | flutter/animation/ |
| flutter.theming | 主题化规范 | flutter/theming/ |
| flutter.fastfile | 项目配置规范 | flutter/fastfile/ |

#### A5: 修改 standards/vue3.yaml（当前2→12 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| vue3.project_structure | 项目结构规范 | vue3/project-structure/ |
| vue3.routing | 路由管理规范 | vue3/routing/ |
| vue3.state_management | 状态管理规范 | vue3/state-management/ |
| vue3.components | 组件设计规范 | vue3/components/ |
| vue3.composables | Composables 规范 | vue3/composables/ |
| vue3.testing | 测试规范 | vue3/testing/ |
| vue3.performance | 性能优化规范 | vue3/performance/ |
| vue3.i18n | 国际化规范 | vue3/i18n/ |
| vue3.styling | 样式管理规范 | vue3/styling/ |
| vue3.build_deploy | 构建与部署规范 | vue3/build-deploy/ |

#### A6: 修改 standards/springboot.yaml（当前4→17 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| springboot.project_structure | 项目结构规范 | springboot/project-structure/ |
| springboot.config | 配置管理规范 | springboot/config/ |
| springboot.security | 安全规范 | springboot/security/ |
| springboot.testing | 测试规范 | springboot/testing/ |
| springboot.caching | 缓存策略规范 | springboot/caching/ |
| springboot.async | 异步处理规范 | springboot/async/ |
| springboot.logging | 日志规范 | springboot/logging/ |
| springboot.monitoring | 监控与指标规范 | springboot/monitoring/ |
| springboot.validation | 校验规范 | springboot/validation/ |
| springboot.migration | 数据库迁移规范 | springboot/migration/ |
| springboot.openapi | OpenAPI 文档规范 | springboot/openapi/ |
| springboot.actuator | Actuator 规范 | springboot/actuator/ |
| springboot.cicd | CI/CD 规范 | springboot/cicd/ |

#### A7: 修改 standards/database.yaml（当前5→7 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| database.backup | 备份与恢复策略 | database/backup/ |
| database.sharding | 分库分表规范 | database/sharding/ |

#### A8: 修改 standards/ai.yaml（当前5→9 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| ai.model_selection | 模型选型规范 | ai/model-selection/ |
| ai.evaluation | AI 评估规范 | ai/evaluation/ |
| ai.fine_tuning | 微调实践规范 | ai/fine-tuning/ |
| ai.cost_optimization | AI 成本优化 | ai/cost-optimization/ |

#### A9: 修改 standards/checklist.yaml（当前4→7 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| checklist.performance | 性能检查清单 | checklist/performance/ |
| checklist.accessibility | 无障碍检查清单 | checklist/accessibility/ |
| checklist.localization | 国际化检查清单 | checklist/localization/ |

#### A10: 修改 standards/business.yaml（当前4→10 doc slots）
新增:
| id | title | knowledge_dir |
|----|-------|-------------|
| business.domain_events | 领域事件规范 | business/domain-events/ |
| business.state_machine | 状态机规范 | business/state-machine/ |
| business.reporting | 报表逻辑规范 | business/reporting/ |
| business.audit | 审计日志规范 | business/audit/ |
| business.retry | 重试策略规范 | business/retry/ |
| business.rule_engine | 规则引擎规范 | business/rule-engine/ |

> **注意:** `standards/template.yaml`（3 doc slots）和 `standards/prompt.yaml`（3 doc slots）**不扩展**。
> 它们的 knowledge/ 内容由 `generate_knowledge.py` 脚本一并生成。

---

### Phase B: 创建知识库生成脚本

#### B1: 创建 scripts/generate_knowledge.py
一个 Python 脚本，功能：
1. 读取所有 standards/*.yaml（读 domain.key, documents[].knowledge_dir）
2. 对于每个 doc slot，检查 knowledge/{dir}/ 是否存在
3. 如果不存在，创建目录并生成 6 个标准文件
4. 支持 `--dry-run` 预览
5. 支持 `--domain DOMAIN` 只处理特定域
6. 支持 `--single DIR` 只处理特定 doc

##### 每个 doc 的 6 个文件模板:

**overview.md**: 概述文档
```markdown
# {title}

## 概述
[2-3段通用概述文字]

## 核心原则
1. 原则1
2. 原则2
3. 原则3

## 适用范围
[适用范围说明]
```

**rule.md**: 规则文档
```markdown
# {title} — 规则

## 规则列表
| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| {rule1} | ... | P0 | 是 |

## 详细说明
[每条规则的详细说明]
```

**example.{ext}**: 示例文件（扩展名由域类型决定）

完整语言映射表:
```python
# 代码域 → 语言扩展
LANGUAGE_EXT = {
    'flutter': 'dart',
    'vue3': 'vue',       # 同时生成 .ts 版本
    'springboot': 'java',
    'go': 'go',
    'react': 'tsx',
    'rust': 'rs',
    'kotlin': 'kt',
    'swift': 'swift',
}

# 非代码域 → 均为 .md（文档型示例）
DOC_EXT = {
    'project': 'md',
    'product': 'md',
    'domain': 'md',
    'capability': 'md',
    'business': 'md',
    'workflow': 'md',
    'event': 'md',
    'ui': 'md',          # 含代码片段在 markdown 代码块中
    'api': 'yaml',       # OpenAPI 示例
    'database': 'sql',   # SQL 示例
    'ai': 'md',
    'security': 'md',
    'test': 'md',
    'deploy': 'yaml',    # K8s/Docker 示例
    'template': 'j2',
    'prompt': 'md',
    'checklist': 'md',
    'context': 'md',
    'operation': 'md',
    'analytics': 'md',
    'performance': 'md',
    'compliance': 'md',
}
```

**faq.md**: 常见问题
```markdown
# {title} — FAQ

## Q1: [问题]?
A: [回答]

## Q2: ...
```

**checklist.md**: 检查清单
```markdown
# {title} — 检查清单

- [ ] 检查项1
- [ ] 检查项2
```

**prompt.md**: AI Prompt
```markdown
# {title} — AI Prompt

## System Prompt
[系统提示词]

## User Prompt 模板
[用户提示词模板]

## 示例
[示例]
```

##### 内容生成策略:
脚本内部按域分类包含内容字典，每个 doc slot 预定义高质量中文内容（约 300-800 字/文件）。

```python
# 内容字典结构示例
KNOWLEDGE_CONTENT = {
    'product/prd': {  # knowledge_dir 路径
        'overview': """
# PRD 标准模板

## 概述
产品需求文档（PRD）是连接产品、设计、开发和测试的核心文档...

## 核心原则
1. **用户价值导向**: 每个需求必须明确说明为用户解决了什么问题
2. **可衡量**: 每个需求必须有关联的成功指标
3. **无二义性**: 使用精确语言，避免"优化""提升"等模糊词汇

## 适用范围
适用于所有产品功能的需求定义阶段
""",
        'rules': [
            ('PRD-001', '每个需求必须有明确的用户故事', 'P0', '是'),
            ('PRD-002', '必须包含验收标准（AC）', 'P0', '是'),
            ...
        ],
        'faq': [
            ('PRD 应该多长?', '建议 2-5 页，聚焦核心功能描述'),
            ...
        ],
        'checklist': [
            '用户故事格式正确（As a... I want... So that...）',
            ...
        ],
        'prompt': '你是一个资深产品经理...',
        'example': '# 示例：用户故事\n\n## As a 注册用户\nI want 重置密码\nSo that 我能在忘记密码时恢复账号...',
    },
    ...
}
```

使用 Python 多行字符串保持内容可读性。所有内容包含 5 个部分：
- **overview.md**: 概述 + 核心原则 + 适用范围（300-500 字）
- **rule.md**: 规则表 + 详细说明（5-15 条规则）
- **faq.md**: 5-10 个常见问题
- **checklist.md**: 10-20 个检查项
- **prompt.md**: AI 系统提示词 + 用户模板
- **example.***: 2-3 个完整示例

脚本需处理 UTF-8 编码（YAML 文件含中文）。

##### 语言映射表:
```python
LANGUAGE_EXT = {
    'flutter': 'dart',
    'vue3': 'vue',  # 也生成 .ts
    'springboot': 'java',
    'go': 'go',
    'react': 'tsx',
    'rust': 'rs',
    'kotlin': 'kt',
    'swift': 'swift',
    'database': 'sql',
    'api': 'yaml',
}
```

#### B2: 创建 scripts/generate_prompts.py
> **⚠️ 注意**: "Prompt 150+" 目标指**独立 prompt 模板文件**，不是 knowledge/ 中的 prompt.md。
> 这些文件存储在独立的 `prompts/` 目录下，与现有 standards/prompt.yaml 无关。
> 
> 生成位置: `prompts/{category}/{name}.md`（新建目录，非 knowledge/ 下）

生成 150+ 独立 prompt 模板文件：
- 位置: `prompts/{category}/{name}.md`
- 分类体系（从设计文档提炼的通用场景）:
  1. `prompt/code-review/` — 代码审查 Prompt
  2. `prompt/architecture/` — 架构设计 Prompt
  3. `prompt/testing/` — 测试生成 Prompt
  4. `prompt/documentation/` — 文档生成 Prompt
  5. `prompt/debugging/` — 调试辅助 Prompt
  6. `prompt/refactoring/` — 重构建议 Prompt
  7. `prompt/security/` — 安全审查 Prompt
  8. `prompt/ui-design/` — UI 设计 Prompt
  9. `prompt/api-design/` — API 设计 Prompt
  10. `prompt/database/` — 数据库设计 Prompt
  11. `prompt/business/` — 业务分析 Prompt
  12. `prompt/interview/` — 面试题 Prompt
  13. `prompt/learning/` — 学习辅导 Prompt
  14. `prompt/code-gen/` — 代码生成 Prompt
  15. `prompt/meeting/` — 会议助手 Prompt

每个分类 10 个 prompt，共 150 个。

##### 输出格式:
```
prompts/{category}/01-overview.md → 分类概述
prompts/{category}/02-{name}.md → 具体 prompt
prompts/{category}/03-{name}.md → 具体 prompt
...
prompts/{category}/10-{name}.md → 具体 prompt
```

##### 每个 prompt 文件结构:
```markdown
# {标题}

## 目标
[该 prompt 解决什么问题]

## System Prompt
```
[系统提示词内容]
```

## User Prompt
```
[用户提示词模板]
```

## 输出格式
[期望的输出格式说明]

## 变量说明
- `{variable1}`: [说明]
- `{variable2}`: [说明]

## 使用场景
[什么场景下使用这个 prompt]
```

#### B3: 创建 scripts/generate_templates.py
> **⚠️ 注意 — 两个不同的事物:**
> 1. `standards/template.yaml` → 定义 3 个知识文档（模板编写规范/文档模板标准/版本管理）
>    → 由 `generate_knowledge.py` 生成到 `knowledge/template/{doc}/`
> 2. `templates/code/` → 代码模板文件（.j2），用于 code generation
>    → 由 `generate_templates.py` 生成此处
> 
> **"Template 100+" 目标指第 2 项（代码模板 .j2 文件）**。第 1 项也会生成但 count 计入 template domain 的 knowledge/ 文件数。
> 
> 当前已有 21 个 .j2 文件，需新增约 80 个达到 100+。

生成 100+ 代码模板到 `templates/code/{lang}/{name}.j2`：
为 7 种语言各生成约 15 个模板：
- flutter/: 15 .j2 (widget, model, provider, service, repository, etc.)
- spring/: 15 .j2 (controller, service, repository, dto, entity, etc.)
- vue3/: 15 .j2 (component, composable, store, page, etc.)
- react/: 15 .j2 (component, hook, context, service, etc.)
- go/: 15 .j2 (handler, service, model, repository, etc.)
- rust/: 15 .j2 (module, handler, model, error, etc.)
- kotlin/: 15 .j2 (controller, service, repository, model, etc.)

---

### Phase C: 运行生成脚本

#### C1: 先生成知识库内容
```bash
python scripts/generate_knowledge.py --dry-run    # 预览
python scripts/generate_knowledge.py              # 执行
```

#### C2: 生成代码模板
```bash
python scripts/generate_templates.py --dry-run
python scripts/generate_templates.py
# 模板输出到 templates/code/{lang}/
```

#### C3: 生成 Prompt 模板
```bash
python scripts/generate_prompts.py --dry-run
python scripts/generate_prompts.py
# 输出到 prompts/{category}/{name}.md
```

#### C4: 验证生成结果
```bash
# 统计各域文件数
python -c "
import os, yaml
from pathlib import Path

for domain_dir in sorted(Path('knowledge').iterdir()):
    if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
        files = list(domain_dir.rglob('*'))
        print(f'{domain_dir.name}: {len(files)} files')
"
```

---

### Phase D: 运行 Generator 输出文档

#### D1: 生成所有文档
```bash
# 生成规则文档 (KnowledgeEngine)
python -m generator.engine --type rule --all

# 生成 prompt 文档（如果 prompt standard 扩展了）
python -m generator.engine --type prompt --all

# 生成 checklist
python -m generator.engine --type checklist --all

# 生成所有类型
python -m generator.engine --type all --all
```

#### D2: 更新 mkdocs.yml
由于 project 域需要 4 个新 doc slots，而现有 mkdocs.yml 已有 10 个 Project 条目（由原有 generator 配置生成）。
如果 standards/project.yaml 的 filename/index 与现有 mkdocs.yml 条目不匹配，需要同步更新 mkdocs.yml。

**操作**: 运行 generator 后，检查 `docs/00_Project/` 下的实际文件名是否与 mkdocs.yml 的 `00_Project/` 条目对应。
如果不符，手动更新 mkdocs.yml 中的 nav 条目。

对其他域（product/ui/flutter/vue3/springboot 等），如果新 doc slots 的 filename/index 与现有 mkdocs.yml 的 nav 条目不冲突，则 generator 会自动处理。

#### D3: 总体验证
```bash
python -m generator.engine --type all --all --dry-run | findstr /c:"Total"
```

---

### Phase E: Git 提交

#### E1: 分批次原子提交
```bash
# Commit 1: Standards 扩展
git add standards/
git commit -m "feat(standards): extend 7 standards with new doc slots

- Add project.yaml (new)
- Extend product (5→7), UI (5→9), flutter (5→14)
- Extend vue3 (2→12), springboot (4→17), database (5→7)
- Extend ai (5→9), checklist (4→7), business (4→10)"

# Commit 2: Knowledge 生成脚本
git add scripts/generate_knowledge.py scripts/generate_prompts.py scripts/generate_templates.py
git commit -m "feat(scripts): add knowledge/prompt/template generators"

# Commit 3: Knowledge 内容
git add knowledge/
git commit -m "feat(knowledge): bulk knowledge content for 16 domains"

# Commit 4: Code 模板
git add templates/code/
git commit -m "feat(templates): expand code templates to 100+"

# Commit 5: Prompt 模板
git add prompts/
git commit -m "feat(prompts): 150+ AI prompt templates in 15 categories"

# Commit 6: Docs 输出
git add docs/
git commit -m "feat(docs): regenerate all docs with new knowledge content"

# Commit 7: Plan
git add .sisyphus/
git commit -m "docs(plan): content injection phase 2 plan"
```

---

## 3. QA 验证清单

### Phase A 验证
- [ ] `standards/project.yaml` 存在，包含 4+ doc slots
- [ ] `standards/product.yaml` 有 7+ doc slots
- [ ] `standards/ui.yaml` 有 9+ doc slots
- [ ] `standards/flutter.yaml` 有 14+ doc slots
- [ ] `standards/vue3.yaml` 有 12+ doc slots
- [ ] `standards/springboot.yaml` 有 17+ doc slots
- [ ] `standards/database.yaml` 有 7+ doc slots
- [ ] `standards/ai.yaml` 有 9+ doc slots
- [ ] `standards/checklist.yaml` 有 7+ doc slots
- [ ] `standards/business.yaml` 有 10+ doc slots
- [ ] 所有 standards YAML 语法正确（`python -c "import yaml; yaml.safe_load(open('standards/...'))"`）

### Phase B-C 验证
- [ ] `scripts/generate_knowledge.py` 可运行
- [ ] `scripts/generate_prompts.py` 可运行
- [ ] `scripts/generate_templates.py` 可运行
- [ ] `generate_knowledge.py --dry-run` 输出正确
- [ ] 所有 knowledge 文件生成，每 doc 6 文件
- [ ] 不存在空文件或残次文件（`find . -size 0` 返回空）

### Phase D 验证
- [ ] `python -m generator.engine --type rule --all` 无报错
- [ ] `python -m generator.engine --type all --all --dry-run` 文件数达标
- [ ] 各域文件数 ≥ 目标数

### 文件数验证脚本
```python
targets = {
    'project': 20, 'product': 40, 'ui': 50,
    'flutter': 80, 'vue3': 70, 'springboot': 100,
    'database': 40, 'ai': 50, 'api': 30,
    'test': 30, 'deploy': 30,
    'prompt': 150, 'checklist': 40,
    'business': 60, 'context': 10,
}
# 知识库文件验证
from pathlib import Path
for domain_key, expected in targets.items():
    d = Path(f'knowledge/{domain_key}')
    if d.exists():
        count = len(list(d.rglob('*')))
    else:
        count = 0
    status = 'PASS' if count >= expected else f'FAIL (got {count}, need {expected})'
    print(f'{domain_key}: {count} files {status}')

# 模板验证
template_count = len(list(Path('templates/code').rglob('*.j2')))
print(f'\ntemplates/code/ .j2 files: {template_count} (need 100+)')

# Prompt 验证
prompt_count = len(list(Path('prompts').rglob('*.md'))) if Path('prompts').exists() else 0
print(f'prompts/ files: {prompt_count} (need 150+)')
```

---

## 4. 文件映射表 — 设计文档内容到通用规范

以下是从两份设计文档中提炼的关键主题，映射到通用规范域的创作依据：

| 域 | 设计文档中的参考内容 | 转化为通用规范 |
|----|---------------------|--------------|
| **Product** | 产品定位、用户画像、核心功能体系、PMF | 通用 PRD 模板、用户故事、验收标准、优先级方法 |
| **UI** | 暗色主题(#121212)、5色系统、9:16竖版、Figma高保真 | 设计令牌、组件库、响应式设计、设计系统管理 |
| **Flutter** | Feature-First架构、Riverpod、go_router、Hive、Flame | Clean Architecture、状态管理、本地存储、游戏引擎规范 |
| **Vue3** | （设计文档无Vue3内容，从零创建） | 组合式API、Pinia、路由、组件规范 |
| **SpringBoot** | （设计文档无后端，从零创建） | 分层架构、Data JPA、REST API、安全、缓存 |
| **AI** | 通义千问/豆包调用、毒鸡汤生成、Prompt模板 | LLM集成、Prompt工程、RAG、安全、评估 |
| **Business** | 打卡-称号-毒鸡汤业务流、商业模式 | 业务规则模式、状态机、领域事件 |
| **Database** | Hive本地、Supabase云同步 | 命名规范、迁移、索引、SQL审查 |

---

## 5. 分工与优先级

### P0 — 必须先完成
这些域需要**先扩展 standards 再创建内容**，且内容最丰富（3 个技术域 + 3 个核心非技术域）：
1. 🔴 **扩展 7 个 standards**（Phase A）
2. 🔴 **创建 generate_knowledge.py** 脚本并运行（Phase B1 → C1）
3. 🔴 **生成 6 个核心域**知识内容：flutter（+9 slots）、vue3（+10）、springboot（+13）、product（+2）、ui（+4）、ai（+4）
4. 🔴 **运行 generator 输出 docs**

### P1 — 重要
这些域 standards 已有足够 slots，只需创建 knowledge 内容（无需扩展 standards）：
1. 🟡 生成 **api（5 slots）、test（6）、deploy（6）、context（4）** 知识内容
2. 🟡 创建 **generate_prompts.py** 生成 150+ prompt 文件（Phase B2 → C3）
3. 🟡 创建 **generate_templates.py** 生成 100+ 代码模板（Phase B3 → C2）

### P2 — 标准优先级
这些域需同时**扩展 standards 并创建内容**，但数量较少：
1. 🟢 **database**（+2 slots）、**checklist**（+3）、**business**（+6）、**project**（新建 4 slots）
2. 🟢 **template**（3 slots）和 **prompt**（3 slots）标准知识内容

### P2 - 收尾（Phase E）
1. 🟢 Git 提交
2. 🟢 最终验证

---

## 6. 关键决策记录

| 决策 | 选择 | 原因 |
|------|------|------|
| 内容风格 | 完全通用 | 用户明确要求 |
| Standards 扩展策略 | 新增 doc slots | 用户明确要求 |
| 生成方式 | Python 脚本 | Subagent 不可用；批量生成高效 |
| 每 doc 文件结构 | 6 文件标准化 | 与现有 flutter/riverpod 保持一致 |
| 设计文档用途 | 主题参考 | 不直接复制，提炼通用主题 |
| 文件数目标 | 按用户指定 | 每个 doc 6 文件 ≈ 用户目标 ÷ 6 |

---

## 7. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 生成脚本内容质量不足 | 中 | 高 | 使用高质量内容字典，每个 doc 预写 300-800 字 |
| 文件数不达标 | 低 | 中 | QA 脚本自动统计并报告差距 |
| YAML 语法错误 | 低 | 高 | 运行 `yaml.safe_load()` 验证所有标准 |
| 生成器 engine.py 不兼容新 standards | 中 | 高 | 先用 `--dry-run` 验证 |
| Python 依赖缺失 | 低 | 低 | `pip install pyyaml jinja2` |

---

## 8. 最终验证标准

**所有任务完成后，必须满足：**
1. 16 个域的 `knowledge/{domain}/` 文件夹存在，文件数 ≥ 目标
2. `templates/code/` 中 .j2 文件数 ≥ 100
3. `prompts/` 下 .md 文件数 ≥ 150
4. `docs/` 中各域文档完整，mkdocs build 无报错
5. `git status` 干净，无未提交文件
6. 所有新 standards 文件 YAML 语法正确

---

> **下一步**: 运行 `/start-work` 开始执行
