# Massive Content Expansion Plan

## 目标
- 从当前 ~566 篇文档扩充到 930 篇
- 为 23 个非 Flutter 领域注入与 Flutter 同等规格的实质章节（每篇 500-3000 行）
- 新增 `--type template` 生成器，支持 100+ 代码模板
- 增强 CodeGenerator，从 domain.yaml 实体定义读取字段生成真实 CRUD

## 现状分析

### 文档统计
```
00_Project:    21 docs    10_Flutter:    36 docs    18_Prompt:      13 docs
01_Product:    21 docs    11_Vue3:       25 docs    19_Checklist:   17 docs  
02_Domain:     21 docs    12_SpringBoot: 29 docs    20_Context:     17 docs
03_Capability: 17 docs    13_AI:         21 docs    21_Operation:   17 docs  
04_Business:   17 docs    14_Security:   25 docs    22_Analytics:   21 docs
05_Workflow:   17 docs    15_Test:       25 docs    23_Performance: 21 docs
06_Event:      21 docs    16_Deploy:     25 docs    24_Compliance:  21 docs
07_UI:         21 docs    17_Template:   13 docs    ---
08_API:        21 docs                                   Total: ~566
09_Database:   21 docs
```

### 两个生成器系统
1. **KnowledgeEngine** (engine.py): knowledge/ + standards/ + templates/ → docs/
   - 当前 8 领域 32 文档（Flutter/SpringBoot/Vue3/React/Go/Rust/Kotlin/Swift）
   - 知识文件在 `knowledge/<domain>/<topic>/`（5 files: overview, rule, faq, checklist, prompt）
   - 元数据在 `standards/<domain>.yaml`

2. **GeneratorEngine** (cli.py): domain.yaml + Jinja2 templates → docs/
   - 24 领域 ~534 文档，通过多种生成器类型（rule/prompt/checklist/context/graph/blueprint/code）
   - domain.yaml 定义所有领域和文档（1239 行）
   - 各模板在 `generator/templates/`

### 内容质量差距
- Flutter 是黄金标准：每个 doc 有 4-8 个 sections，每个 30-150 行实质代码 + 表格 + 原则
- 多数其他领域 doc 只有标题和简短描述，缺乏实质章节内容

## 分阶段计划

---

## Phase 1: 生成器基础设施整合与增强

