"""配置加载 — 从 YAML 文件读取并验证域配置"""

import sys
from pathlib import Path
from typing import Optional

import yaml

from .models import (
    CodeExample,
    Document,
    DocumentSection,
    Domain,
    DomainRelation,
    GeneratorConfig,
    NamingRule,
    PerformanceTarget,
    Principle,
)


def _parse_principles(raw: list) -> list[Principle]:
    return [Principle(**p) for p in raw] if raw else []


def _parse_naming_rules(raw: list) -> list[NamingRule]:
    return [NamingRule(**r) for r in raw] if raw else []


def _parse_code_examples(raw: list) -> list[CodeExample]:
    return [CodeExample(**e) for e in raw] if raw else []


def _parse_performance_targets(raw: list) -> list[PerformanceTarget]:
    return [PerformanceTarget(**t) for t in raw] if raw else []


def load_config(config_path: Optional[Path] = None) -> GeneratorConfig:
    """加载 domain.yaml 配置并验证"""
    if config_path is None:
        config_path = Path(__file__).parent.resolve() / "config" / "domain.yaml"

    if not config_path.exists():
        print(f"[ERROR] 配置文件不存在: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    domains = []
    for d in raw.get("domains", []):
        documents = []
        for doc in d.get("documents", []):
            sections = [
                DocumentSection(title=s.get("title", ""), content=s.get("content", ""))
                for s in doc.get("sections", [])
            ]
            documents.append(
                Document(
                    title=doc["title"],
                    category=doc.get("category", ""),
                    description=doc.get("description", ""),
                    sections=sections,
                    principles=_parse_principles(doc.get("principles")),
                    naming_rules=_parse_naming_rules(doc.get("naming_rules")),
                    good_examples=_parse_code_examples(doc.get("good_examples")),
                    bad_examples=_parse_code_examples(doc.get("bad_examples")),
                    performance_targets=_parse_performance_targets(doc.get("performance_targets")),
                    security_notes=doc.get("security_notes", ""),
                    state_management=doc.get("state_management", ""),
                    conventions=doc.get("conventions", []),
                )
            )
        domains.append(
            Domain(
                key=d["key"],
                name=d["name"],
                dir=d["dir"],
                prefix=d.get("prefix", 0),
                description=d.get("description", ""),
                documents=documents,
                source_files=d.get("source_files", []),
                domain_principles=_parse_principles(d.get("domain_principles")),
                domain_naming_rules=_parse_naming_rules(d.get("domain_naming_rules")),
                domain_conventions=d.get("domain_conventions", []),
            )
        )

    relations = [
        DomainRelation(
            source=r.get("source", ""),
            target=r.get("target", ""),
            type_label=r.get("type", "references"),
            description=r.get("description", ""),
        )
        for r in raw.get("relations", [])
    ]

    return GeneratorConfig(
        version=raw.get("version", "1.0"),
        base_dir=raw.get("base_dir", "../docs"),
        domains=domains,
        relations=relations,
    )
