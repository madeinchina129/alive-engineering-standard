import yaml, os, sys
from pathlib import Path

BASE = Path("C:/Users/made1/alive-engineering-standard")
STD_DIR = BASE / "standards"
KNOW_DIR = BASE / "knowledge"

# Load custom content
try:
    sys.path.insert(0, str(BASE / "scripts"))
    from knowledge_content import CONTENT
except Exception as e:
    print("Warning: knowledge_content not loaded:", e)
    CONTENT = {}

LANG_EXTS = {
    "flutter": "dart", "vue3": "vue", "springboot": "java",
    "go": "go", "react": "tsx", "rust": "rs", "kotlin": "kt",
    "swift": "swift", "database": "sql", "api": "yaml",
    "deploy": "yaml", "template": "j2",
}
def get_ext(key):
    return LANG_EXTS.get(key, "md")

SKIP = set()

# ── Generic fallback content ──

def gen_overview(title, desc):
    return f"# {title}\n\n## 概述\n{desc}\n\n## 核心原则\n1. 标准化：统一规范，确保团队协作一致\n2. 可维护性：便于长期维护和迭代\n3. 可验证：所有规则可通过流程自动验证\n\n## 适用范围\n适用于所有涉及 {title} 的场景。\n"

def gen_rules(title, _desc):
    return f"# {title} — 规则\n\n## 规则列表\n\n| 规则 | 说明 | 优先级 | 强制 |\n|------|------|--------|------|\n| GEN-001 | 所有实现必须遵循本标准 | P0 | 是 |\n| GEN-002 | 标准应定期审查更新 | P1 | 是 |\n| GEN-003 | 例外需记录并评审 | P2 | 是 |\n\n## 详细说明\n\n### GEN-001（P0）\n所有实现必须遵循本标准。\n\n### GEN-002（P1）\n标准应定期审查和更新。\n\n### GEN-003（P2）\n例外情况需要记录并评审。\n"

def gen_example(title, ext, desc):
    if ext in ("dart","java","go","rs","kt","swift"):
        return f"// {title} — 示例\n// {desc}\n// TODO: 补充具体实现\n"
    elif ext in ("yaml","yml","sql"):
        return f"# {title} — 示例\n# {desc}\n"
    return f"# {title} — 示例\n\n## 场景\n{desc}\n\n## 内容\n```\n具体示例应根据实际场景补充\n```\n"

def gen_faq(title):
    return f"# {title} — FAQ\n\n## Q1: 这个规范适用于哪些场景？\nA: 适用于项目中所有相关场景。\n\n## Q2: 如何更新规范？\nA: 通过 PR 提交变更，经团队评审后更新版本号。\n\n## Q3: 遇到未覆盖的情况？\nA: 与团队讨论后补充规范。\n"

def gen_checklist(title):
    return f"# {title} — 检查清单\n\n- [ ] 实现符合本规范要求\n- [ ] 相关文档已同步更新\n- [ ] 团队成员已了解变更\n- [ ] 单元测试已覆盖\n- [ ] Code Review 已通过\n"

def gen_prompt(title, desc):
    return f"# {title} — AI Prompt\n\n## System Prompt\n你是一个技术专家，精通 {title}。\n\n## User Prompt 模板\n需求：{{requirement}}\n约束：{{constraints}}\n"

# ── Custom content builders ──