### 1.1 合并两个生成器系统
**问题**: KnowledgeEngine 和 GeneratorEngine 并行存在，各自独立。
**方案**: 
- 保留 KnowledgeEngine 作为核心（纯 Python，无外部依赖）
- 将 GeneratorEngine 的生成器类型（rule/prompt/checklist/context/graph/blueprint/code）迁移到 KnowledgeEngine
- domain.yaml → 映射到 knowledge/ 目录结构（待生成的知识文件清单）
- standards/*.yaml 补全所有 24 领域

**任务**: 
```
[1.1.a] 创建 standards/ 缺失标准文件
  - product.yaml, domain.yaml, capability.yaml, business.yaml, workflow.yaml
  - event.yaml, ui.yaml, api.yaml, database.yaml, ai.yaml, security.yaml
  - test.yaml, deploy.yaml, template.yaml, prompt.yaml, checklist.yaml
  - context.yaml, operation.yaml, analytics.yaml, performance.yaml
  - compliance.yaml, project.yaml
  → 每个文件从 domain.yaml 提取文档元数据
  → 预计 20 个新 standards 文件

[1.1.b] 增强 KnowledgeEngine 支持新生成器类型
  - 添加 `--type code`、`--type template`、`--type blueprint`、`--type graph`
  - engine.py 的 _jinja2_render 替换为真正的 Jinja2（条件判断完整支持）
  - 添加 `--type` flag 到 engine.py 的 argparse
  
[1.1.c] 创建 standards/domain.yaml 作为通用域配置（合并现有 domain.yaml）
```

### 1.2 新增 --type template 生成器
**任务**:
```
[1.2.a] 创建 code template 仓库布局
  templates/code/
  ├── flutter/
  │   ├── model.dart.j2        # JSON Model + fromJson/toJson
  │   ├── service.dart.j2      # API Service + CRUD
  │   ├── provider.dart.j2     # Riverpod Provider
  │   ├── screen.dart.j2       # Screen page
  │   └── widget.dart.j2       # Reusable widget
  ├── spring/
  │   ├── entity.java.j2       # JPA Entity + annotations
  │   ├── repository.java.j2   # Spring Data JPA Repository
  │   ├── service.java.j2      # Service + transactional
  │   ├── controller.java.j2   # REST Controller
  │   ├── dto.java.j2          # Request/Response DTO
  │   └── mapper.java.j2       # MapStruct mapper
  ├── vue3/
  │   ├── page.vue.j2          # Vue3 page with Composition API
  │   ├── component.vue.j2     # Vue3 component
  │   ├── composable.ts.j2     # Composable function
  │   ├── store.ts.j2          # Pinia store
  │   └── api.ts.j2            # API client
  ├── react/
  │   ├── component.tsx.j2     # React component
  │   ├── hook.ts.j2           # Custom hook
  │   ├── store.ts.j2          # Zustand store
  │   └── api.ts.j2            # API service
  ├── go/
  │   ├── handler.go.j2        # HTTP handler
  │   ├── service.go.j2        # Business service
  │   ├── repository.go.j2     # Data repository
  │   └── model.go.j2          # Data model
  ├── kotlin/
  │   ├── model.kt.j2          # Data class
  │   ├── repository.kt.j2     # Repository
  │   ├── service.kt.j2        # Service
  │   └── route.kt.j2          # Ktor route
  └── rust/
      ├── model.rs.j2          # Struct + serde
      ├── handler.rs.j2        # Axum handler
      ├── service.rs.j2        # Business logic
      └── repository.rs.j2     # Data access
```

**实体定义 schema** (entity 配置嵌入 domain.yaml 或独立 entities.yaml):
```yaml
# entities.yaml
entities:
  - name: User
    table: t_user
    fields:
      - name: id
        type: Long          # Java/Long, Dart/int, Go/int64
        pk: true
        auto: true
      - name: name
        type: String
        length: 100
        nullable: false
      - name: email
        type: String
        unique: true
      - name: status
        type: Enum
        values: [ACTIVE, INACTIVE, DELETED]
    relations:
      - type: OneToMany
        target: Order
        mappedBy: userId
```

---

## Phase 2: 23 领域内容注入（与 Flutter 同等规格）

### 2.1 内容优先级

| 优先级 | 领域 | 目标文档数 | 策略 |
|--------|------|-----------|------|
| P0 | api, database, ui, security | 各 30+ | 最重要、使用最广 |
| P1 | product, domain, business, test, deploy | 各 25+ | 核心规范 |
| P2 | event, workflow, ai, operation, analytics | 各 20+ | 重要但使用较少 |
| P3 | capability, template, prompt, checklist, context, performance, compliance | 各 15+ | 支撑性规范 |
| P4 | project, capability | 各 10+ | 基础框架 |

### 2.2 每领域知识文件规格

每个 topic 在 `knowledge/<domain>/<topic>/` 下包含 5 个文件（同 Flutter）：

```yaml
topic_name/          # 如 api/restful-api/
├── overview.md      # 概述：定义、适用范围、核心概念（200-500 字）
├── rule.md          # 细则：MUST/SHOULD/MUST NOT + 代码示例（500-1500 行）
├── faq.md           # FAQ：5-10 个 Q&A（300-800 字）
├── checklist.md     # 检查清单：15-30 个检查项（200-400 字）
└── prompt.md        # AI Prompt：给 AI 助手的上下文提示（200-500 字）
```

### 2.3 各领域 topic 计划

```
[api]
├── restful-api          # REST 设计标准
├── api-versioning       # 版本管理策略
├── error-codes          # 错误码规范
├── pagination-filter    # 分页/排序/过滤
├── openapi-spec         # OpenAPI 文档
├── graphql-api          # GraphQL 规范 (新增)
└── websocket-api        # WebSocket 规范 (新增)

[database]
├── naming-conventions   # 命名规范
├── migration-strategy   # 迁移策略
├── index-design         # 索引设计
├── sql-review           # SQL 审查
├── security             # 数据库安全
├── sharding             # 分库分表 (新增)
└── backup-recovery      # 备份恢复 (新增)

[ui/ui-ux]
├── component-library    # 组件库标准
├── design-tokens        # 设计令牌
├── responsive-design    # 响应式设计
├── accessibility        # 无障碍访问
├── theme-styling        # 主题与配色
└── design-system        # 设计系统管理 (新增)

[security]
├── owasp-top10          # OWASP 防护
├── authentication       # 认证规范
├── authorization        # 鉴权规范
├── data-encryption      # 数据加密
├── key-management       # 密钥管理
├── secure-coding        # 安全编码
└── dependency-security  # 依赖漏洞管理

[product]
├── prd-template         # PRD 模板
├── user-story           # 用户故事
├── acceptance-criteria  # 验收标准
├── design-flow          # 设计流程
└── priority-ranking     # 优先级排序

[domain/ddd]
├── bounded-context      # 限界上下文
├── ubiquitous-language  # 通用语言
├── aggregate-design     # 聚合设计
├── domain-events        # 领域事件
└── value-objects        # 值对象与实体

[test]
├── test-pyramid         # 测试金字塔
├── unit-testing         # 单元测试
├── integration-test     # 集成测试
├── e2e-testing          # E2E 测试
├── coverage-standards   # 覆盖率标准
└── test-automation      # 测试自动化

[deploy]
├── cicd-pipeline        # CI/CD 流水线
├── environment-mgmt     # 环境管理
├── rollback-strategy    # 回滚策略
├── canary-release       # 灰度发布
├── containerization     # 容器化
└── iac-standards        # IaC 规范

[其余 15 领域...]
```

**(完整 topic 清单在 Phase 2 执行中逐步精化)**

---

## Phase 3: 数量扩增 566 → 930

### 3.1 扩增策略

| 方法 | 增量 | 说明 |
|------|------|------|
| 新增 domains | +50 | 新增 5-8 个领域（如 SRE、微服务、消息队列、前端架构、iOS） |
| 新增 topics/domain | +150 | 每个 domain 增加 3-8 个新 topic |
| 子 doc/topic | +100 | 现有 topic 拆分为多篇子文档 |
| 语言变体 | +64 | Flutter/SpringBoot/Vue3/React/Go/Rust/Kotlin/Swift → 每个 8 篇 |

### 3.2 额外领域建议
```
added-domains/
├── 25_MicroService      # 微服务架构规范
├── 26_MessageQueue      # 消息队列规范
├── 27_FrontendArch      # 前端架构规范
├── 28_iOS               # iOS 原生开发规范
├── 29_QA                # QA 质量保障规范
└── 30_SRE               # SRE 运维规范
```

### 3.3 每个 document 的 section 标准化

每个 document 包含 4-8 个 sections，确保实质内容：
```
1. 概述（why + when + 适用范围）
2. 核心原则（3-5 条 MUST 原则）
3. 规范细则（MUST / SHOULD / MAY / MUST NOT）
4. 代码示例（好/坏对比）
5. 常见错误（Anti-patterns）
6. FAQ（5 个以上问答）
7. 工具与命令（对应 CLI/IDE 操作）
8. 检查清单
```

---

## Phase 4: CodeGenerator 实体驱动增强

### 4.1 entities.yaml schema

```yaml
# config/entities.yaml — 实体定义
version: "2.0"
entities:
  - name: User
    module: user
    table: t_user
    description: "系统用户"
    fields:
      - name: id
        type: Long
        pk: true
        auto: true
        description: "主键"
      - name: username
        type: String
        length: 50
        nullable: false
        unique: true
        description: "用户名"
      - name: email
        type: String
        length: 100
        nullable: false
        description: "邮箱"
      - name: password
        type: String
        length: 255
        nullable: false
        description: "加密密码"
        ignore_in_response: true  # 不在 API 响应中暴露
        ignore_in_list: true
      - name: status
        type: Enum
        enumClass: UserStatus
        values: [ACTIVE, INACTIVE, DELETED]
        default: ACTIVE
        description: "用户状态"
      - name: createdAt
        type: LocalDateTime
        auto: true
        description: "创建时间"
    indexes:
      - fields: [username]
        unique: true
      - fields: [status, createdAt]
    relations:
      - type: OneToMany
        target: Order
        mappedBy: userId
        cascade: ALL
      - type: ManyToMany
        target: Role
        through: user_role
        joinColumn: userId
        inverseJoinColumn: roleId
```

### 4.2 CodeGenerator 读取流程

```
entities.yaml → CodeGenerator → per-language generators
                                ├── flutter/    → Model, Service, Provider, Screen, Widget
                                ├── spring/     → Entity, Repository, Service, Controller, DTO, Mapper  
                                ├── vue3/       → Page, Composable, Store, API
                                ├── react/      → Component, Hook, Store, API
                                ├── go/         → Model, Handler, Service, Repository
                                ├── rust/       → Model, Handler, Service, Repository
                                └── kotlin/     → Model, Repository, Service, Route
```

### 4.3 CRUD 操作表

| 实体操作 | Flutter | Spring | Vue3 | React | Go | Rust | Kotlin |
|---------|---------|--------|------|-------|----|------|--------|
| Create | POST | @PostMapping | POST | POST | http.Post | POST | post |
| Read | GET /{id} | @GetMapping | GET | GET | http.Get | GET | get |
| Update | PUT /{id} | @PutMapping | PUT | PUT | http.Put | PUT | put |
| Delete | DELETE /{id} | @DeleteMapping | DELETE | DELETE | http.Delete | DELETE | delete |
| List | GET | @GetMapping(list) | GET | GET | http.Get(list) | GET | get(list) |

---

## 执行计划

### Phase 1: 基础设施（预计 2-3 次会话）
- [ ] 1.1.a 创建 20 个新 standards/*.yaml 文件
- [ ] 1.1.b 增强 KnowledgeEngine 支持多生成器类型
- [ ] 1.2.a Code template 仓库布局（~30 个 .j2 模板）
- [ ] 1.2.b entities.yaml schema 定义
- [ ] 1.2.c CodeGenerator 读取 entities.yaml 生成真实 CRUD
- [ ] 1.3 更新 mkdocs.yml 包含所有 24+ 领域

### Phase 2: 内容注入（预计 10-15 次会话）
- [ ] API 领域（7 topics × 5 files = 35 knowledge files）
- [ ] Database 领域（7 topics × 5 files = 35 knowledge files）
- [ ] UI/UX 领域（6 topics × 5 files = 30 knowledge files）
- [ ] Security 领域（7 topics × 5 files = 35 knowledge files）
- [ ] Product 领域（5 topics × 5 files = 25 knowledge files）
- [ ] Domain/DDD 领域（5 topics × 5 files = 25 knowledge files）
- [ ] Test 领域（6 topics × 5 files = 30 knowledge files）
- [ ] Deploy 领域（6 topics × 5 files = 30 knowledge files）
- [ ] Event 领域（5 topics × 5 files = 25 knowledge files）
- [ ] Workflow 领域（4 topics × 5 files = 20 knowledge files）
- [ ] AI 领域（5 topics × 5 files = 25 knowledge files）
- [ ] Operation 领域（4 topics × 5 files = 20 knowledge files）
- [ ] Analytics 领域（5 topics × 5 files = 25 knowledge files）
- [ ] Security 领域（7 topics × 5 files = 35 knowledge files）
- [ ] 其他 9 领域（3-4 topics × 5 files = 15-20 files each）

### Phase 3: 数量扩增 566 → 930（分步执行）
- [ ] 3.1 新增 5-8 个额外领域
- [ ] 3.2 现有 domain 增加 3-8 个新 topic
- [ ] 3.3 子文档拆分
- [ ] 3.4 语言变体文档

### Phase 4: CodeGenerator 增强
- [ ] 4.1 entities.yaml 实体定义完成（20+ 实体）
- [ ] 4.2 CodeGenerator refactor（读取 entities.yaml）
- [ ] 4.3 每语言 5 个模板（~35 个 .j2 模板文件）
- [ ] 4.4 集成测试

---

## 关键决策

| 决策 | 选项 | 推荐 |
|------|------|------|
| 生成器合并 | 保留 KnowledgeEngine 还是 GeneratorEngine? | 保留 KnowledgeEngine（纯 Python, 0 依赖），移植 GeneratorEngine 功能 |
| Jinja2 依赖 | 是否引入 Jinja2? | 是 — KnowledgeEngine 使用纯 Python 模板引擎太受限，引入 Jinja2 |
| 实体定义位置 | 新文件 entities.yaml 还是嵌入 domain.yaml? | 独立 entities.yaml，保持关注点分离 |
| 代码模板目录 | generator/templates/code/ 还是 templates/code/? | templates/code/（与已有 rule.md.j2 同级） |
| content 注入顺序 | P0→P4 还是按领域分组? | 按领域分组 + P0 优先 |

## 当前状态

| Phase | 完成度 | 备注 |
|-------|--------|------|
| Phase 1 | 0% | 待开始 |
| Phase 2 | 0% | 待开始 |
| Phase 3 | 0% | 待开始 |
| Phase 4 | 0% | 待开始 |
