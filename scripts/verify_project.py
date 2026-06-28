#!/usr/bin/env python3
"""Final verification of YAML vs knowledge dir alignment."""
from pathlib import Path
import yaml

BASE = Path('C:/Users/made1/alive-engineering-standard')

# 1. Check all 31 YAML files and their knowledge_dir coverage
yaml_dirs = {}
yaml_files = sorted(BASE.glob('standards/*.yaml'))
for yf in yaml_files:
    try:
        data = yaml.safe_load(open(yf, encoding='utf-8'))
        domain = data.get('domain', {}).get('key', '')
        for doc in data.get('documents', []):
            kd = doc.get('knowledge_dir', '').rstrip('/')
            if kd:
                yaml_dirs[kd] = {
                    'title': doc.get('title', ''),
                    'file': yf.name,
                    'domain': domain,
                }
    except Exception as e:
        print(f"Error reading {yf}: {e}")

print(f'YAML-defined knowledge dirs: {len(yaml_dirs)}')

# 2. Count actual knowledge directories
actual_dirs = set()
for dd in (BASE / 'knowledge').iterdir():
    if dd.is_dir():
        for t in dd.iterdir():
            if t.is_dir():
                actual_dirs.add(f'{dd.name}/{t.name}')
print(f'Actual knowledge dirs: {len(actual_dirs)}')

# 3. Find mismatches
orphans = actual_dirs - set(yaml_dirs.keys())
missing = set(yaml_dirs.keys()) - actual_dirs

if orphans:
    print(f'\nKnowledge dirs WITHOUT YAML entry ({len(orphans)}):')
    for d in sorted(orphans):
        print(f'  {d}')
if missing:
    print(f'\nYAML entries WITHOUT knowledge dir ({len(missing)}):')
    for d in sorted(missing):
        info = yaml_dirs[d]
        print(f'  {d} [{info["file"]}] - {info["title"]}')
if not orphans and not missing:
    print('\nAll YAML entries match actual knowledge directories!')

# 4. File count consistency
print('\n--- File Count Consistency ---')
inconsistent = []
for dd in (BASE / 'knowledge').iterdir():
    if dd.is_dir():
        for t in dd.iterdir():
            if t.is_dir():
                fc = len(list(t.iterdir()))
                if fc != 6:
                    inconsistent.append(f'{dd.name}/{t.name}: {fc} files')
if inconsistent:
    for i in inconsistent:
        print(f'  WARNING: {i}')
else:
    print(f'All {len(actual_dirs)} dirs have exactly 6 files')

print('\nDone.')
