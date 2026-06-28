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
"""

import os
import sys
import yaml
import json
import click
from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Optional

# ── 路径 ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_DIR = BASE_DIR / "config"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_BASE = BASE_DIR.parent / "docs"

# ── 全局配置缓存 ────────────────────────────────────
_config: Optional[dict] = None

# ── 模板引擎 ─────────────────────────────────────────
env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=False,
    trim_blocks=True,
)


def load_config() -> dict:
    """加载 domain.yaml 配置"""
    config_path = CONFIG_DIR / "domain.yaml"
    if not config_path.exists():
        click.echo(f"[ERROR] 配置文件不存在: {config_path}", err=True)
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_domain(config: dict, key: str) -> Optional[dict]:
    """按 key 查找域"""
    for domain in config.get("domains", []):
        if domain["key"] == key:
            return domain
    return None


def compute_filename(domain: dict, doc: dict) -> str:
    """计算输出文件名：{prefix}_{key}_{slug}.md"""
    prefix = str(domain.get("prefix", 0)).zfill(2)
    key = domain["key"]
    slug = doc["title"].lower() \
        .replace(" ", "-") \
        .replace("/", "-") \
        .replace("(", "") \
        .replace(")", "")
    return f"{prefix}_{key}_{slug}.md"


def build_sections(doc: dict) -> list:
    """从文档配置生成默认章节内容"""
    title = doc["title"]
    return [
        {
            "title": "目标",
            "content": f"本文档定义「{title}」的标准化规范，确保团队在相关工作中保持一致性和高质量输出。"
        },
        {
            "title": "适用范围",
            "content": "本规范适用于所有涉及该领域的工程活动，包括新功能开发、技术重构、代码审查等环节。"
        },
        {
            "title": "规范细则",
            "content": f"待完善：{title} 的具体规范细则。请根据项目实际情况补充完整。\n\n"
                       f"1. 原则一：保持简洁\n"
                       f"2. 原则二：遵从标准\n"
                       f"3. 原则三：持续改进"
        },
        {
            "title": "违规处理",
            "content": "违反本规范的情况应在代码审查中被标注并修复。累计违规将纳入技术债务跟踪。"
        },
    ]


def generate_domain_docs(
    domain: dict,
    config: dict,
    count: Optional[int] = None,
    dry_run: bool = False,
    verbose: bool = True,
) -> list:
    """
    为指定域生成文档。

    Args:
        domain: domain.yaml 中的域定义
        config: 完整配置（用于读取 version 等）
        count: 生成的文档数量（None=全部）
        dry_run: 仅打印，不写入文件
        verbose: 是否打印详细信息

    Returns:
        生成的文档路径列表
    """
    docs = domain.get("documents", [])
    if not docs:
        if verbose:
            click.echo(f"  [SKIP] domain '{domain['name']}' has no documents defined")
        return []

    # Skip domains with source files (already exist)
    if domain.get("source_files"):
        if verbose:
            click.echo(f"  [SKIP] domain '{domain['name']}' uses existing source files")
        return []

    if count and count < len(docs):
        docs = docs[:count]

    output_dir = DOCS_BASE / domain["dir"]
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    template = env.get_template("rule.md.j2")
    generated = []

    for i, doc in enumerate(docs, 1):
        sections = build_sections(doc)

        context = {
            "title": doc["title"],
            "module_name": domain["name"],
            "category": doc.get("category", ""),
            "version": config.get("version", "1.0"),
            "description": doc.get("description", ""),
            "sections": sections,
            "related_docs": [],
            "checklist": [
                f"已阅读并理解「{doc['title']}」规范",
                f"相关代码符合「{doc['title']}」规范要求",
                f"已通过代码审查确认规范符合性",
            ],
            "date": date.today().isoformat(),
        }

        rendered = template.render(**context)
        filename = compute_filename(domain, doc)
        filepath = output_dir / filename

        if dry_run:
            click.echo(f"  [DRY-RUN] {filepath.relative_to(BASE_DIR.parent)}")
            click.echo(rendered[:200] + "...\n")
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(rendered)

        generated.append(str(filepath))

        if verbose:
            click.echo(f"  + [{i}/{len(docs)}] {filename}")

    return generated


# ── CLI ──────────────────────────────────────────────

@click.command()
@click.option("--domain", "-d", default=None, help="指定域 key（如 flutter、api）")
@click.option("--count", "-c", default=None, type=int, help="生成的文档数量")
@click.option("--all", "-a", "all_flag", is_flag=True, help="生成所有域的文档")
@click.option("--list", "-l", "list_flag", is_flag=True, help="列出可用域")
@click.option("--dry-run", "-n", is_flag=True, help="调试模式，不写入文件")
@click.option("--verbose", "-v", is_flag=True, default=True, help="详细输出")
def main(domain, count, all_flag, list_flag, dry_run, verbose):
    """AES Documentation Generator — 规范文档生成器"""

    global _config
    _config = load_config()

    if list_flag:
        click.echo("\nAvailable Domains:\n")
        for d in _config.get("domains", []):
            docs_count = len(d.get("documents", []))
            has_source = "(source files)" if d.get("source_files") else ""
            click.echo(f"  {d['key']:15s} - {d['name']} ({docs_count} docs) {has_source}")
        click.echo()
        return

    if all_flag:
        click.echo("\nGenerating all domain documents...\n")
        total = 0
        for d in _config.get("domains", []):
            click.echo(f"[{d['key']}] {d['name']}")
            generated = generate_domain_docs(d, _config, count, dry_run, verbose)
            total += len(generated)
            click.echo()
        click.echo(f"Done! Generated {total} documents.")
        return

    if domain:
        d = get_domain(_config, domain)
        if not d:
            click.echo(f"[ERROR] Domain not found: {domain}")
            click.echo("Available domains:")
            for d_ in _config.get("domains", []):
                click.echo(f"  - {d_['key']} ({d_['name']})")
            sys.exit(1)

        click.echo(f"\nGenerating: {d['name']}\n")
        generated = generate_domain_docs(d, _config, count, dry_run, verbose)
        if not dry_run:
            if generated:
                click.echo(f"\nDone. Generated {len(generated)} docs -> docs/{d['dir']}/")
            else:
                click.echo(f"\nNo new documents generated.")
        return

    # Default: show help
    click.echo(__doc__)


if __name__ == "__main__":
    main()
