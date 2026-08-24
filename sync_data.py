import json, re

with open('built_site_data.json', 'r', encoding='utf-8') as f:
    site_bundle = json.load(f)

js_sites = json.dumps(site_bundle['SITES'], ensure_ascii=False, indent=2)
js_real_data = json.dumps(site_bundle['REAL_SITE_DATA'], ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace REAL_SITE_DATA and SITES
pattern = r'(// ══ 현장 마스터[\s\S]*?)(function hash\(s\))'
replacement = f'''// ══ 현장 마스터 (실제 본사 계약 현황 59개 현장) ══
const SITES = {js_sites};
const DIVORD = {{인프라:0, 건축:1, 플랜트:2}};

// ══ 실제 본사 계약 데이터 맵 (총 59개 현장, 총 1,669건 개별 계약 행) ══
const REAL_SITE_DATA = {js_real_data};

\\2'''

html = re.sub(pattern, replacement, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('SUCCESSFULLY UPDATED REAL_SITE_DATA in index.html!')
