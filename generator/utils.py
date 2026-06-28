"""工具函数 — 文件名计算、章节构建等"""

from datetime import date
from typing import Optional

from .models import Domain, Document


def compute_filename(domain: Domain, doc: Document) -> str:
    """计算输出文件名：{prefix}_{domain_key}_{slug}.md"""
    prefix = str(domain.prefix).zfill(2)
    key = domain.key
    slug = (
        doc.title.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("(", "")
        .replace(")", "")
    )
    return f"{prefix}_{key}_{slug}.md"


def build_sections(doc: Document) -> list[dict]:
    """从文档的 sections 字段构建渲染上下文。

    如果 doc.sections 有内容，按实际数据构建；
    否则 fallback 到 description 生成默认章节。
    """
    title = doc.title
    desc = doc.description or ""

    if doc.sections:
        return [
            {"title": sec.title, "content": sec.content}
            for sec in doc.sections
        ]

    # fallback: 只有 description 时生成最小结构
    return [
        {
            "title": "概述",
            "content": desc if desc else f"本文档定义「{title}」的规范。",
        },
        {
            "title": "规范内容",
            "content": f"详细规范内容待补充。请参考相关领域文档。",
        },
    ]


def today_str() -> str:
    """返回今天的 ISO 日期字符串"""
    return date.today().isoformat()


def get_domain(config, key: str) -> Optional[Domain]:
    """按 key 查找域"""
    for domain in config.domains:
        if domain.key == key:
            return domain
    return None
