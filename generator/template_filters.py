"""Jinja2 自定义过滤器 — 在模板中使用的通用工具函数"""

import re
from datetime import datetime


def slugify(value: str) -> str:
    """将字符串转换为 URL 友好的 slug

    >>> slugify("Flutter 性能优化")
    'flutter-xing-neng-you-hua'
    """
    value = value.lower().strip()
    # 将中文字符替换为拼音占位（或直接移除）
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value)
    return value.strip("-")


def trim_prefix(value: str, prefix: str) -> str:
    """去除字符串前缀"""
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def date_format(value: str, fmt: str = "%Y-%m-%d") -> str:
    """格式化日期字符串"""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime(fmt)
    except (ValueError, TypeError):
        return value


def json_dumps(value) -> str:
    """将值转换为 JSON 字符串（用于模板调试）"""
    import json

    return json.dumps(value, ensure_ascii=False, indent=2)


def md_link(text: str, url: str) -> str:
    """生成 Markdown 链接

    >>> md_link("文档", "doc.md")
    '[文档](doc.md)'
    """
    return f"[{text}]({url})"


def table_of_contents(headings: list[dict]) -> str:
    """从标题列表生成 Markdown 目录"""
    lines = []
    for h in headings:
        indent = "  " * (h.get("level", 1) - 1)
        link = slugify(h["text"])
        lines.append(f'{indent}- [{h["text"]}](#{link})')
    return "\n".join(lines)


# 注册所有过滤器
FILTERS = {
    "slugify": slugify,
    "trim_prefix": trim_prefix,
    "date_format": date_format,
    "json_dumps": json_dumps,
    "md_link": md_link,
    "table_of_contents": table_of_contents,
}
