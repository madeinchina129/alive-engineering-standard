"""蓝图生成器 — 从 blueprint/ 配置生成产品/架构/设计文档"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment

from ..models import GeneratorConfig
from ..utils import today_str


class BlueprintGenerator:
    """蓝图生成器 — 生成 PRD、架构设计、ER 图等产品文档"""

    # 蓝图类型映射：类型名 → 模板文件名
    BLUEPRINT_TYPES = {
        "prd": "blueprint/prd.md.j2",
        "architecture": "blueprint/architecture.md.j2",
        "er": "blueprint/er.md.j2",
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
        """生成蓝图文档"""
        blueprint_dir = self.docs_base.parent / "blueprint"
        if not blueprint_dir.exists():
            if verbose:
                print(f"  [SKIP] blueprint directory not found: {blueprint_dir}")
            return []

        generated = []
        for bp_type, _ in self.BLUEPRINT_TYPES.items():
            path = self._generate_type(blueprint_dir, bp_type, dry_run, verbose)
            if path:
                generated.append(path)

        return generated

    def _generate_type(
        self, blueprint_dir: Path, bp_type: str, dry_run: bool, verbose: bool
    ) -> Optional[str]:
        """生成特定类型的蓝图模板实例"""
        template_name = self.BLUEPRINT_TYPES.get(bp_type)
        if template_name not in self.env.list_templates():
            if verbose:
                print(f"  [SKIP] template not found: {template_name}")
            return None

        template = self.env.get_template(template_name)
        context = self._build_context(bp_type)
        rendered = template.render(**context)

        # 输出到 blueprint/{type}/
        output_dir = blueprint_dir / bp_type.replace("_", " ").title()
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"_{bp_type}.generated.md"
        filepath = output_dir / filename

        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(rendered)

        if verbose:
            print(f"  + [Blueprint] {bp_type}/{filename}")

        return str(filepath)

    def _build_context(self, bp_type: str) -> dict:
        """构建蓝图模板上下文"""
        base = {
            "date": today_str(),
            "version": self.config.version,
        }

        contexts = {
            "prd": {
                "title": "产品名称（自动生成）",
                "status": "草稿",
                "owner": "产品经理",
                "created_date": today_str(),
                "background": "请在此描述产品背景和要解决的问题。",
                "goals": ["目标 1：提升用户体验", "目标 2：提高转化率"],
                "north_star_metric": "核心用户指标",
                "metrics": ["指标 1：日活跃用户数", "指标 2：功能使用率"],
                "epics": [
                    {
                        "name": "核心功能",
                        "stories": [
                            {
                                "id": "US-001",
                                "description": "作为用户，我想要...",
                                "priority": "P0",
                                "acceptance_criteria": ["功能正常可用", "错误处理完善"],
                            }
                        ],
                    }
                ],
                "features": [
                    {
                        "id": "F-001",
                        "name": "功能名称",
                        "trigger": "用户操作触发",
                        "precondition": "用户已登录",
                        "main_flow": ["用户进入页面", "系统加载数据", "用户执行操作"],
                    }
                ],
                "non_functional": [
                    {"name": "性能", "value": "响应时间 < 200ms"},
                    {"name": "安全", "value": "数据传输加密"},
                ],
                "constraints": [
                    {"type": "不做", "description": "本次不实现的功能"},
                    {"type": "技术约束", "description": "需兼容现有技术栈"},
                ],
            },
            "architecture": {
                "title": "系统架构",
                "status": "草稿",
                "architect": "系统架构师",
                "context_diagram": '    User["用户"] --> System["本系统"]',
                "container_diagram": '    Web["Vue3 Web"] --> Gateway["API Gateway"]',
                "decisions": [
                    {
                        "title": "技术栈选型",
                        "status": "已接受",
                        "context": "需要确定后端技术栈",
                        "decision": "采用 Spring Boot 3.x",
                        "alternatives": [
                            {"name": "Spring Boot", "chosen": True, "reason": "团队经验丰富"},
                            {"name": "Go", "chosen": False, "reason": "学习成本高"},
                        ],
                        "consequence": "开发效率高，生态成熟",
                    }
                ],
                "modules": [
                    {"name": "API Gateway", "responsibility": "请求路由和认证", "tech_stack": "Spring Cloud Gateway"},
                    {"name": "User Service", "responsibility": "用户管理", "tech_stack": "Spring Boot"},
                ],
                "tech_choices": [
                    {"domain": "编程语言", "selection": "Java", "version": "21", "rationale": "LTS 版本"},
                    {"domain": "框架", "selection": "Spring Boot", "version": "3.2", "rationale": "生态成熟"},
                ],
            },
            "er": {
                "title": "数据模型",
                "er_diagram": '    ENTITY_A ||--o{ ENTITY_B : has',
                "entities": [
                    {
                        "name": "实体 A",
                        "table": "t_entity_a",
                        "fields": [
                            {"name": "id", "type": "UUID", "constraint": "PK", "description": "主键"},
                            {"name": "name", "type": "VARCHAR(255)", "constraint": "NOT NULL", "description": "名称"},
                        ],
                        "indexes": [
                            {"name": "idx_entity_a_name", "columns": "name"},
                        ],
                    }
                ],
                "relationships": [
                    {"entity_a": "实体 A", "type": "1:N", "entity_b": "实体 B", "description": "拥有关系"},
                ],
            },
        }

        ctx = contexts.get(bp_type, {})
        ctx.update(base)
        return ctx
