"""代码生成器 — 从模板生成 Flutter/Spring Boot/Vue3 源代码"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import GeneratorConfig


class CodeGenerator:
    """代码生成器 — 生成 Flutter、Spring Boot、Vue3 源码"""

    LANGUAGES = {
        "flutter": {
            "templates": {
                "model": "code/flutter/model.dart.j2",
                "service": "code/flutter/service.dart.j2",
            },
            "ext": ".dart",
            "base_dir": "apps/mobile-flutter/lib",
        },
        "spring": {
            "templates": {
                "entity": "code/spring/entity.java.j2",
                "repository": "code/spring/repository.java.j2",
                "service": "code/spring/service.java.j2",
                "controller": "code/spring/controller.java.j2",
            },
            "ext": ".java",
            "base_dir": "backend",
        },
        "vue3": {
            "templates": {
                "page": None,  # TODO: add Vue3 templates
            },
            "ext": ".vue",
            "base_dir": "apps/web-vue3/src",
        },
    }

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
        """生成代码文件"""
        # Default: generate for all languages
        languages = list(self.LANGUAGES.keys())

        # If domain_key is specified, map it to a language
        if domain_key:
            if domain_key in self.LANGUAGES:
                languages = [domain_key]
            else:
                if verbose:
                    print(f"  [SKIP] unknown language: {domain_key}")
                return []

        generated = []
        for lang in languages:
            path = self._generate_language(lang, dry_run, verbose)
            if path:
                generated.extend(path)

        return generated

    def _generate_language(
        self, language: str, dry_run: bool, verbose: bool
    ) -> list[str]:
        """为特定语言生成代码模板"""
        lang_config = self.LANGUAGES.get(language)
        if not lang_config:
            return []

        output_base = self.docs_base.parent / lang_config["base_dir"]
        generated = []

        for template_type, template_path in lang_config["templates"].items():
            if template_path is None:
                continue
            if template_path not in self.env.list_templates():
                continue

            template = self.env.get_template(template_path)
            context = self._build_code_context(language, template_type)
            rendered = template.render(**context)

            # Determine output path
            filename = f"{context['class_name']}{lang_config['ext']}"
            output_dir = self._get_output_dir(output_base, language, template_type)
            if not dry_run:
                output_dir.mkdir(parents=True, exist_ok=True)

            filepath = output_dir / filename
            if not dry_run:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rendered)

            generated.append(str(filepath))
            if verbose:
                print(f"  + [{language}] {template_type}/{filename}")

        return generated

    def _build_code_context(self, language: str, template_type: str) -> dict:
        """构建代码模板上下文"""
        base = {
            "date": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
            "version": self.config.version,
        }

        contexts = {
            "flutter": {
                "model": {
                    "description": "数据模型",
                    "class_name": "ExampleModel",
                    "fields": [
                        {"name": "id", "type": "String"},
                        {"name": "name", "type": "String"},
                        {"name": "createdAt", "type": "DateTime"},
                    ],
                    "has_json": True,
                },
                "service": {
                    "description": "API 服务",
                    "class_name": "ExampleService",
                    "model_name": "ExampleModel",
                    "has_model": True,
                    "has_list": True,
                    "has_detail": True,
                    "has_create": True,
                    "has_update": True,
                    "has_delete": True,
                    "endpoint": "examples",
                },
            },
            "spring": {
                "entity": {
                    "description": "JPA 实体",
                    "class_name": "ExampleEntity",
                    "package": "com.alive.{module}.entity",
                    "table_name": "t_example",
                    "fields": [
                        {"name": "name", "type": "String", "column": "name", "nullable": "false"},
                        {"name": "description", "type": "String", "column": "description", "nullable": "true"},
                    ],
                },
                "repository": {
                    "description": "JPA Repository",
                    "class_name": "ExampleRepository",
                    "package": "com.alive.{module}.repository",
                    "entity_package": "com.alive.{module}.entity",
                    "entity_name": "ExampleEntity",
                    "custom_methods": [],
                },
                "service": {
                    "description": "业务服务",
                    "class_name": "ExampleService",
                    "package": "com.alive.{module}.service",
                    "entity_package": "com.alive.{module}.entity",
                    "entity_name": "ExampleEntity",
                    "repository_package": "com.alive.{module}.repository",
                    "repository_name": "ExampleRepository",
                    "repository_var": "exampleRepository",
                },
                "controller": {
                    "description": "REST 控制器",
                    "class_name": "ExampleController",
                    "package": "com.alive.{module}.controller",
                    "entity_package": "com.alive.{module}.entity",
                    "entity_name": "ExampleEntity",
                    "service_package": "com.alive.{module}.service",
                    "service_name": "ExampleService",
                    "service_var": "exampleService",
                    "endpoint": "examples",
                },
            },
        }

        ctx = contexts.get(language, {}).get(template_type, {})
        ctx.update(base)
        return ctx

    def _get_output_dir(self, base: Path, language: str, template_type: str) -> Path:
        """计算输出目录"""
        dir_map = {
            "flutter": {
                "model": base / "models",
                "service": base / "services",
            },
            "spring": {
                "entity": base / "common" / "src" / "main" / "java" / "com" / "alive" / "common" / "entity",
                "repository": base / "common" / "src" / "main" / "java" / "com" / "alive" / "common" / "repository",
                "service": base / "common" / "src" / "main" / "java" / "com" / "alive" / "common" / "service",
                "controller": base / "common" / "src" / "main" / "java" / "com" / "alive" / "common" / "controller",
            },
        }
        return dir_map.get(language, {}).get(template_type, base)
