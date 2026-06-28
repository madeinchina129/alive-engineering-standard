#!/usr/bin/env python3
"""Clean duplicate content entries from knowledge_content.py.

Old unfixed keys (duplicates after key fix) are removed.
Genuinely new topics with no matching YAML dir are kept.
"""
import sys, re
from pathlib import Path

BASE = Path("C:/Users/made1/alive-engineering-standard")
CONTENT_FILE = BASE / "scripts" / "knowledge_content.py"

# ── Keys to REMOVE (old duplicates that don't match any YAML dir) ──
REMOVE_KEYS = {
    # AI duplicates (correct key already exists)
    "ai/ai-safety/",        # dup of ai/ai/
    "ai/ai-agent-design/",  # dup of ai/ai-agent/
    "ai/model-evaluation/", # dup of ai/evaluation/
    "ai/rag-system/",       # dup of ai/rag/

    # API duplicates
    "api/restful-api-design/",  # dup of api/restful-api/
    "api/api-security/",        # dup of api/api/
    "api/api-versioning/",      # dup of api/doc-3/
    "api/api-documentation/",   # dup of api/doc-4/
    "api/graphql-api/",         # dup of api/openapi/

    # Business duplicates
    "business/product-management/",   # dup of business/doc-1/
    "business/business-strategy/",    # dup of business/doc-2/
    "business/requirement-analysis/", # dup of business/doc-3/
    "business/market-research/",      # dup of business/doc-4/
    "business/kpi-dashboard/",        # dup of business/domain-events/
    "business/user-growth/",          # dup of business/state-machine/
    "business/data-driven/",          # dup of business/reporting/
    "business/agile-process/",        # dup of business/audit/
    "business/project-management/",   # dup of business/retry/
    "business/risk-management/",      # dup of business/rule-engine/

    # Database duplicates (keep relational-design as new)
    "database/sql-optimization/",   # dup of database/sql/
    "database/nosql-design/",       # dup of database/sharding/
    "database/data-modeling/",      # dup of database/doc-3/
    "database/migration-strategy/", # dup of database/doc-2/
    "database/backup-recovery/",    # dup of database/backup/
    "database/data-warehouse/",     # dup of database/doc-5/

    # Deploy duplicates (keep container-deploy as new)
    "deploy/ci-cd-pipeline/",        # dup of deploy/doc-2/
    "deploy/environment-management/",# dup of deploy/doc-5/
    "deploy/kubernetes/",            # dup of deploy/doc-4/
    "deploy/monitoring-alerting/",   # dup of deploy/iac/
    "deploy/rollback-strategy/",     # dup of deploy/doc-3/

    # Test duplicates (keep tdd as new)
    "test/unit-testing/",        # dup of test/doc-2/
    "test/integration-testing/", # dup of test/doc-3/
    "test/e2e-testing/",         # dup of test/e-e/
    "test/performance-testing/", # dup of test/doc-5/
    "test/test-automation/",     # dup of test/doc-6/
}

# ── Read knowledge_content.py ──
with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the CONTENT dict
exec_vars = {}
exec(compile(content, CONTENT_FILE, 'exec'), {}, exec_vars)
old_cont = dict(exec_vars.get('CONTENT', {}))

removed_counts = {}
for domain, topics in list(old_cont.items()):
    removed = 0
    for key in list(topics.keys()):
        if key in REMOVE_KEYS:
            del topics[key]
            removed += 1
    if removed:
        removed_counts[domain] = removed
        print(f"  {domain}: removed {removed} duplicates")

# Write back
lines = content.split('\n')
new_lines = []
inside_content = False
content_start = None
content_end = None

# Find CONTENT = { ... } boundaries
# Pattern: look for "CONTENT = {" and track brace depth
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("CONTENT = {"):
        inside_content = True
        content_start = i

if content_start is None:
    print("ERROR: Could not find CONTENT = {")
    sys.exit(1)

# Generate new CONTENT string
import pprint
pp = pprint.PrettyPrinter(indent=2, width=120, compact=False, sort_dicts=False)
cont_str = pp.pformat(old_cont)

# Build the output file
new_file = ''
with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
    new_file = f.read()

# Replace the content dict (from CONTENT = { to the closing })
# Find where CONTENT = { starts
idx = new_file.find('CONTENT = {')
if idx == -1:
    print("ERROR: Could not find CONTENT = {")
    sys.exit(1)

# Find the matching closing brace by tracking depth
brace_depth = 0
content_start_idx = idx
end_idx = -1
for i in range(content_start_idx, len(new_file)):
    c = new_file[i]
    if c == '{':
        brace_depth += 1
    elif c == '}':
        brace_depth -= 1
        if brace_depth == 0:
            end_idx = i + 1
            break

if end_idx == -1:
    print("ERROR: Could not find closing brace of CONTENT dict")
    sys.exit(1)

old_dict_str = new_file[content_start_idx:end_idx]

# Replace it with clean dict
new_dict_str = "CONTENT = " + cont_str

result = new_file[:content_start_idx] + new_dict_str + new_file[end_idx:]

with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nDone! Removed duplicates: {removed_counts}")
print(f"Total removed: {sum(removed_counts.values())}")