def build_custom_files(dest, custom, ext):
    files = {}
    files["overview.md"] = f"# {custom['title']}\n\n## 概述\n{custom['overview']}\n\n## 核心原则\n" + \
        "\n".join(f"{i+1}. {p}" for i,p in enumerate(custom.get('principles',[]))) + \
        "\n\n## 适用范围\n适用于本项目中所有相关场景。\n"

    rules = custom.get("rules", [])
    r_lines = [f"# {custom['title']} — 规则\n\n## 规则列表\n\n| 规则 | 说明 | 优先级 | 强制 |\n|------|------|--------|------|\n"]
    for r in rules:
        r_lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n")
    r_lines.append("\n## 详细说明\n\n")
    for r in rules:
        r_lines.append(f"### {r[0]}（{r[2]}）\n{r[1]}\n\n")
    files["rule.md"] = "".join(r_lines)

    c_ext = custom.get("example_ext", ext)
    files[f"example.{c_ext}"] = custom.get("example_text", "")

    qas = custom.get("faqs", [])
    files["faq.md"] = f"# {custom['title']} — FAQ\n\n" + \
        "\n".join(f"## Q{i+1}: {q}\n{a}\n" for i,(q,a) in enumerate(qas))

    checks = custom.get("checks", ["实现符合规范要求"])
    files["checklist.md"] = f"# {custom['title']} — 检查清单\n\n" + \
        "\n".join(f"- [ ] {c}" for c in checks) + "\n"

    sp = custom.get("prompt_sp", "")
    up = custom.get("prompt_up", "")
    files["prompt.md"] = f"# {custom['title']} — AI Prompt\n\n## System Prompt\n```\n{sp}\n```\n\n## User Prompt 模板\n```\n{up}\n```\n"
    return files

def run(dry_run=False, domain_filter=None, verbose=True):
    std_files = sorted(STD_DIR.glob("*.yaml"))
    total, skipped, created, errors = 0, 0, 0, 0

    for sf in std_files:
        dk = sf.stem
        if dk in SKIP:
            continue
        if domain_filter and dk not in domain_filter:
            continue
        try:
            data = yaml.safe_load(sf.read_text(encoding="utf-8"))
        except Exception as e:
            if verbose: print(f"  [ERR] {sf.name}: {e}")
            errors += 1
            continue
        for doc in data.get("documents", []):
            kdir = doc.get("knowledge_dir","").strip("/")
            if not kdir:
                continue
            total += 1
            dest = KNOW_DIR / kdir
            title = doc.get("title","Untitled")
            desc = doc.get("description","")
            ext = get_ext(dk)
            custom = CONTENT.get(dk, {}).get(kdir + "/", None)

            # Check which files are missing
            if custom:
                c_ext = custom.get("example_ext", ext)
                needed = ["overview.md","rule.md","faq.md","checklist.md","prompt.md",f"example.{c_ext}"]
            else:
                needed = ["overview.md","rule.md","faq.md","checklist.md","prompt.md",f"example.{ext}"]
            missing = [f for f in needed if not (dest / f).exists()]
            if not missing:
                skipped += 1
                continue

            if dry_run:
                if verbose:
                    print(f"  WOULD CREATE: {kdir} ({title})")
                continue

            dest.mkdir(parents=True, exist_ok=True)

            if custom:
                files = build_custom_files(dest, custom, ext)
                for fname, fcontent in files.items():
                    if not (dest / fname).exists():
                        (dest / fname).write_text(fcontent, encoding="utf-8")
                if verbose:
                    print(f"  CUSTOM: {kdir} ({title}): {len(missing)} files")
            else:
                generic = {
                    "overview.md": gen_overview(title, desc),
                    "rule.md": gen_rules(title, desc),
                    f"example.{ext}": gen_example(title, ext, desc),
                    "faq.md": gen_faq(title),
                    "checklist.md": gen_checklist(title),
                    "prompt.md": gen_prompt(title, desc),
                }
                for fname, fcontent in generic.items():
                    if not (dest / fname).exists():
                        (dest / fname).write_text(fcontent, encoding="utf-8")
                if verbose:
                    print(f"  GENERIC: {kdir} ({title}): {len(missing)} files")
            created += 1

    print(f"\n{'='*50}")
    print(f"Total doc slots:    {total}")
    print(f"Already complete:   {skipped}")
    if dry_run:
        print(f"WOULD CREATE:       {total - skipped}")
    else:
        print(f"Created/updated:    {created}")
        empty = total - skipped - created
        if empty > 0:
            print(f"Still incomplete:   {empty}")
    print(f"{'='*50}")
    return total, skipped, created, errors

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--domain", type=str, default=None)
    p.add_argument("--verbose", "-v", action="store_true", default=True)
    p.add_argument("--quiet", "-q", action="store_true")
    a = p.parse_args()
    df = a.domain.split(",") if a.domain else None
    run(dry_run=a.dry_run, domain_filter=df, verbose=a.verbose and not a.quiet)
