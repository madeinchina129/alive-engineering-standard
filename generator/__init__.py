# Alive Engineering Standard — Documentation Generator
#
# 从 YAML 配置和 Jinja2 模板自动生成规范文档。
# 支持规则文档、Prompt、检查清单、上下文文档等多种类型。

from .engine import GeneratorEngine
from .config import load_config
from .models import GeneratorConfig, Domain, Document

__all__ = [
    "GeneratorEngine",
    "load_config",
    "GeneratorConfig",
    "Domain",
    "Document",
]

__version__ = "1.0.0"
