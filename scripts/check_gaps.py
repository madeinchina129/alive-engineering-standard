#!/usr/bin/env python3
"""Check which CONTENT entries don't have matching knowledge directories."""
import sys, yaml
sys.path.insert(0, 'C:/Users/made1/alive-engineering-standard/scripts')
from knowledge_content import CONTENT
from pathlib import Path

BASE = Path('C:/Users/made1/alive-engineering-standard')
KNOW_DIR = BASE / 'knowledge'
STD_DIR = BASE / 'standards'

# Find all existing knowledge dirs (domain/topic)
existing_dirs = set()
domain_dirs = [d for d in KNOW_DIR.iterdir() if d.is_dir()]
for dd in domain_dirs:
    for t in dd.iterdir():
        if t.is_dir():
            existing_dirs.add(f'{dd.name}/{t.name}')

# Find all CONTENT keys (as domain/topic without trailing /)
content_keys = set()
for domain, topics in CONTENT.items():
    for key in topics:
        clean = key.rstrip('/')
        content_keys.add(clean)

# Find unused content (key exists in CONTENT but no matching dir)
unused = content_keys - existing_dirs
print('=== CONTENT entries without matching knowledge dirs ===')
for k in sorted(unused):
    domain, topic = k.split('/', 1)
    title = CONTENT.get(domain, {}).get(k + '/', {}).get('title', 'N/A')
    print(f'  {k}/ -> "{title}"')

print(f'\n=== Summary ===')
print(f'Total CONTENT entries: {len(content_keys)}')
print(f'Existing knowledge dirs: {len(existing_dirs)}')
print(f'Unused CONTENT entries: {len(unused)}')

# Also show what YAML file would need updating for each unused entry
print('\n=== Which YAML files need updates ===')
for k in sorted(unused):
    domain, topic = k.split('/', 1)
    yaml_path = STD_DIR / f'{domain}.yaml'
    if yaml_path.exists():
        print(f'  {k}/ -> update {domain}.yaml')
    else:
        print(f'  {k}/ -> needs NEW {domain}.yaml')
