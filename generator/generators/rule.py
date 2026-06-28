"""规则文档生成器 — 从 YAML 配置和 Jinja2 模板生成规范文档"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..config import load_config
from ..models import Domain, GeneratorConfig
from ..utils import build_sections, compute_filename, today_str, get_domain


class RuleGenerator:
    """规则文档生成器"""

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
        """生成规则文档

        Args:
            domain_key: 指定域 key（如 flutter、api），None 时根据 all_flag 决定
            count: 生成的文档数量（None=全部）
            all_flag: 是否生成所有域的文档
            dry_run: 仅打印，不写入文件
            verbose: 是否打印详细信息

        Returns:
            生成的文档路径列表
        """
        if all_flag:
            return self._generate_all(count, dry_run, verbose)
        if domain_key:
            domain = get_domain(self.config, domain_key)
            if not domain:
                print(f"[ERROR] Domain not found: {domain_key}")
                return []
            return self._generate_domain(domain, count, dry_run, verbose)
        return []

    def _generate_all(
        self,
        count: Optional[int] = None,
        dry_run: bool = False,
        verbose: bool = True,
    ) -> list[str]:
        """生成所有域的文档"""
        total = []
        if verbose:
            print("\nGenerating all domain documents...\n")
        for domain in self.config.domains:
            if verbose:
                print(f"[{domain.key}] {domain.name}")
            generated = self._generate_domain(domain, count, dry_run, verbose)
            total.extend(generated)
            if verbose:
                print()
        if verbose:
            print(f"Done! Generated {len(total)} documents.")
        return total

    def _generate_domain(
        self,
        domain: Domain,
        count: Optional[int] = None,
        dry_run: bool = False,
        verbose: bool = True,
    ) -> list[str]:
        """为指定域生成文档"""
        # Skip domains with source files (manually written, not generated)
        if domain.source_files:
            if verbose:
                print(f"  [SKIP] domain '{domain.name}' uses existing source files")
            return []

        docs = domain.documents
        if not docs:
            if verbose:
                print(f"  [SKIP] domain '{domain.name}' has no documents defined")
            return []

        if count and count < len(docs):
            docs = docs[:count]

        output_dir = self.docs_base / domain.dir
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        template = self.env.get_template("rule.md.j2")
        generated = []

        for i, doc in enumerate(docs, 1):
            sections = build_sections(doc)

            # 合并域级 + 文档级结构化数据（文档级优先）
            principles = doc.principles or domain.domain_principles
            naming_rules = doc.naming_rules or domain.domain_naming_rules
            conventions = doc.conventions or domain.domain_conventions

            context = {
                "title": doc.title,
                "module_name": domain.name,
                "category": doc.category,
                "version": self.config.version,
                "description": doc.description,
                "sections": sections,
                "principles": principles,
                "naming_rules": naming_rules,
                "good_examples": doc.good_examples,
                "bad_examples": doc.bad_examples,
                "performance_targets": doc.performance_targets,
                "security_notes": doc.security_notes,
                "state_management": doc.state_management,
                "conventions": conventions,
                "related_docs": [],
                "checklist": [
                    f"已阅读并理解「{doc.title}」规范",
                    f"相关代码符合「{doc.title}」规范要求",
                    f"已通过代码审查确认规范符合性",
                ],
                "domain_key": domain.key,
                "date": today_str(),
            }

            rendered = template.render(**context)
            filename = compute_filename(domain, doc)
            filepath = output_dir / filename

            if dry_run:
                print(f"  [DRY-RUN] {filepath.relative_to(self.docs_base.parent)}")
                print(rendered[:200] + "...\n")
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rendered)

            generated.append(str(filepath))

            if verbose:
                print(f"  + [{i}/{len(docs)}] {filename}")

        return generated
