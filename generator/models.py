"""Pydantic 数据模型 — 域、文档、配置的结构定义"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Principle(BaseModel):
    """核心原则"""

    name: str = ""
    description: str = ""
    example_good: str = ""
    example_bad: str = ""
    example_lang: str = ""


class NamingRule(BaseModel):
    """命名规则"""

    category: str = ""
    pattern: str = ""
    example: str = ""


class CodeExample(BaseModel):
    """代码示例"""

    title: str = ""
    code: str = ""
    lang: str = ""


class PerformanceTarget(BaseModel):
    """性能指标"""

    metric: str = ""
    target: str = ""
    condition: str = ""


class DocumentSection(BaseModel):
    """文档章节 — 包含标题和完整的 Markdown 内容"""

    title: str = ""
    content: str = ""


class Document(BaseModel):
    """单个文档定义"""

    title: str
    category: str = ""
    description: str = ""
    # 自由格式章节
    sections: list[DocumentSection] = Field(default_factory=list)
    # 结构化数据（供模板使用）
    principles: list[Principle] = Field(default_factory=list)
    naming_rules: list[NamingRule] = Field(default_factory=list)
    good_examples: list[CodeExample] = Field(default_factory=list)
    bad_examples: list[CodeExample] = Field(default_factory=list)
    performance_targets: list[PerformanceTarget] = Field(default_factory=list)
    security_notes: str = ""
    state_management: str = ""
    conventions: list[str] = Field(default_factory=list)


class Domain(BaseModel):
    """域定义（如 flutter、api、database）"""

    key: str
    name: str
    dir: str
    prefix: int = 0
    description: str = ""
    documents: list[Document] = Field(default_factory=list)
    source_files: list[str] = Field(default_factory=list)
    # 域级变量（共享给所有文档）
    domain_principles: list[Principle] = Field(default_factory=list)
    domain_naming_rules: list[NamingRule] = Field(default_factory=list)
    domain_conventions: list[str] = Field(default_factory=list)


class DomainRelation(BaseModel):
    """域间依赖关系"""

    source: str = ""
    target: str = ""
    type_label: str = "references"
    description: str = ""


class GeneratorConfig(BaseModel):
    """完整生成器配置"""

    version: str = "1.0"
    base_dir: str = "../docs"
    domains: list[Domain] = Field(default_factory=list)
    relations: list[DomainRelation] = Field(default_factory=list)
