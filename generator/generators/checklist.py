"""检查清单生成器 — 从文档章节内容生成检查清单"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import Domain, GeneratorConfig
from ..utils import build_sections, compute_filename, today_str, get_domain


class ChecklistGenerator:
    """检查清单生成器"""

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
        """生成检查清单文档"""
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

        template = self.env.get_template("checklist.md.j2")
        generated = []

        for i, doc in enumerate(docs, 1):
            sections = build_sections(doc)
            section_titles = [s["title"] for s in sections]

            check_items = {
                "功能完整性": [
                    {"description": f"「{doc.title}」的所有核心规范已实现", "ref": None, "ref_path": ""},
                    {"description": "边界情况和异常流程已处理", "ref": None, "ref_path": ""},
                    {"description": f"涉及的全部章节已覆盖：{'、'.join(section_titles[:4])}", "ref": None, "ref_path": ""},
                ],
                "规范符合性": [
                    {"description": f"实现符合 {doc.title} 规范要求", "ref": doc.title, "ref_path": f"{compute_filename(domain, doc)}"},
                    {"description": f"遵守 {domain.name} 整体架构规范", "ref": f"{domain.name} 架构总览", "ref_path": f"../{domain.dir}/{compute_filename(domain, doc)}"},
                    {"description": "代码命名、格式符合项目标准", "ref": "命名规范", "ref_path": "../00_Project/003_Project_Naming.md"},
                ],
                "代码质量": [
                    {"description": "核心逻辑有单元测试覆盖", "ref": None, "ref_path": ""},
                    {"description": "Widget/组件有交互测试", "ref": None, "ref_path": ""},
                    {"description": "无编译警告和 Lint 错误", "ref": None, "ref_path": ""},
                    {"description": "代码复杂度合理，单文件不超过 400 行", "ref": None, "ref_path": ""},
                ],
                "文档与注释": [
                    {"description": "关键 API 和复杂逻辑有注释", "ref": None, "ref_path": ""},
                    {"description": "README 或相关文档已更新", "ref": None, "ref_path": ""},
                    {"description": "没有遗留 TODO/FIXME", "ref": None, "ref_path": ""},
                ],
            }

            context = {
                "title": doc.title,
                "rule_ref": f"{domain.name}/{doc.title}",
                "description": doc.description,
                "prerequisites": [
                    f"已阅读「{doc.title}」规范文档",
                    "已了解相关技术栈和工具链",
                ],
                "check_items": check_items,
                "today": today_str(),
            }

            rendered = template.render(**context)
            filename = f"checklist_{compute_filename(domain, doc)}"
            filepath = output_dir / filename

            if not dry_run:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rendered)

            generated.append(str(filepath))
            if verbose:
                print(f"  + [Checklist] {filename}")

        return generated
