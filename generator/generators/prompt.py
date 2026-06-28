"""Prompt 文档生成器 — 从文档章节内容生成 AI Prompt 文档"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import Domain, GeneratorConfig
from ..utils import build_sections, compute_filename, today_str, get_domain


class PromptGenerator:
    """Prompt 文档生成器"""

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
        """生成 Prompt 文档"""
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

        template = self.env.get_template("prompt.md.j2")
        generated = []

        for i, doc in enumerate(docs, 1):
            sections = build_sections(doc)
            # 从章节内容中提取前 200 字作为 prompt 场景描述
            content_preview = ""
            for sec in sections[:2]:
                clean = sec["content"].strip().replace("\n", " ")[:200]
                if clean:
                    content_preview += f"{sec['title']}：{clean}\n\n"

            prompt_id = f"{domain.key}_{doc.title.lower().replace(' ', '_')}"

            context = {
                "domain": domain.key,
                "prompt_id": prompt_id,
                "title": doc.title,
                "scenario": (
                    f"场景：{domain.name} - {doc.title}\n\n"
                    f"{doc.description}\n\n"
                    f"涉及以下内容：\n{content_preview}"
                    if content_preview
                    else f"场景：{domain.name} - {doc.title}\n\n{doc.description}"
                ),
                "prompt_text": (
                    f"## 角色\n"
                    f"你是一位资深 {domain.name} 工程师。\n\n"
                    f"## 任务\n"
                    f"按照 AES 标准规范，{doc.description}。\n\n"
                    f"## 要求\n"
                    f"1. 严格遵循 {domain.name} 规范\n"
                    f"2. 提供完整的代码示例（如适用）\n"
                    f"3. 包含注释说明关键设计决策\n"
                    f"4. 确保符合企业级质量标准\n\n"
                    f"## 参考规范\n"
                    f"- {doc.title}\n"
                    f"- AES {domain.name} 标准\n\n"
                    f"## 输出格式\n"
                    f"使用 Markdown 格式输出，包含标题、代码块（标注语言）、列表和表格。"
                ),
                "expected_output": (
                    f"一份完整的 {doc.title} 文档，包含：\n\n"
                    f"1. **概述**：说明文档的目的和适用范围\n"
                    f"2. **核心规范**：逐条列出规范细则\n"
                    f"3. **代码示例**：提供规范的正面和反面示例\n"
                    f"4. **检查清单**：规范符合性检查项"
                ),
                "usage_notes": (
                    f"本 Prompt 用于生成或审查 {domain.name} 领域的「{doc.title}」。\n\n"
                    f"**使用前**：确保已阅读 {domain.name} 相关规范文档\n"
                    f"**适用场景**：新模块开发、代码审查、技术方案设计\n"
                    f"**输出验证**：生成结果需对照 AES 检查清单确认"
                ),
            }

            rendered = template.render(**context)
            filename = f"prompt_{compute_filename(domain, doc)}"
            filepath = output_dir / filename

            if not dry_run:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rendered)

            generated.append(str(filepath))
            if verbose:
                print(f"  + [Prompt] {filename}")

        return generated
