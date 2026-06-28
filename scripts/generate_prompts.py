import re
from pathlib import Path

BASE = Path("C:/Users/made1/alive-engineering-standard")
PROMPTS_DIR = BASE / "prompts"

PROMPTS = {
    "code-review": [
        "代码安全审查：检查常见安全漏洞",
        "代码性能审查：识别性能瓶颈",
        "代码风格审查：检查编码规范",
        "API 设计审查：检查 API 设计规范",
        "并发安全审查：检查竞态条件",
        "异常处理审查：检查异常处理",
        "日志审查：检查日志规范",
        "依赖审查：检查第三方依赖",
        "测试覆盖审查：检查测试覆盖",
        "架构一致性审查：检查架构一致性",
    ],
    "architecture": [
        "微服务拆分设计：设计微服务边界",
        "分层架构设计：设计层级结构",
        "事件驱动架构：设计事件方案",
        "CQRS 模式设计：设计 CQRS 方案",
        "领域驱动设计：设计限界上下文",
        "API 网关设计：设计网关方案",
        "数据架构设计：设计数据架构",
        "安全架构设计：设计安全架构",
        "可观测性设计：设计观测方案",
        "灾备架构设计：设计高可用方案",
    ],
    "testing": [
        "单元测试生成：为 Service 层生成测试",
        "集成测试生成：为 API 生成集成测试",
        "E2E 测试生成：生成端到端测试",
        "性能测试生成：生成压力测试",
        "安全测试生成：生成安全测试用例",
        "Mock 数据生成：生成 Mock 数据",
        "边界测试生成：生成边界测试",
        "UI 测试生成：生成前端组件测试",
        "数据库测试生成：生成数据层测试",
        "回归测试选择：选择回归测试范围",
    ],
    "documentation": [
        "API 文档生成：生成 OpenAPI 文档",
        "架构文档生成：生成架构说明",
        "部署文档生成：生成部署手册",
        "用户手册生成：生成使用说明",
        "变更日志生成：生成版本日志",
        "数据库文档生成：生成表结构文档",
        "接口文档生成：生成接口说明",
        "故障处理文档：生成 SOP 文档",
        "环境搭建文档：生成配置指南",
        "迁移指南生成：生成版本迁移指南",
    ],
    "debugging": [
        "异常栈分析：定位异常根因",
        "性能问题诊断：诊断性能瓶颈",
        "内存泄漏分析：定位内存泄漏",
        "网络问题排查：排查网络异常",
        "慢查询分析：分析慢查询",
        "并发问题诊断：诊断死锁",
        "日志分析：分析错误模式",
        "配置问题排查：排查配置错误",
        "环境差异排查：排查环境差异",
        "集成问题诊断：诊断集成失败",
    ],
    "refactoring": [
        "代码重构建议：识别代码坏味道",
        "函数拆分建议：拆分大函数",
        "设计模式引入：推荐设计模式",
        "API 重构建议：优化 API 接口",
        "数据库重构：优化 Schema",
        "模块解耦建议：解耦模块",
        "遗留系统现代化：改造遗留系统",
        "性能重构建议：优化性能",
        "测试重构建议：改进测试",
        "配置重构建议：优化配置",
    ],
    "security": [
        "安全漏洞扫描：扫描安全漏洞",
        "认证方案设计：设计认证方案",
        "授权方案设计：设计权限控制",
        "数据加密方案：设计加密方案",
        "安全配置检查：检查安全配置",
        "API 安全设计：设计 API 安全",
        "前端安全设计：设计前端防护",
        "供应链安全：检查依赖安全",
        "合规性检查：检查合规要求",
        "安全响应计划：设计应急响应",
    ],
    "ui-design": [
        "UI 组件设计：设计可复用组件",
        "页面布局设计：设计页面布局",
        "表单设计：设计输入表单",
        "数据可视化：设计数据图表",
        "移动端适配：设计移动适配",
        "暗黑模式设计：设计深色主题",
        "动效设计：设计界面动效",
        "无障碍设计：设计无障碍界面",
        "设计系统构建：构建设计系统",
        "设计评审：审查设计规范",
    ],
    "api-design": [
        "RESTful API 设计：设计 REST API",
        "GraphQL 设计：设计 GraphQL Schema",
        "API 版本策略：设计版本管理",
        "错误码设计：设计错误码体系",
        "API 分页设计：设计分页方案",
        "API 鉴权设计：设计鉴权方案",
        "API 限流设计：设计限流策略",
        "API 文档生成：生成接口文档",
        "WebSocket 设计：设计实时通信",
        "gRPC 设计：设计 gRPC 接口",
    ],
    "database": [
        "表结构设计：设计关系表结构",
        "索引策略设计：设计索引策略",
        "查询优化：优化 SQL 查询",
        "数据迁移设计：设计迁移方案",
        "分库分表设计：设计分片策略",
        "缓存策略设计：设计缓存方案",
        "备份恢复设计：设计备份方案",
        "数据归档设计：设计归档方案",
        "Sharding 设计：设计分片键",
        "读写分离设计：设计读写分离",
    ],
    "business": [
        "业务建模：业务领域建模",
        "流程设计：设计业务流程",
        "规则定义：定义业务规则",
        "状态机设计：设计状态流转",
        "报表设计：设计业务报表",
        "领域事件设计：设计事件处理",
        "业务策略设计：设计可配置策略",
        "业务异常处理：设计异常处理",
        "审计日志设计：设计审计追踪",
        "合规检查：检查业务合规",
    ],
    "interview": [
        "Java 面试题：Java 核心技术",
        "系统设计面试：系统设计题目",
        "算法面试题：算法数据结构",
        "前端面试题：前端技术题目",
        "数据库面试题：数据库题目",
        "架构师面试题：架构师题目",
        "项目管理面试题：项目管理题目",
        "DevOps 面试题：DevOps 题目",
        "行为面试题：行为情景题",
        "Python 面试题：Python 题目",
    ],
    "learning": [
        "技术概念解释：解释复杂概念",
        "代码教程生成：生成分步教程",
        "学习路径设计：设计学习路线",
        "知识总结：结构化知识总结",
        "实践练习：生成编程练习",
        "技术对比：对比技术优缺点",
        "最佳实践：领域最佳实践",
        "常见错误：常见错误总结",
        "代码示例：功能代码示例",
        "读书笔记：技术书籍笔记",
    ],
    "code-gen": [
        "CRUD 代码生成：生成 CRUD 接口",
        "Service 代码生成：生成服务层",
        "Repository 生成：生成数据访问层",
        "DTO 生成：生成数据传输对象",
        "配置类生成：生成框架配置",
        "Dockerfile 生成：生成容器配置",
        "CI/CD 配置生成：生成流水线",
        "测试桩生成：生成 Mock 代码",
        "错误处理生成：生成错误处理",
        "API 客户端生成：生成调用代码",
    ],
    "meeting": [
        "会议议程生成：生成会议议程",
        "会议纪要生成：生成会议纪要",
        "技术方案评审：评审技术方案",
        "Sprint 计划生成：生成迭代计划",
        "周报生成：根据工作生成周报",
        "项目复盘生成：生成复盘总结",
        "故障复盘生成：生成故障分析",
        "技术分享文案：生成演讲文案",
        "RFC 文档生成：生成 RFC 文档",
        "OKR 制定生成：生成 OKR",
    ],
}

