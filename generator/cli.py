"""命令行入口 — Click CLI 定义"""

import sys

import click

from .engine import GeneratorEngine
from .settings import GeneratorSettings, SETTINGS_FILENAME


# 全局设置实例
_settings: GeneratorSettings = None  # type: ignore


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--domain", "-d", default=None, help="指定域 key（如 flutter、api）")
@click.option("--count", "-c", default=None, type=int, help="生成的文档数量")
@click.option("--all", "-a", "all_flag", is_flag=True, help="生成所有域的文档")
@click.option("--list", "-l", "list_flag", is_flag=True, help="列出可用域")
@click.option("--dry-run", "-n", is_flag=True, help="调试模式，不写入文件")
@click.option("--verbose", "-v", is_flag=True, default=None, help="详细输出")
@click.option(
    "--type", "-t", "generator_type",
    default=None,
    type=click.Choice(["rule", "prompt", "checklist", "context", "graph", "blueprint", "code"]),
    help="生成器类型（rule、prompt、checklist、context、graph、blueprint、code）",
)
@click.option(
    "--format", "-f", "output_format",
    default=None,
    type=click.Choice(["md", "json"]),
    help="输出格式（md=Markdown 文件, json=JSON manifest）",
)
def cli(ctx, domain, count, all_flag, list_flag, dry_run, verbose, generator_type, output_format):
    """AES Documentation Generator — 规范文档生成器

    从 YAML 配置和 Jinja2 模板自动生成规范文档。

    用法示例:

        # 列出所有可用域
        python -m generator --list

        # 生成指定域的文档
        python -m generator --domain flutter

        # 生成所有域的文档
        python -m generator --all

        # 仅生成前 3 篇文档
        python -m generator --domain api --count 3

        # 调试模式（不写入文件）
        python -m generator --domain flutter --dry-run

        # JSON 输出模式
        python -m generator --domain flutter --format json

        # 初始化配置文件
        python -m generator init
    """
    # 加载持久化设置
    global _settings
    _settings = GeneratorSettings()

    # 使用配置文件中的默认值（CLI 参数优先）
    if generator_type is None:
        generator_type = _settings.default_generator_type
    if output_format is None:
        output_format = _settings.default_output_format
    if verbose is None:
        verbose = _settings.verbose
    else:
        verbose = True

    ctx.ensure_object(dict)
    ctx.obj = {
        "settings": _settings,
        "generator_type": generator_type,
        "output_format": output_format,
        "domain": domain,
        "count": count,
        "all_flag": all_flag,
        "list_flag": list_flag,
        "dry_run": dry_run,
        "verbose": verbose,
    }

    if ctx.invoked_subcommand is None:
        # 没有子命令时执行默认逻辑
        _run_generate(ctx)


def _run_generate(ctx):
    """执行文档生成"""
    params = ctx.obj
    engine = GeneratorEngine()

    if params["list_flag"]:
        click.echo("\nAvailable Domains:\n")
        for d in engine.config.domains:
            docs_count = len(d.documents)
            has_source = " (source files)" if d.source_files else ""
            click.echo(f"  {d.key:15s} - {d.name} ({docs_count} docs){has_source}")
        click.echo()
        return

    if params["all_flag"]:
        generated = engine.generate(
            generator_type=params["generator_type"],
            all_flag=True,
            count=params["count"],
            dry_run=params["dry_run"],
            verbose=params["verbose"],
            output_format=params["output_format"],
        )
        click.echo(f"Done! Generated {len(generated)} documents.")
        return

    if params["domain"]:
        domain_key = params["domain"]
        generator_type = params["generator_type"]

        # 代码生成器使用自己的域映射，跳过标准域验证
        if generator_type == "code":
            generated = engine.generate(
                generator_type=generator_type,
                domain_key=domain_key,
                count=params["count"],
                dry_run=params["dry_run"],
                verbose=params["verbose"],
                output_format=params["output_format"],
            )
            if not params["dry_run"]:
                if generated:
                    click.echo(f"\nDone. Generated {len(generated)} files.")
                else:
                    click.echo(f"\nNo files generated.")
            return

        # 验证域是否存在
        domain_obj = None
        for d in engine.config.domains:
            if d.key == domain_key:
                domain_obj = d
                break

        if not domain_obj:
            click.echo(f"[ERROR] Domain not found: {domain_key}")
            click.echo("Available domains:")
            for d_ in engine.config.domains:
                click.echo(f"  - {d_.key} ({d_.name})")
            sys.exit(1)

        click.echo(f"\nGenerating: {domain_obj.name} (type: {generator_type})\n")
        generated = engine.generate(
            generator_type=generator_type,
            domain_key=domain_key,
            count=params["count"],
            dry_run=params["dry_run"],
            verbose=params["verbose"],
            output_format=params["output_format"],
        )
        if not params["dry_run"]:
            if generated:
                click.echo(f"\nDone. Generated {len(generated)} docs -> docs/{domain_obj.dir}/")
            else:
                click.echo(f"\nNo new documents generated.")
        return

    # 默认：显示帮助
    click.echo(cli.get_help(ctx))


