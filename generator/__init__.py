# Alive Engineering Standard — Knowledge-Driven Documentation Generator
#
# 从 knowledge/ 知识文件 + standards/ 标准配置 + templates/ 模板组装文档。
# 通过 `python generator/engine.py [domain]` 或 `python -m generator` 运行。

from .engine import KnowledgeEngine, load_standards, list_standards, main

__all__ = [
    "KnowledgeEngine",
    "load_standards",
    "list_standards",
    "main",
]

__version__ = "2.0.0"
