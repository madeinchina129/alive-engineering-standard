# Phase 1 实施指南 — 生成器基础设施

## 已完成：Phase 1.1 ✅
**21 个 standards/*.yaml** 已从 domain.yaml 自动生成：
`product`, `domain`, `capability`, `business`, `workflow`, `event`, `ui`, `api`, `database`,
`ai`, `security`, `test`, `deploy`, `template`, `prompt`, `checklist`, `context`,
`operation`, `analytics`, `performance`, `compliance`

---

## 待实施：Phase 1.2 — 增强 KnowledgeEngine

### 目标
engine.py 添加 Jinja2 支持 + 多生成器类型 + `--type`/`--format` 参数

### 具体修改

**engine.py 第 1-20 行**：添加 Jinja2 导入和 GENERATORS 注册表

```python
try:
    from jinja2 import Environment, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

# 生成器类型注册表
GENERATOR_TYPES = {
    'rule': '规则文档',
    'prompt': 'AI Prompt 文档',
    'checklist': '检查清单文档',
    'template': '代码模板',
    'code': 'CRUD 代码生成',
    'blueprint': '架构蓝图',
    'graph': '依赖关系图',
}
```

**engine.py 第 509-530 行（main 函数）**：添加 `--type` 和 `--format` 参数

```python
parser.add_argument("--type", "-t", choices=list(GENERATOR_TYPES.keys()) + ["all"],
                    default="rule", help="生成器类型")
parser.add_argument("--format", "-f", choices=["md", "json"],
                    default="md", help="输出格式")
```

**engine.py**：添加 GeneratorRegistry 类

```python
class GeneratorRegistry:
    """生成器注册表 — 根据类型分派到不同生成逻辑"""
    
    def __init__(self, engine: 'KnowledgeEngine'):
        self.engine = engine
        self._generators = {
            'rule': self._gen_rule,
            'prompt': self._gen_prompt,
            'checklist': self._gen_checklist,
            'template': self._gen_template,
            'code': self._gen_code,
            'blueprint': self._gen_blueprint,
            'graph': self._gen_graph,
        }
    
    def generate(self, gen_type: str, domain_key: Optional[str] = None,
                 all_flag: bool = False, dry_run: bool = False,
                 output_format: str = "md") -> list[str]:
        handler = self._generators.get(gen_type)
        if not handler:
            print(f"[ERROR] Unknown generator type: {gen_type}")
            return []
        return handler(domain_key, all_flag, dry_run, output_format)
    
    def _gen_rule(self, domain_key, all_flag, dry_run, fmt):
        """规则文档 — 现有 KnowledgeEngine 逻辑"""
        if all_flag:
            domains = list_standards()
            total = []
            for dk in domains:
                total.extend(self.engine.generate_domain(dk, dry_run=dry_run))
            return total
        if domain_key:
            return self.engine.generate_domain(domain_key, dry_run=dry_run)
        return []
    
    def _gen_prompt(self, domain_key, all_flag, dry_run, fmt):
        """提取 knowledge/ 中的 prompt.md 文件"""
        return self._extract_section('prompt', domain_key, all_flag, dry_run, fmt)
    
    def _gen_checklist(self, domain_key, all_flag, dry_run, fmt):
        """提取 knowledge/ 中的 checklist.md 文件"""
        return self._extract_section('checklist', domain_key, all_flag, dry_run, fmt)
    
    def _extract_section(self, section_type, domain_key, all_flag, dry_run, fmt):
        """提取指定 section 类型"""
        domains = [domain_key] if domain_key else list_standards()
        results = []
        for dk in domains:
            std = load_standards(dk)
            if not std: continue
            for doc in std.get('documents', []):
                kdir = doc.get('knowledge_dir', '')
                if not kdir: continue
                sections = read_knowledge_dir(kdir)
                for sec in sections:
                    if sec['type'] == section_type:
                        if fmt == 'json':
                            print(json.dumps({'domain': dk, 'title': doc['title'],
                                              'content': sec['content']}, ensure_ascii=False))
                        results.append(f"{dk}/{doc['title']}")
        return results
    
    def _gen_template(self, domain_key, all_flag, dry_run, fmt):
        """代码模板生成器 — 读取 templates/code/{lang}/*.j2"""
        langs = ['flutter', 'spring', 'vue3', 'react', 'go', 'rust', 'kotlin']
        if domain_key and domain_key in langs:
            langs = [domain_key]
        results = []
        for lang in langs:
            tmpl_dir = TEMPLATES_DIR / 'code' / lang
            if not tmpl_dir.exists():
                continue
            for tmpl_file in tmpl_dir.glob('*.j2'):
                output_name = tmpl_file.stem.replace('.j2', '')
                section = tmpl_file.stem.split('.')[0]  # model, service, etc.
                ctx = _build_template_context(lang, section)
                rendered = _render_jinja(tmpl_file.read_text(encoding='utf-8'), ctx)
                if not dry_run:
                    out_dir = DOCS_DIR / f'templates/{lang}'
                    out_dir.mkdir(parents=True, exist_ok=True)
                    (out_dir / output_name).write_text(rendered, encoding='utf-8')
                results.append(f"{lang}/{output_name}")
        return results
    
    def _gen_code(self, domain_key, all_flag, dry_run, fmt):
        """CRUD 代码生成 — 从 entities.yaml 读取实体定义"""
        entities_path = CONFIG_DIR / 'entities.yaml'
        entities = []
        if entities_path.exists():
            with open(entities_path, encoding='utf-8') as f:
                entities = yaml.safe_load(f).get('entities', [])
        if not entities:
            entities = _default_entities()
        langs = ['flutter', 'spring']
        if domain_key and domain_key in langs:
            langs = [domain_key]
        results = []
        for entity in entities:
            for lang in langs:
                result = _gen_crud_for_lang(entity, lang, dry_run)
                if result:
                    results.extend(result)
        return results
    
    def _gen_blueprint(self, domain_key, all_flag, dry_run, fmt):
        """架构蓝图生成"""
        return self._gen_rule(domain_key, all_flag, dry_run, fmt)
    
    def _gen_graph(self, domain_key, all_flag, dry_run, fmt):
        """依赖关系图 — 从 standards/ 生成 domain 间关系"""
        if fmt == 'json':
            graph = {'nodes': [], 'edges': []}
            for f in STANDARDS_DIR.glob('*.yaml'):
                std = yaml.safe_load(f.read_text(encoding='utf-8'))
                if std and 'domain' in std:
                    graph['nodes'].append({'id': std['domain']['key'], 'name': std['domain']['name']})
            print(json.dumps(graph, ensure_ascii=False))
        return ['graph generated']


def _build_template_context(lang: str, section: str) -> dict:
    """构建代码模板上下文"""
    ctx = {'date': date.today().isoformat(), 'lang': lang, 'section': section}
    if section == 'model':
        ctx.update({'class_name': 'ExampleModel', 'fields': [
            {'name': 'id', 'type': 'String'}, {'name': 'name', 'type': 'String'}
        ]})
    elif section == 'service':
        ctx.update({'class_name': 'ExampleService', 'model_name': 'ExampleModel'})
    elif section == 'controller':
        ctx.update({'class_name': 'ExampleController', 'endpoint': 'examples'})
    elif section == 'repository':
        ctx.update({'class_name': 'ExampleRepository', 'entity_name': 'ExampleEntity'})
    return ctx


def _render_jinja(template_str: str, context: dict) -> str:
    """渲染 Jinja2 模板（可选）"""
    if HAS_JINJA2:
        env = Environment()
        tmpl = env.from_string(template_str)
        return tmpl.render(**context)
    return template_str


def _default_entities() -> list:
    """默认实体示例"""
    return [{
        'name': 'User', 'table': 't_user',
        'fields': [
            {'name': 'id', 'type': 'Long', 'pk': True, 'auto': True},
            {'name': 'name', 'type': 'String', 'nullable': False},
            {'name': 'email', 'type': 'String', 'unique': True},
            {'name': 'status', 'type': 'String', 'default': 'ACTIVE'},
        ]
    }]


def _gen_crud_for_lang(entity: dict, lang: str, dry_run: bool) -> list:
    """为指定语言生成 CRUD 代码"""
    results = []
    entity_name = entity['name']
    fields = entity.get('fields', [])
    tmpl_dir = TEMPLATES_DIR / 'code' / lang
    if not tmpl_dir.exists():
        return results
    for tmpl_file in tmpl_dir.glob('*.j2'):
        ctx = {
            'entity': entity_name,
            'fields': fields,
            'entity_lower': entity_name.lower(),
            'table': entity.get('table', 't_' + entity_name.lower()),
            'date': date.today().isoformat(),
            'has_id': any(f.get('pk') for f in fields),
        }
        rendered = _render_jinja(tmpl_file.read_text(encoding='utf-8'), ctx)
        if not dry_run:
            out_dir = DOCS_DIR / f'code/{lang}'
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{entity_name}{tmpl_file.stem.replace('.j2', '')}"
            out_file.write_text(rendered, encoding='utf-8')
            results.append(str(out_file))
    return results
```

**engine.py main 函数修改**：
```python
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AES Knowledge-Driven Multi-Type Generator")
    parser.add_argument("domain", nargs="?", help="领域 key")
    parser.add_argument("--all", "-a", action="store_true")
    parser.add_argument("--dry-run", "-n", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--list", "-l", action="store_true")
    parser.add_argument("--type", "-t", choices=list(GENERATOR_TYPES.keys()) + ["all"],
                        default="all" if "--all" in sys.argv else "rule")
    parser.add_argument("--format", "-f", choices=["md", "json"], default="md")
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable domains:")
        for key in list_standards():
            print(f"  - {key}")
        print("\nGenerator types:")
        for gt, desc in GENERATOR_TYPES.items():
            print(f"  - {gt}: {desc}")
        return
    
    engine = KnowledgeEngine(verbose=args.verbose or args.dry_run)
    registry = GeneratorRegistry(engine)
    
    if args.type == 'all':
        types_to_run = list(GENERATOR_TYPES.keys())
    else:
        types_to_run = [args.type]
    
    total = 0
    for gt in types_to_run:
        files = registry.generate(gt, args.domain, args.all, args.dry_run, args.format)
        total += len(files)
    
    print(f"\nTotal: {total} files generated.")
```

---

## 待实施：Phase 1.3 — 创建代码模板仓库

### 目录结构
创建以下 `templates/code/{lang}/` 目录和模板文件：

```
templates/code/
├── flutter/
│   ├── model.dart.j2         # class {{ entity }} ...
│   ├── service.dart.j2       # class {{ entity }}Service ...
│   └── provider.dart.j2      # final {{ entity_lower }}Provider ...
├── spring/
│   ├── entity.java.j2        # @Entity @Table(name="{{ table }}")
│   ├── repository.java.j2    # public interface {{ entity }}Repository
│   ├── service.java.j2       # @Service public class {{ entity }}Service
│   ├── controller.java.j2    # @RestController @RequestMapping("/api/v1/{{ entity_lower }}s")
│   └── dto.java.j2           # public class {{ entity }}Request / {{ entity }}Response
├── vue3/
│   ├── page.vue.j2           # <script setup lang="ts"> ...
│   ├── composable.ts.j2      # export function use{{ entity }}() ...
│   └── api.ts.j2             # export const {{ entity_lower }}Api = ...
├── react/
│   ├── component.tsx.j2      # export function {{ entity }}List() ...
│   ├── hook.ts.j2            # export function use{{ entity }}() ...
│   └── api.ts.j2             # export const {{ entity_lower }}Api = ...
├── go/
│   ├── model.go.j2           # type {{ entity }} struct ...
│   ├── handler.go.j2         # func (h *Handler) Create{{ entity }} ...
│   └── repository.go.j2      # type {{ entity }}Repository struct ...
├── rust/
│   ├── model.rs.j2           # struct {{ entity }} ...
│   └── handler.rs.j2         # async fn create_{{ entity_lower }} ...
└── kotlin/
    ├── model.kt.j2           # data class {{ entity }} ...
    └── route.kt.j2           # fun Route.{{ entity_lower }}Routes() ...
```

### 最小模板示例 (spring/entity.java.j2)
```java
package com.alive.{{ entity_lower }};

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "{{ table }}")
public class {{ entity }} {
    {% for field in fields %}
    {% if field.pk %}@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY){% endif %}
    @Column(name = "{{ field.name }}"{% if field.nullable is false %}, nullable = false{% endif %})
    private {{ field.type }} {{ field.name }};
    {% endfor %}
}
```

---

## 待实施：Phase 1.4 — entities.yaml schema

### 文件位置
`generator/config/entities.yaml`

### 内容
```yaml
# AES CRUD Code Generation Entity Definitions
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
      - name: username
        type: String
        length: 50
        nullable: false
        unique: true
      - name: email
        type: String
        length: 100
        nullable: false
      - name: status
        type: String
        default: ACTIVE
      - name: createdAt
        type: LocalDateTime
        auto: true
    indexes:
      - fields: [username]
        unique: true

  - name: Product
    module: product
    table: t_product
    description: "产品"
    fields:
      - name: id
        type: Long
        pk: true
        auto: true
      - name: name
        type: String
        length: 200
        nullable: false
      - name: price
        type: BigDecimal
        nullable: false
      - name: description
        type: String
        length: 2000
      - name: status
        type: String
        default: DRAFT

  - name: Order
    module: order
    table: t_order
    description: "订单"
    fields:
      - name: id
        type: Long
        pk: true
        auto: true
      - name: userId
        type: Long
        nullable: false
      - name: totalAmount
        type: BigDecimal
        nullable: false
      - name: status
        type: String
        default: PENDING
```

---

## 待实施：Phase 1.5 — mkdocs.yml 更新

### 现有 mkdocs.yml 有 24 个领域的 nav 条目
需要更新所有 domain 的 nav 指向其生成的 doc 文件：

找到 `mkdocs.yml` 中 `nav:` 部分，对每个新 standards 文件对应的领域添加 nav 条目。

### Nav 条目格式示例（API 领域）
```yaml
  - API 设计规范:
    - RESTful API 规范: 08_API/801_RESTfulAPI.md
    - API 版本管理: 08_API/802_API.md
    - 错误码规范: 08_API/803_Doc3.md
    - 分页与过滤: 08_API/804_Doc4.md
    - OpenAPI 规范: 08_API/805_OpenAPI.md
```

---

## 执行方式

由于环境限制（子代理 API key 缺失），Phase 1.2-1.5 需要以下方式之一执行：

### 方式 A：将任务带入新会话
复制 Phase 1.2 的 `engine.py` 修改代码（见上），在新会话中使用 `task` 或直接 `write` 写入。

### 方式 B：手动执行
1. 编辑 `generator/engine.py` — 添加 Jinja2 导入 + GeneratorRegistry 类 + 增强 main
2. 创建 `templates/code/{lang}/*.j2` — 代码模板文件
3. 创建 `generator/config/entities.yaml` — 实体定义
4. 编辑 `mkdocs.yml` — 更新 nav 条目
5. 运行 `python -m generator --all --type all` 验证

### 方式 C：配置 API key
```bash
# Windows
setx GOOGLE_GENERATIVE_AI_API_KEY "your-api-key-here"
# 然后重启 OpenCode
```
