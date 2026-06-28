#!/usr/bin/env python3
"""
Alive Engineering Standard — Documentation Generator
=====================================================
从 YAML 配置和 Jinja2 模板自动生成规范文档。

用法:
    # 生成所有域的所有文档
    python generate_rule.py --all

    # 生成指定域的文档
    python generate_rule.py --domain flutter

    # 生成指定域的前 N 篇文档
    python generate_rule.py --domain flutter --count 3

    # 查看可用域列表
    python generate_rule.py --list

    # 调试模式（不写入文件，只打印）
    python generate_rule.py --domain flutter --dry-run

注意: 这是向后兼容入口点，已重构为 generator 包。
      新用法: python -m generator [options]
"""

import sys
import os

# 确保项目根目录在路径中（使 generator 包可导入）
_pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)
    # 清理可能存在的错误路径
    sys.path = [p for p in sys.path if not p.endswith("generator")]

from generator.cli import cli as main

if __name__ == "__main__":
    main()
