# Phase 1.1 — 生成 21 个缺失的 standards/*.yaml

## 执行命令

在项目根目录运行以下 Python 命令：

```python
python -c "import yaml, re, sys; from pathlib import Path; \
root = Path(r'C:\Users\made1\alive-engineering-standard'); \
c = yaml.safe_load(open(root/'generator'/'config'/'domain.yaml', encoding='utf-8')); \
sd = root/'standards'; \
existing = {f.stem for f in sd.glob('*.yaml') if f.stem != 'domain'}; \
gen = 0; \
to_id = lambda t: re.sub(r'[^a-z0-9_]', '', t.lower().replace(' ','_').replace('/','_').replace('-','_')); \
to_fn = lambda t: re.sub(r'[^a-zA-Z0-9]', '', t.replace(' ','').replace('/','').replace('-','')); \
to_kd = lambda t: re.sub(r'[^a-z0-9-]', '', t.lower().replace(' ','-').replace('/','-')); \
for d in c['domains']: \
  key=d['key']; \
  if key in existing or not d.get('documents'): continue; \
  out = {'domain':{'key':key,'name':d['name'],'dir':d['dir'],'prefix':d.get('prefix',0)},'documents':[]}; \
  for i,doc in enumerate(d['documents'],1): \
    t=doc['title']; tags=[key]; cat=doc.get('category',''); \
    if cat: tags.append(cat.lower().replace('/','').strip()); \
    out['documents'].append({'id':f'{key}.{to_id(t)}','title':t,'priority':'P1', \
      'owner':f'{d[\"name\"]} Team','version':'1.0','filename':to_fn(t), \
      'index':i,'knowledge_dir':f'{key}/{to_kd(t)}/', \
      'description':doc.get('description',''),'tags':tags,'related':[]}); \
  yaml.dump(out, open(sd/f'{key}.yaml','w',encoding='utf-8'), allow_unicode=True, default_flow_style=False, sort_keys=False); \
  gen+=1; print(f'{key}.yaml ({len(out[\"documents\"])} docs)'); \
print(f'Total: {gen}')
```

## 验证

运行后检查：
```
ls -la standards/*.yaml | wc -l  # 应显示 29 文件（8 原有 + 21 新）
```

新生成文件清单：
- product.yaml (5 docs)
- domain.yaml (5 docs)
- capability.yaml (4 docs)
- business.yaml (4 docs)
- workflow.yaml (4 docs)
- event.yaml (5 docs)
- ui.yaml (5 docs)
- api.yaml (5 docs)
- database.yaml (5 docs)
- ai.yaml (5 docs)
- security.yaml (6 docs)
- test.yaml (6 docs)
- deploy.yaml (6 docs)
- template.yaml (3 docs)
- prompt.yaml (3 docs)
- checklist.yaml (4 docs)
- context.yaml (4 docs)
- operation.yaml (4 docs)
- analytics.yaml (5 docs)
- performance.yaml (5 docs)
- compliance.yaml (5 docs)
