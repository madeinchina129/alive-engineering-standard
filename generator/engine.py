"""AES Knowledge-Driven Document Generator

从 knowledge/ + standards/ + templates/ 组装生成多类型文档。
支持类型: rule, prompt, checklist, template, code, blueprint, graph
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    from jinja2 import Environment, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False


# -- Paths -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STANDARDS_DIR = PROJECT_ROOT / "standards"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "generator" / "config"


# -- Generator Types Registry ------------------------------------------------

GENERATOR_TYPES = {
    "rule": "规则文档",
    "prompt": "AI Prompt 文档",
    "checklist": "检查清单文档",
    "template": "代码模板",
    "code": "CRUD 代码生成",
    "blueprint": "架构蓝图",
    "graph": "依赖关系图",
}


# -- Section type mapping ---------------------------------------------------

SECTION_TYPE_MAP = {
    "overview": "overview",
    "rule": "rule",
    "faq": "faq",
    "checklist": "checklist",
    "prompt": "prompt",
}

CODE_EXTENSIONS = {".dart", ".java", ".kt", ".ts", ".vue", ".py", ".yaml", ".xml", ".json", ".sql"}


def _detect_section_type(filename: str) -> str:
    """根据文件名推断 section 类型"""
    stem = Path(filename).stem.lower()
    ext = Path(filename).suffix.lower()
    if ext in CODE_EXTENSIONS:
        return "example"
    if stem in SECTION_TYPE_MAP:
        return SECTION_TYPE_MAP[stem]
    if ext == ".md":
        return "content"
    return "content"


# -- YAML loader ------------------------------------------------------------

def load_standards(domain_key: str) -> Optional[dict]:
    """加载 standards/<domain>.yaml"""
    path = STANDARDS_DIR / f"{domain_key}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_standards() -> list[str]:
    """列出所有可用标准"""
    return sorted(
        [f.stem for f in STANDARDS_DIR.glob("*.yaml") if f.stem != "domain"]
    )


# -- Knowledge reader -------------------------------------------------------

def read_knowledge_dir(knowledge_dir: str) -> list[dict]:
    """读取 knowledge/<knowledge_dir>/ 下的所有知识文件"""
    base = KNOWLEDGE_DIR / knowledge_dir
    if not base.exists():
        return []
    sections = []
    files = sorted(base.iterdir(), key=lambda f: _sort_key(f.name))
    for fpath in files:
        if not fpath.is_file() or fpath.name.startswith("."):
            continue
        content = fpath.read_text(encoding="utf-8").strip()
        if not content:
            continue
        section_type = _detect_section_type(fpath.name)
        ext = fpath.suffix.lower()
        sections.append({
            "type": section_type,
            "source": fpath.name,
            "content": content,
            "is_code": ext in CODE_EXTENSIONS,
        })
    return sections


def _sort_key(filename: str) -> int:
    """排序键：固定顺序"""
    order = ["overview", "rule", "example", "faq", "checklist", "prompt"]
    stem = Path(filename).stem.lower()
    try:
        return order.index(stem)
    except ValueError:
        return 99


# -- Template renderer ------------------------------------------------------

def _jinja2_render(template_content: str, **kwargs) -> str:
    """简化模板渲染（优先使用 Jinja2，否则降级到自定义渲染器）"""
    if HAS_JINJA2:
        try:
            env = Environment()
            tmpl = env.from_string(template_content)
            return tmpl.render(**kwargs)
        except Exception:
            pass
    return _simple_render(template_content, **kwargs)


def _simple_render(template_content: str, **kwargs) -> str:
    """自定义模板渲染（无依赖版本）"""
    result = template_content

    def replace_var(match):
        expr = match.group(1).strip()
        if "| default(" in expr:
            parts = expr.split("| default(")
            var_name = parts[0].strip()
            default_val = parts[1].rstrip(")").strip().strip("'\"")
            keys = var_name.split(".")
            val = kwargs
            for k in keys:
                if isinstance(val, dict):
                    val = val.get(k, ...)
                else:
                    val = ...
                if val is ...:
                    break
            if val is ... or val is None:
                return default_val
            return str(val)
        keys = expr.split(".")
        val = kwargs
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, ...)
            else:
                val = ...
            if val is ...:
                return ""
        if val is None:
            return ""
        return str(val)

    result = re.sub(r"\{\{\s*(.*?)\s*\}\}", replace_var, result)

    def replace_for(match):
        loop_content = match.group(1)
        for_match = re.search(r"{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}", loop_content)
        if not for_match:
            return match.group(0)
        item_var = for_match.group(1)
        list_var = for_match.group(2)
        items = kwargs.get(list_var, [])
        if not items:
            return ""
        body = re.sub(r"{%\s*for\s+.*?%}", "", loop_content, count=1).strip()
        body = re.sub(r"{%\s*endfor\s*%}", "", body).strip()
        parts = []
        for item in items:
            item_kwargs = {**kwargs, item_var: item}
            def replace_item_var(m):
                expr = m.group(1).strip()
                if expr.startswith(f"{item_var}."):
                    key = expr[len(item_var) + 1:]
                    if isinstance(item, dict):
                        val = item.get(key, "")
                        return str(val) if val is not None else ""
                if expr == "loop.index":
                    return str(len(parts) + 1)
                return replace_var(m)
            rendered = re.sub(r"\{\{\s*(.*?)\s*\}\}", replace_item_var, body)
            parts.append(rendered)
        return "\n".join(parts)

    result = re.sub(
        r"({%\s*for\s+.*?%}.*?{%\s*endfor\s*%})",
        replace_for,
        result,
        flags=re.DOTALL,
    )

    def replace_if(match):
        block = match.group(1)
        return _evaluate_if_block(block, kwargs)

    result = re.sub(
        r"({%\s*if\s+.*?%}.*?{%\s*endif\s*%})",
        replace_if,
        result,
        flags=re.DOTALL,
    )

    result = re.sub(r"{%\s*endif\s*%}", "", result)
    result = re.sub(r"{%\s*else\s*%}", "", result)
    result = re.sub(r"{%\s*if\s+.*?%}", "", result)
    result = re.sub(r"{%\s*elif\s+.*?%}", "", result)

    return result


def _evaluate_if_block(block: str, kwargs: dict) -> str:
    """评估 if/elif/else 块"""
    pattern = r"{%\s*(if|elif|else)\s*(.*?)\s*%}"
    parts = re.split(pattern, block)
    i = 1
    while i < len(parts):
        tag = parts[i].strip() if i < len(parts) else ""
        condition = parts[i + 1].strip() if i + 1 < len(parts) else ""
        content = parts[i + 2] if i + 2 < len(parts) else ""
        i += 3
        if tag == "if" or tag == "elif":
            if _eval_condition(condition, kwargs):
                return _render_if_body(content, kwargs)
        elif tag == "else":
            return _render_if_body(content, kwargs)
    return ""


def _eval_condition(condition: str, kwargs: dict) -> bool:
    condition = condition.strip()
    if not condition:
        return True
    if condition.startswith("not "):
        var = condition[4:].strip()
        return not bool(_resolve_var(var, kwargs))
    return bool(_resolve_var(condition, kwargs))


def _resolve_var(expr: str, kwargs: dict) -> Any:
    keys = expr.split(".")
    val = kwargs
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k, ...)
        else:
            val = ...
        if val is ...:
            return ...
    return val


def _render_if_body(content: str, kwargs: dict) -> str:
    result = content.strip()
    result = re.sub(
        r"{%\s*for\s+.*?%}.*?{%\s*endfor\s*%}",
        lambda m: replace_for_block_simple(m, kwargs),
        result,
        flags=re.DOTALL,
    )
    result = re.sub(r"\{\{\s*(.*?)\s*\}\}", lambda m: replace_var_simple(m, kwargs), result)
    return result


def replace_var_simple(match, kwargs) -> str:
    expr = match.group(1).strip()
    val = _resolve_var(expr, kwargs)
    if val is ... or val is None:
        return ""
    return str(val)


def replace_for_block_simple(match, kwargs) -> str:
    block = match.group(0)
    for_match = re.search(r"{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}", block)
    if not for_match:
        return block
    item_var = for_match.group(1)
    list_var = for_match.group(2)
    items = kwargs.get(list_var, [])
    if not items:
        return ""
    body = re.sub(r"{%\s*for\s+.*?%}", "", block, count=1)
    body = re.sub(r"{%\s*endfor\s*%}", "", body).strip()
    parts = []
    for item in items:
        item_kwargs = {**kwargs, item_var: item}
        rendered = re.sub(
            r"\{\{\s*(.*?)\s*\}\}",
            lambda m: _replace_item_var(m, item_var, item, item_kwargs),
            body,
        )
        parts.append(rendered)
    return "\n".join(parts)


def _replace_item_var(match, item_var, item, kwargs) -> str:
    expr = match.group(1).strip()
    if expr.startswith(f"{item_var}."):
        key = expr[len(item_var) + 1:]
        if isinstance(item, dict):
            val = item.get(key, "")
            return str(val) if val is not None else ""
    return replace_var_simple(match, kwargs)


# -- Generator Registry -----------------------------------------------------

class GeneratorRegistry:
    """生成器注册表 — 根据类型分派到不同生成逻辑"""

    def __init__(self, engine):
        self.engine = engine
        self._generators = {
            "rule": self._gen_rule,
            "prompt": self._gen_prompt,
            "checklist": self._gen_checklist,
            "template": self._gen_template,
            "code": self._gen_code,
            "blueprint": self._gen_blueprint,
            "graph": self._gen_graph,
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
        """规则文档 — KnowledgeEngine 核心逻辑"""
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
        return self._extract_section("prompt", domain_key, all_flag, dry_run, fmt)

    def _gen_checklist(self, domain_key, all_flag, dry_run, fmt):
        """提取 knowledge/ 中的 checklist.md 文件"""
        return self._extract_section("checklist", domain_key, all_flag, dry_run, fmt)

    def _extract_section(self, section_type, domain_key, all_flag, dry_run, fmt):
        """提取指定 section 类型的内容"""
        domains = [domain_key] if domain_key else list_standards()
        results = []
        for dk in domains:
            std = load_standards(dk)
            if not std:
                continue
            for doc in std.get("documents", []):
                kdir = doc.get("knowledge_dir", "")
                if not kdir:
                    continue
                sections = read_knowledge_dir(kdir)
                for sec in sections:
                    if sec["type"] == section_type:
                        if fmt == "json":
                            print(json.dumps({
                                "domain": dk,
                                "title": doc["title"],
                                "content": sec["content"],
                            }, ensure_ascii=False))
                        results.append(f"{dk}/{doc['title']}")
        return results

    def _gen_template(self, domain_key, all_flag, dry_run, fmt):
        """代码模板生成器 — 读取 templates/code/{lang}/*.j2"""
        langs = ["flutter", "spring", "vue3", "react", "go", "rust", "kotlin"]
        if domain_key and domain_key in langs:
            langs = [domain_key]
        results = []
        for lang in langs:
            tmpl_dir = TEMPLATES_DIR / "code" / lang
            if not tmpl_dir.exists():
                continue
            for tmpl_file in tmpl_dir.glob("*.j2"):
                output_name = tmpl_file.stem.replace(".j2", "")
                section = tmpl_file.stem.split(".")[0]
                ctx = _build_template_context(lang, section)
                rendered = _jinja2_render(tmpl_file.read_text(encoding="utf-8"), **ctx)
                if not dry_run:
                    out_dir = DOCS_DIR / f"templates/{lang}"
                    out_dir.mkdir(parents=True, exist_ok=True)
                    (out_dir / output_name).write_text(rendered, encoding="utf-8")
                results.append(f"{lang}/{output_name}")
        return results

    def _gen_code(self, domain_key, all_flag, dry_run, fmt):
        """CRUD 代码生成 — 从 entities.yaml 读取实体定义"""
        entities_path = CONFIG_DIR / "entities.yaml"
        entities = []
        if entities_path.exists():
            with open(entities_path, encoding="utf-8") as f:
                entities = yaml.safe_load(f).get("entities", [])
        if not entities:
            entities = _default_entities()
        langs = ["flutter", "spring"]
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
        if fmt == "json":
            graph = {"nodes": [], "edges": []}
            for f in STANDARDS_DIR.glob("*.yaml"):
                std = yaml.safe_load(f.read_text(encoding="utf-8"))
                if std and "domain" in std:
                    graph["nodes"].append({"id": std["domain"]["key"], "name": std["domain"]["name"]})
            print(json.dumps(graph, ensure_ascii=False))
        return ["graph generated"]


def _build_template_context(lang: str, section: str) -> dict:
    """构建代码模板上下文"""
    ctx = {"date": date.today().isoformat(), "lang": lang, "section": section}
    if section == "model":
        ctx.update({"class_name": "ExampleModel", "fields": [
            {"name": "id", "type": "String"}, {"name": "name", "type": "String"}
        ]})
    elif section == "service":
        ctx.update({"class_name": "ExampleService", "model_name": "ExampleModel"})
    elif section == "controller":
        ctx.update({"class_name": "ExampleController", "endpoint": "examples"})
    elif section == "repository":
        ctx.update({"class_name": "ExampleRepository", "entity_name": "ExampleEntity"})
    return ctx


def _default_entities() -> list:
    """默认实体示例"""
    return [{
        "name": "User", "table": "t_user",
        "fields": [
            {"name": "id", "type": "Long", "pk": True, "auto": True},
            {"name": "name", "type": "String", "nullable": False},
            {"name": "email", "type": "String", "unique": True},
            {"name": "status", "type": "String", "default": "ACTIVE"},
        ]
    }]


def _gen_crud_for_lang(entity: dict, lang: str, dry_run: bool) -> list:
    """为指定语言生成 CRUD 代码"""
    results = []
    entity_name = entity["name"]
    fields = entity.get("fields", [])
    tmpl_dir = TEMPLATES_DIR / "code" / lang
    if not tmpl_dir.exists():
        return results
    for tmpl_file in tmpl_dir.glob("*.j2"):
        ctx = {
            "entity": entity_name,
            "fields": fields,
            "entity_lower": entity_name.lower(),
            "table": entity.get("table", "t_" + entity_name.lower()),
            "date": date.today().isoformat(),
            "has_id": any(f.get("pk") for f in fields),
        }
        rendered = _jinja2_render(tmpl_file.read_text(encoding="utf-8"), **ctx)
        if not dry_run:
            out_dir = DOCS_DIR / f"code/{lang}"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{entity_name}{tmpl_file.stem.replace('.j2', '')}"
            out_file.write_text(rendered, encoding="utf-8")
            results.append(str(out_file))
    return results


# -- Document generation ----------------------------------------------------

class KnowledgeEngine:
    """知识驱动文档生成引擎"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.registry = GeneratorRegistry(self)

    def generate_domain(self, domain_key: str, dry_run: bool = False) -> list[str]:
        """生成一个领域的所有文档"""
        standards = load_standards(domain_key)
        if not standards:
            print(f"[ERROR] Standards not found: {domain_key}")
            return []

        domain_info = standards.get("domain", {})
        documents = standards.get("documents", [])
        domain_name = domain_info.get("name", domain_key)
        domain_dir = domain_info.get("dir", domain_key)
        domain_prefix = domain_info.get("prefix", "")

        output_base = DOCS_DIR / domain_dir
        if not dry_run:
            output_base.mkdir(parents=True, exist_ok=True)

        generated = []
        template_content = self._load_template()

        for doc in documents:
            knowledge_dir = doc.get("knowledge_dir", "")
            if not knowledge_dir:
                if self.verbose:
                    print(f"  SKIP {doc['title']}: no knowledge_dir")
                continue

            sections = read_knowledge_dir(knowledge_dir)
            if not sections:
                if self.verbose:
                    print(f"  SKIP {doc['title']}: no knowledge content at {knowledge_dir}")
                continue

            metadata = {
                "id": doc.get("id", ""),
                "title": doc.get("title", ""),
                "priority": doc.get("priority", "P2"),
                "owner": doc.get("owner", ""),
                "version": doc.get("version", "1.0"),
                "description": doc.get("description", ""),
            }

            related = doc.get("related", [])
            related_docs = []
            for rel_id in related:
                rel_doc = self._find_doc_by_id(standards, rel_id)
                if rel_doc:
                    rel_index = rel_doc.get("index", 0)
                    rel_filename = rel_doc.get("filename", rel_doc.get("title", ""))
                    related_docs.append({
                        "id": rel_id,
                        "title": rel_doc.get("title", rel_id),
                        "path": f"../{domain_dir}/{domain_prefix}{rel_index:02d}_{rel_filename}.md",
                    })

            rendered = self._render_document(
                template_content=template_content,
                metadata=metadata,
                domain_name=domain_name,
                domain_key=domain_key,
                knowledge_rel_dir=knowledge_dir,
                sections=sections,
                related_docs=related_docs,
            )

            index = doc.get("index", 0)
            filename = doc.get("filename", doc["title"])
            output_name = f"{domain_prefix}{index:02d}_{filename}.md"
            output_path = output_base / output_name

            if not dry_run:
                output_path.write_text(rendered, encoding="utf-8")
                if self.verbose:
                    print(f"  WRITE {output_path.name} ({len(sections)} sections)")
            else:
                if self.verbose:
                    print(f"  DRY-RUN {output_path.name} ({len(sections)} sections)")

            generated.append(str(output_path))

        return generated

    def _load_template(self) -> str:
        """加载模板"""
        template_path = TEMPLATES_DIR / "rule.md.j2"
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        return """# {{ metadata.title }}

> **领域**: {{ domain_name }}

{% for section in sections %}
{% if section.type == 'overview' %}
## 概述
{{ section.content }}
{% elif section.type == 'rule' %}
## 使用规范
{{ section.content }}
{% elif section.type == 'example' %}
## 代码示例
```dart
{{ section.content }}
```
{% elif section.type == 'faq' %}
## 常见问题
{{ section.content }}
{% elif section.type == 'checklist' %}
## 检查清单
{{ section.content }}
{% elif section.type == 'prompt' %}
## AI Prompt
{{ section.content }}
{% endif %}
{% endfor %}
"""

    def _render_document(
        self,
        template_content: str,
        metadata: dict,
        domain_name: str,
        domain_key: str,
        knowledge_rel_dir: str,
        sections: list,
        related_docs: list,
    ) -> str:
        """渲染文档"""
        today = date.today().isoformat()
        return _jinja2_render(
            template_content,
            metadata=metadata,
            domain_name=domain_name,
            domain_key=domain_key,
            knowledge_rel_dir=knowledge_rel_dir,
            sections=sections,
            related_docs=related_docs,
            date=today,
        )

    @staticmethod
    def _find_doc_by_id(standards: dict, doc_id: str) -> Optional[dict]:
        """按 ID 查找文档"""
        for doc in standards.get("documents", []):
            if doc.get("id") == doc_id:
                return doc
        return None


# -- CLI --------------------------------------------------------------------

def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AES Knowledge-Driven Document Generator"
    )
    parser.add_argument("domain", nargs="?", help="领域 key (flutter, springboot, ...)")
    parser.add_argument("--all", "-a", action="store_true", help="生成所有领域")
    parser.add_argument("--dry-run", "-n", action="store_true", help="调试模式，不写入")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用领域和生成器类型")
    parser.add_argument("--type", "-t",
                        choices=list(GENERATOR_TYPES.keys()) + ["all"],
                        default="rule", help="生成器类型")
    parser.add_argument("--format", "-f", choices=["md", "json"],
                        default="md", help="输出格式")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable domains:")
        for key in list_standards():
            print(f"  - {key}")
        print("\nGenerator types:")
        for gt, desc in GENERATOR_TYPES.items():
            print(f"  - {gt}: {desc}")
        print()
        return

    engine = KnowledgeEngine(verbose=args.verbose or args.dry_run)

    if args.type == "all":
        types_to_run = list(GENERATOR_TYPES.keys())
    else:
        types_to_run = [args.type]

    total = 0
    for gt in types_to_run:
        if args.verbose:
            print(f"\n[{gt}] Generating...")
        files = engine.registry.generate(
            gt,
            domain_key=args.domain if args.domain else None,
            all_flag=args.all,
            dry_run=args.dry_run,
            output_format=args.format,
        )
        total += len(files)
        if args.verbose and files:
            for f in files[:5]:
                print(f"  + {f}")

    print(f"\nTotal: {total} files generated.")


if __name__ == "__main__":
    main()