# ── generate 子命令 ──────────────────────────────────

_GENERATOR_TYPES = ["rule", "prompt", "checklist", "context"]

# 领域别名映射（方便输入）
_DOMAIN_ALIASES = {
    "spring": "springboot",
    "sb": "springboot",
    "vue": "vue3",
    "ui": "ui",
    "api": "api",
    "db": "database",
}


def _resolve_domain(domain_key: str) -> str:
    """解析领域别名"""
    return _DOMAIN_ALIASES.get(domain_key, domain_key)


def _generate_domain_all_types(ctx, domain_key: str, dry_run: bool, verbose: bool) -> list[str]:
    """为一个域生成所有类型的文档"""
    domain_key = _resolve_domain(domain_key)
    engine = GeneratorEngine()
    all_files = []
    for gtype in _GENERATOR_TYPES:
        click.echo(f"\n[{gtype}] Generating {domain_key}...")
        files = engine.generate(
            generator_type=gtype,
            domain_key=domain_key,
            count=None,
            dry_run=dry_run,
            verbose=verbose,
        )
        all_files.extend(files)
    click.echo(f"\nDone. Generated {len(all_files)} files for '{domain_key}'.")
    return all_files


@cli.group(invoke_without_command=True)
@click.pass_context
@click.argument("domain", required=False)
@click.option("--dry-run", "-n", is_flag=True, help="调试模式，不写入文件")
@click.option("--verbose", "-v", is_flag=True, default=True, help="详细输出")
def generate(ctx, domain, dry_run, verbose):
    """生成文档
    
    用法:
        python -m generator generate              # 显示帮助
        python -m generator generate all          # 生成全部文档（rule + prompt + checklist + context）
        python -m generator generate flutter      # 生成 Flutter 全部文档类型
        python -m generator generate springboot   # 生成 Spring Boot 全部文档类型
    """
    if ctx.invoked_subcommand is not None:
        return
    if domain is None:
        click.echo(ctx.get_help())
        return
    if domain == "all":
        # 生成所有域的所有类型文档
        engine = GeneratorEngine()
        total = 0
        for gtype in _GENERATOR_TYPES:
            click.echo(f"\n{'='*50}")
            click.echo(f"  Generator: {gtype}")
            click.echo(f"{'='*50}")
            files = engine.generate(
                generator_type=gtype,
                all_flag=True,
                count=None,
                dry_run=dry_run,
                verbose=verbose,
            )
            total += len(files)
        click.echo(f"\n{'='*50}")
        click.echo(f"  TOTAL: {total} files generated.")
        click.echo(f"{'='*50}")
        return
    # 指定域
    _generate_domain_all_types(ctx, domain, dry_run, verbose)


@generate.command()
@click.pass_context
@click.option("--dry-run", "-n", is_flag=True, help="调试模式，不写入文件")
@click.option("--verbose", "-v", is_flag=True, default=True, help="详细输出")
def all(ctx, dry_run, verbose):
    """生成所有域的文档"""
    # 直接调用主 generate 逻辑
    engine = GeneratorEngine()
    total = 0
    for gtype in _GENERATOR_TYPES:
        click.echo(f"\n{'='*50}")
        click.echo(f"  Generator: {gtype}")
        click.echo(f"{'='*50}")
        files = engine.generate(
            generator_type=gtype,
            all_flag=True,
            count=None,
            dry_run=dry_run,
            verbose=verbose,
        )
        total += len(files)
    click.echo(f"\n{'='*50}")
    click.echo(f"  TOTAL: {total} files generated.")
    click.echo(f"{'='*50}")


# ── 原有子命令 ──────────────────────────────────────

@cli.command()
@click.option("--default-type", default="rule", help="默认生成器类型")
@click.option("--default-format", default="md", help="默认输出格式（md/json）")
def init(default_type, default_format):
    """初始化配置文件（generator.json）"""
    settings = GeneratorSettings()
    settings.set("default_generator_type", default_type)
    settings.set("default_output_format", default_format)
    settings.set("verbose", True)
    settings.save()
    click.echo(f"\n[OK] 配置文件已创建: {settings.config_path}")
    click.echo(f"     默认生成器类型: {default_type}")
    click.echo(f"     默认输出格式: {default_format}")


@cli.command()
def config():
    """查看当前配置"""
    settings = GeneratorSettings()
    click.echo(f"\n配置文件路径: {settings.config_path}")
    click.echo(f"配置文件存在: {settings.config_path.exists()}")
    if settings.config_path.exists():
        click.echo(f"\n当前配置:")
        for key, value in settings.to_dict().items():
            click.echo(f"  {key}: {value}")
    else:
        click.echo("  未配置（使用默认值）")


@cli.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
    """设置配置项（例: set default_generator_type prompt）"""
    settings = GeneratorSettings()
    # 尝试转换为适当类型
    if value.lower() in ("true", "false"):
        value = value.lower() == "true"
    elif value.isdigit():
        value = int(value)
    settings.set(key, value)
    settings.save()
    click.echo(f"[OK] {key} = {value}")


def main():
    """主入口点"""
    cli(obj={})


if __name__ == "__main__":
    main()
