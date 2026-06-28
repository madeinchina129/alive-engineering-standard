"""AES Knowledge-Driven Document Generator

从 knowledge/ + standards/ + templates/ 组装生成 Markdown 文档。
"""

import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml


# ── Paths ─────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STANDARDS_DIR = PROJECT_ROOT / "standards"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DOCS_DIR = PROJECT_ROOT / "docs"


# ── Section type mapping ──────────────────────────────────────────────────

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
    # fallback: use extension
    if ext == ".md":
        return "content"  # generic markdown section
    return "content"


# ── YAML loader ───────────────────────────────────────────────────────────

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


# ── Knowledge reader ──────────────────────────────────────────────────────

def read_knowledge_dir(knowledge_dir: str) -> list[dict]:
    """读取 knowledge/<knowledge_dir>/ 下的所有知识文件"""
    base = KNOWLEDGE_DIR / knowledge_dir
    if not base.exists():
        return []

    sections = []
    # 按名称排序确保一致顺序
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


# ── Template renderer ────────────────────────────────────────────────────

def _jinja2_render(template_content: str, **kwargs) -> str:
    """简化 Jinja2 渲染（无依赖版，仅支持变量替换和 for/if）"""
    result = template_content

    # 替换 {{ var }} / {{ var | default('x') }}
    def replace_var(match):
        expr = match.group(1).strip()
        # 处理 default filter
        if "| default(" in expr:
            parts = expr.split("| default(")
            var_name = parts[0].strip()
            default_val = parts[1].rstrip(")").strip().strip("'\"")
            # 尝试从 kwargs 获取
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
        # 普通变量替换
        keys = expr.split(".")
        val = kwargs
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, ...)
            else:
                val = ...
            if val is ...:
                return f"{{{{ {expr} }}}}"  # 保持原样
        if val is None:
            return ""
        return str(val)

    result = re.sub(r"\{\{\s*(.*?)\s*\}\}", replace_var, result)

    # 处理简单的 {% for section in sections %} ... {% endfor %}
    def replace_for(match):
        loop_content = match.group(1)
        # 解析 for 语句
        for_match = re.search(r"{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}", loop_content)
        if not for_match:
            return match.group(0)
        item_var = for_match.group(1)
        list_var = for_match.group(2)

        items = kwargs.get(list_var, [])
        if not items:
            return ""

        # 获取循环体内的内容（去掉 for 和 endfor 标签）
        body = re.sub(
            r"{%\s*for\s+.*?%}", "", loop_content, count=1
        ).strip()
        body = re.sub(r"{%\s*endfor\s*%}", "", body).strip()

        parts = []
        for item in items:
            item_kwargs = {**kwargs, item_var: item}
            # 替换 item 内部的变量
            def replace_item_var(m):
                expr = m.group(1).strip()
                # {{ section.type }} → item['type']
                if expr.startswith(f"{item_var}."):
                    key = expr[len(item_var) + 1:]
                    if isinstance(item, dict):
                        val = item.get(key, "")
                        return str(val) if val is not None else ""
                # {{ loop.index }}
                if expr == "loop.index":
                    return str(len(parts) + 1)
                # 其他变量从 kwargs 取
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

    # 处理 {% if x %} ... {% elif y %} ... {% else %} ... {% endif %}
    def replace_if(match):
        block = match.group(1)
        return _evaluate_if_block(block, kwargs)

    result = re.sub(
        r"({%\s*if\s+.*?%}.*?{%\s*endif\s*%})",
        replace_if,
        result,
        flags=re.DOTALL,
    )

    # 去除所有残留模板标签
    result = re.sub(r"{%\s*endif\s*%}", "", result)
    result = re.sub(r"{%\s*else\s*%}", "", result)
    result = re.sub(r"{%\s*if\s+.*?%}", "", result)
    result = re.sub(r"{%\s*elif\s+.*?%}", "", result)

    return result


def _evaluate_if_block(block: str, kwargs: dict) -> str:
    """评估 if/elif/else 块"""
    # 分割条件块
    pattern = r"{%\s*(if|elif|else)\s*(.*?)\s*%}"
    parts = re.split(pattern, block)
    
    # parts[0] = leading text (usually empty)
    # parts[1] = 'if', parts[2] = condition, parts[3] = content
    # parts[4] = 'elif'/'else', parts[5] = condition/'', parts[6] = content
    # ...

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
    """评估简单的模板条件"""
    condition = condition.strip()
    if not condition:
        return True
    
    # not X
    if condition.startswith("not "):
        var = condition[4:].strip()
        val = _resolve_var(var, kwargs)
        return not bool(val)

    # X
    val = _resolve_var(condition, kwargs)
    if val is ...:
        return False
    return bool(val)


def _resolve_var(expr: str, kwargs: dict) -> Any:
    """从 kwargs 中解析变量值"""
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
    """渲染 if 块内部的内容（递归处理嵌套的 for/if）"""
    result = content.strip()
    # 嵌套的 for 循环
    result = re.sub(
        r"{%\s*for\s+.*?%}.*?{%\s*endfor\s*%}",
        lambda m: replace_for_block_simple(m, kwargs),
        result,
        flags=re.DOTALL,
    )
    # 变量替换
    result = re.sub(r"\{\{\s*(.*?)\s*\}\}", lambda m: replace_var_simple(m, kwargs), result)
    return result


def replace_var_simple(match, kwargs) -> str:
    expr = match.group(1).strip()
    val = _resolve_var(expr, kwargs)
    if val is ... or val is None:
        return ""
    return str(val)


def replace_for_block_simple(match, kwargs) -> str:
    """处理 for 循环块（简化版）"""
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


# ── Document generation ─────────────────────────────────────────────────

class KnowledgeEngine:
    """知识驱动文档生成引擎"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

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

            # 构建模板上下文
            metadata = {
                "id": doc.get("id", ""),
                "title": doc.get("title", ""),
                "priority": doc.get("priority", "P2"),
                "owner": doc.get("owner", ""),
                "version": doc.get("version", "1.0"),
                "description": doc.get("description", ""),
            }

            # 关联文档链接
            related = doc.get("related", [])
            related_docs = []
            for rel_id in related:
                rel_name = rel_id.replace(f"{domain_key}.", "").replace("_", " ").title()
                # 查找关联文档的 knowledge_dir
                rel_doc = self._find_doc_by_id(standards, rel_id)
                if rel_doc:
                    rel_index = rel_doc.get("index", 0)
                    rel_filename = rel_doc.get("filename", rel_doc.get("title", ""))
                    related_docs.append({
                        "id": rel_id,
                        "title": rel_doc.get("title", rel_name),
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

            # 生成文件名
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
        # 默认模板
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


# ── CLI ───────────────────────────────────────────────────────────────────

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
    parser.add_argument("--list", "-l", action="store_true", help="列出可用领域")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable domains:")
        for key in list_standards():
            print(f"  - {key}")
        print()
        return

    engine = KnowledgeEngine(verbose=args.verbose or args.dry_run)

    if args.all:
        domains = list_standards()
        total = 0
        for domain_key in domains:
            print(f"\n[{domain_key}]")
            files = engine.generate_domain(domain_key, dry_run=args.dry_run)
            total += len(files)
            print(f"  -> {len(files)} files")
        print(f"\nTotal: {total} files generated.")
        return

    if args.domain:
        print(f"\nGenerating: {args.domain}")
        files = engine.generate_domain(args.domain, dry_run=args.dry_run)
        print(f"  -> {len(files)} files generated.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
