"""知识图谱生成器 — 生成域间关系图和 Mermaid 可视化"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import DomainRelation, GeneratorConfig
from ..utils import today_str


# 关系类型 → 中文标签映射
RELATION_LABELS = {
    "references": "引用",
    "extends": "扩展",
    "depends_on": "依赖",
    "conflicts": "冲突",
}

# 关系类型 → Mermaid 边样式映射
EDGE_STYLES = {
    "references": "-.-->",
    "extends": "-->",
    "depends_on": "==>",
    "conflicts": "-.->",
}


class GraphGenerator:
    """知识图谱生成器 — 分析域间关系并生成可视化图表"""

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
        **kwargs,
    ) -> list[str]:
        """生成知识图谱文档"""
        generated = []

        if all_flag or domain_key is None:
            path = self._generate_full_graph(dry_run, verbose)
            if path:
                generated.append(path)

        if domain_key:
            path = self._generate_domain_graph(domain_key, dry_run, verbose)
            if path:
                generated.append(path)

        return generated

    def _generate_full_graph(self, dry_run: bool, verbose: bool) -> Optional[str]:
        """生成完整域间关系图谱"""
        output_dir = self.docs_base
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        relations_with_labels = self._annotate_relations(self.config.relations)
        mermaid_code = self._build_mermaid_graph()
        stats = {
            "total_domains": len(self.config.domains),
            "total_docs": sum(len(d.documents) for d in self.config.domains),
            "total_relations": len(self.config.relations),
        }

        template = self.env.get_template("graph.md.j2")
        content = template.render(
            title="完整域间关系图谱",
            date=today_str(),
            version=self.config.version,
            mermaid_code=mermaid_code,
            relations=relations_with_labels,
            stats=stats,
        )

        filepath = output_dir / "knowledge-graph.md"
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        if verbose:
            print(f"  + [Graph] knowledge-graph.md")
        return str(filepath)

    def _generate_domain_graph(self, domain_key: str, dry_run: bool, verbose: bool) -> Optional[str]:
        """生成指定域的局部关系图谱"""
        domain = None
        for d in self.config.domains:
            if d.key == domain_key:
                domain = d
                break
        if not domain:
            return None

        output_dir = self.docs_base / domain.dir
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        # 筛选与当前域相关的关系
        related_relations = [
            r for r in self.config.relations
            if r.source == domain_key or r.target == domain_key
        ]
        relations_with_labels = self._annotate_relations(related_relations)
        mermaid_code = self._build_mermaid_graph(domain_key)

        template = self.env.get_template("graph.md.j2")
        content = template.render(
            title=f"{domain.name} — 关系图谱",
            date=today_str(),
            version=self.config.version,
            mermaid_code=mermaid_code,
            relations=relations_with_labels,
            stats=None,
        )

        filepath = output_dir / "domain-graph.md"
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        if verbose:
            print(f"  + [Graph] {domain.key}/domain-graph.md")
        return str(filepath)

    def _annotate_relations(self, relations: list[DomainRelation]) -> list[dict]:
        """为关系添加中文标签"""
        result = []
        for r in relations:
            result.append({
                "source": r.source,
                "target": r.target,
                "type": r.type,
                "type_label": RELATION_LABELS.get(r.type, r.type),
                "description": r.description,
            })
        return result

    def _build_mermaid_graph(self, center_key: Optional[str] = None) -> str:
        """构建 Mermaid.js 关系图代码"""
        lines = ["graph LR"]
        domain_map = {d.key: d for d in self.config.domains}

        for d in self.config.domains:
            if center_key and d.key != center_key:
                has_relation = any(
                    (r.source == center_key and r.target == d.key)
                    or (r.source == d.key and r.target == center_key)
                    for r in self.config.relations
                )
                if not has_relation:
                    continue
            label = d.name[:20]
            lines.append(f'    {d.key}["{label}"]')

        for rel in self.config.relations:
            if center_key and rel.source != center_key and rel.target != center_key:
                continue
            if rel.source not in domain_map or rel.target not in domain_map:
                continue
            edge_style = EDGE_STYLES.get(rel.type, "-.-->")
            lines.append(f'    {rel.source}{edge_style}{rel.target}')

        lines.append("")
        lines.append("    %% 图例")
        lines.append("    %% -->  extends")
        lines.append("    %% -.-->  references")
        lines.append("    %% ==>  depends_on")

        return "\n".join(lines)