def safe_name(title):
    # Remove colons, replace spaces with hyphens, keep only safe chars
    name = title.split("：")[0].split(":")[0]
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.strip().replace(" ", "-").lower()
    return name[:40]

def generate(dry_run=False, verbose=True):
    created = 0
    for category, titles in PROMPTS.items():
        cat_dir = PROMPTS_DIR / category
        if not dry_run:
            cat_dir.mkdir(parents=True, exist_ok=True)
            # Overview
            overview = f"# {category}\n\n## 分类说明\n\n{category} 分类下的 Prompt 模板，共 {len(titles)} 个。\n\n## 模板列表\n\n"
            for i, t in enumerate(titles, 1):
                overview += f"{i}. {t}\n"
            (cat_dir / "00-overview.md").write_text(overview, encoding="utf-8")

        for i, title in enumerate(titles, 1):
            name = f"{i:02d}-{safe_name(title)}"
            content = f"""# {title}

## 目标
{title}

## System Prompt
你是一个专业的技术专家，精通相关领域的最佳实践。请根据用户的需求提供高质量的回答。

## User Prompt
```
请完成以下任务：
{title}

背景信息：
{{context}}

具体要求：
{{requirements}}
```

## 输出格式
请提供结构化的输出，包含必要的代码示例和详细说明。

## 变量说明
- `{{context}}`: 相关背景信息
- `{{requirements}}`: 具体需求描述

## 使用场景
适用于 {category} 相关工作场景。
"""
            if not dry_run:
                fp = cat_dir / f"{name}.md"
                fp.write_text(content, encoding="utf-8")
            created += 1

    if verbose:
        print(f"{'DRY RUN - ' if dry_run else ''}Generated {created} prompts across {len(PROMPTS)} categories")
    return created

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    generate(dry_run=args.dry_run)
