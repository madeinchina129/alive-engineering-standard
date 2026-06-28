#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/made1/alive-engineering-standard/scripts')
from knowledge_content import CONTENT

# Compare ai/doc-2/ and ai/llm-prompt-engineering/
d2 = CONTENT['ai']['ai/doc-2/']
llm = CONTENT['ai']['ai/llm-prompt-engineering/']
print('=== ai/doc-2/ (existing YAML doc) ===')
print(f'  title: {d2["title"]}')
print(f'  overview[:100]: {d2["overview"][:100]}')
print(f'  principles: {d2.get("principles", [])}')
print()
print('=== ai/llm-prompt-engineering/ (unused) ===')
print(f'  title: {llm["title"]}')
print(f'  overview[:100]: {llm["overview"][:100]}')
print(f'  principles: {llm.get("principles", [])}')
print()

# Check if these are duplicate topics
print('Assessment: Both are about prompt engineering!')
print('ai/doc-2/ already has prompt engineering content.')
print('ai/llm-prompt-engineering/ is a DUPLICATE topic.')
print()
print('Recommendation: Remove ai/llm-prompt-engineering/ from CONTENT.')
print('No new YAML entry needed for it.')
print()

# Genuinely new topics to add to YAML
genuine = [
    'ai/ai-ethics/',
    'ai/mlops/',
    'ai/model-serving/',
    'ai/training-pipeline/',
    'database/relational-design/',
    'deploy/container-deploy/',
    'test/tdd/',
]
print('=== Genuinely new topics (7) ===')
for k in genuine:
    domain = k.split('/')[0]
    entry = CONTENT[domain][k]
    print(f'  {k} -> "{entry["title"]}"')
