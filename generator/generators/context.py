"""上下文文档生成器 — 从文档章节内容生成 AI 上下文文档"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import Domain, GeneratorConfig
from ..utils import build_sections, compute_filename, today_str, get_domain


class ContextGenerator:
    """上下文文档生成器"""

    def __init__(self, env: Environment, docs_base: Path, config: GeneratorConfig):
        self.env = env
        self.docs_base = docs_base
        self.config = config

    def generate(
        self,
        domain_key: Optional[str] = None,
        count: Optional[int] = None,
        all_flag: bool = False,
        dry_run: bool = False,
        verbose: bool = True,
    ) -> list[str]:
        """生成上下文文档"""
        if all_flag:
            return self._generate_all(count, dry_run, verbose)
        if domain_key:
            domain = get_domain(self.config, domain_key)
            if not domain:
                return []
            return self._generate_domain(domain, count, dry_run, verbose)
        return []

    def _generate_all(self, count=None, dry_run=False, verbose=True) -> list[str]:
        total = []
        for domain in self.config.domains:
            total.extend(self._generate_domain(domain, count, dry_run, verbose))
        return total

    def _generate_domain(
        self, domain: Domain, count=None, dry_run=False, verbose=True
    ) -> list[str]:
        docs = domain.documents
        if not docs or domain.source_files:
            return []

        if count and count < len(docs):
            docs = docs[:count]

        output_dir = self.docs_base / domain.dir
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        template = self.env.get_template("context.md.j2")
        generated = []

        for i, doc in enumerate(docs, 1):
            sections = build_sections(doc)
            rules = []
            for sec in sections:
                summary = sec["content"].strip().replace("\n", " ")[:150]
                rules.append({
                    "title": f"{doc.title} — {sec['title']}",
                    "summary": summary,
                })

            # 从所有章节提取关键约定
            conventions = []
            seen_terms = set()
            for sec in sections:
                content_lower = sec["content"].lower()
                for kw in ["必须", "禁止", "推荐", "统一使用", "不允许", "规则"]:
                    if kw in content_lower:
                        # 提取含有关键词的第一句
                        for line in sec["content"].split("\n"):
                            if kw in line.lower() and line.strip():
                                key = line.strip()[:60]
                                if key not in seen_terms:
                                    seen_terms.add(key)
                                    conventions.append({
                                        "name": f"{sec['title']}：{kw}",
                                        "description": line.strip()[:120],
                                    })
                                break

            references = [
                {"title": f"{doc.title}", "path": compute_filename(domain, doc)},
            ]

            context = {
                "title": f"{domain.name} — AI 上下文",
                "domain_name": domain.name,
                "version": self.config.version,
                "domain_description": domain.description,
                "rules": rules,
                "conventions": conventions[:8],  # 最多 8 条
                "references": references,
                "date": today_str(),
            }

            rendered = template.render(**context)
            filename = f"context_{compute_filename(domain, doc)}"
            filepath = output_dir / filename

            if not dry_run:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rendered)

            generated.append(str(filepath))
            if verbose:
                print(f"  + [Context] {filename}")

        return generated
