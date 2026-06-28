#!/usr/bin/env python3
"""Remove ai/llm-prompt-engineering/ duplicate from knowledge_content.py."""
import sys
from pathlib import Path

BASE = Path("C:/Users/made1/alive-engineering-standard")
CONTENT_FILE = BASE / "scripts" / "knowledge_content.py"

with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and remove the ai/llm-prompt-engineering entry
import re

# Pattern: the entire entry line + the complex dict block
# The key is a CONTENT dict entry like: 'ai/llm-prompt-engineering/': { ... },
# We need to find this and remove it

# Strategy: find the start of the entry and track brace depth to find where it ends
start_marker = "'ai/llm-prompt-engineering/'"
idx = content.find(start_marker)
if idx == -1:
    print("ERROR: Could not find ai/llm-prompt-engineering/ in knowledge_content.py")
    sys.exit(1)

# Find the colon after the key
colon_idx = content.find(':', idx)
dict_start = content.find('{', colon_idx)

# Track brace depth to find where this entry ends
depth = 1
end_idx = dict_start + 1
while depth > 0 and end_idx < len(content):
    c = content[end_idx]
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
    end_idx += 1

# The entry goes from idx to end_idx (includes the closing })
# But we also need to remove the preceding line's comma or following comma
# Let's find the start of the line
line_start = content.rfind('\n', 0, idx) + 1
entry_end = end_idx

# Check if there's a comma after the closing brace
if content[end_idx:end_idx+1] == ',':
    entry_end = end_idx + 1

# Remove from line_start to entry_end plus the newline
if content[entry_end:entry_end+1] == '\n':
    entry_end = entry_end + 1

removed_text = content[line_start:entry_end]
result = content[:line_start] + content[entry_end:]
print(f"Removed entry: {removed_text[:80]}...")

with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
    f.write(result)

print("Done. Written back to knowledge_content.py")

# Verify
exec_vars = {}
exec(compile(open(CONTENT_FILE, encoding='utf-8').read(), CONTENT_FILE, 'exec'), {}, exec_vars)
cont = exec_vars.get('CONTENT', {})
print(f"AI entries: {len(cont.get('ai', {}))}")
total = sum(len(t) for t in cont.values())
print(f"Total entries: {total}")
