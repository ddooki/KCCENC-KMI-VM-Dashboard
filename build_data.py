import json, hashlib, re

with open('parsed_contracts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

site_div_map = data['site_div_map']
site_code_map = data['site_code_map']
mat_contracts = data['mat_contracts']
sub_contracts = data['sub_contracts']

infra_keywords = ['고속도로', '철도', '도로', '택지', '전력구', '상수도', '터널', '포장', '유도로', '탄약고', '지하철', '7호선', '교량', '연안정비', '용수도']
plant_keywords = ['플랜트', '공장', 'GEL', 'BLEND', 'HPC', '데이터센터']

for s in site_div_map:
    if any(k in s for k in infra_keywords):
        site_div_map[s] = '인프라'
    elif any(k in s for k in plant_keywords):
        site_div_map[s] = '플랜트'

# Group contracts by site -> vendor
site_vendor_contracts = {}
unique_vendors = set()

for c in mat_contracts:
    s = c['site']
    v = c['vendor']
    if not s or not v: continue
    site_vendor_contracts.setdefault(s, {})
    site_vendor_contracts[s].setdefault(v, {'mat_items': [], 'sub_items': [], 'amt': 0.0, 'has_install': False})
    site_vendor_contracts[s][v]['mat_items'].append(c)
    site_vendor_contracts[s][v]['amt'] += c['amt']
    if c['inst']:
        site_vendor_contracts[s][v]['has_install'] = True
    unique_vendors.add(v)

for c in sub_contracts:
    s = c['site']
    v = c['vendor']
    if not s or not v: continue
    site_vendor_contracts.setdefault(s, {})
    site_vendor_contracts[s].setdefault(v, {'mat_items': [], 'sub_items': [], 'amt': 0.0, 'has_install': True})
    site_vendor_contracts[s][v]['sub_items'].append(c)
    site_vendor_contracts[s][v]['amt'] += c['amt']
    unique_vendors.add(v)

# Stable finance generation per vendor
CREDIT_LIST = ['AAA','AA+','AA0','AA-','A+','A0','A-','BBB+','BBB0','BBB-','BB+','BB0','BB-','B+','B0','B-','CCC','CC','C','D']
CASH_LIST = ['A+','A0','A-','B+','B0','B-','C+','C0','C-','D','E']

vendor_fin_map = {}
for v in sorted(unique_vendors):
    h = int(hashlib.md5(v.encode('utf-8')).hexdigest(), 16)
    r_val = (h % 7) + 1 # 1 to 7
    c_idx = (h >> 3) % len(CREDIT_LIST)
    h_idx = (h >> 6) % len(CASH_LIST)
    
    if r_val <= 3:
        c_idx = min(c_idx, 9)
        h_idx = min(h_idx, 5)
    elif r_val >= 6:
        c_idx = max(c_idx, 10)
        h_idx = max(h_idx, 6)
        
    vendor_fin_map[v] = {
        'c': CREDIT_LIST[c_idx],
        'h': CASH_LIST[h_idx],
        'r': r_val
    }

TRADE_KEYWORDS = [
    ('전기', '전기'), ('통신', '통신'), ('컨테이너', '콘테이너'), ('콘테이너', '콘테이너'),
    ('샤워부스', '샤워부스'), ('렌지후드', '렌지후드'), ('보일러', '보일러(관류형)'),
    ('사다리', '사다리'), ('FAN', 'FAN'), ('휀', 'FAN'), ('에어컨', '에어컨(가설용)'),
    ('주차관제', '주차관제,주차유도설비'), ('환기', '지하주차장 환기시스템'), ('출입통제', '출입통제설비'),
    ('도어록', '출입통제설비'), ('건조대', '전동식빨래건조대'), ('위생도기', '위생도기'),
    ('수전', '위생도기'), ('철근콘크리트', '철근콘크리트'), ('토공', '토공구조물공'),
    ('철골', '철골공사'), ('석공사', '석공사'), ('파일', '파일'), ('습식', '습식'),
    ('방수', '방수'), ('도장', '도장'), ('조경', '조경식재'), ('포장', '포장'), ('소방', '기계설비 기타')
]

def infer_trade(text):
    for kw, tr in TRADE_KEYWORDS:
        if kw in text:
            return tr
    return '기계설비 기타'

real_site_data = {}
for s, v_dict in site_vendor_contracts.items():
    v_list = []
    for v_name, info in v_dict.items():
        m_items = info['mat_items']
        s_items = info['sub_items']
        amt = info['amt']
        has_install = info['has_install']
        
        ct_list = []
        for item in m_items:
            it_name = item['item'] or item['cat']
            it_amt = int(item['amt'])
            ct_list.append([it_name, f'{it_amt:,}'])
        for item in s_items:
            it_name = item['item'] or item['cat']
            it_amt = int(item['amt'])
            ct_list.append([it_name, f'{it_amt:,}'])
            
        if s_items and m_items:
            first_name = s_items[0]['item']
            cat = f'외주/자재 · {first_name} 外 {len(ct_list)-1}건' if len(ct_list)>1 else f'외주/자재 · {first_name}'
            scope = 'all'
        elif s_items:
            first_name = s_items[0]['item']
            cat = f'외주 · {first_name}'
            scope = 'sub'
        else:
            cat = m_items[0]['cat']
            scope = 'mat'
            
        trade = infer_trade(cat + ' ' + ' '.join([x[0] for x in ct_list]))
        fin = vendor_fin_map[v_name]
        
        v_list.append({
            'n': v_name,
            'cat': cat,
            'amt': amt,
            'inst': has_install,
            'trade': trade if has_install else None,
            'scope': scope,
            'ct': ct_list,
            'fin': fin
        })
    v_list.sort(key=lambda x: x['amt'], reverse=True)
    real_site_data[s] = v_list

DIV_ORDER = {'인프라': 0, '건축': 1, '플랜트': 2}
sites_arr = []
for s in sorted(site_div_map.keys(), key=lambda x: (DIV_ORDER.get(site_div_map[x], 3), x)):
    sites_arr.append({
        'name': s,
        'div': site_div_map[s],
        'code': site_code_map.get(s, '')
    })

# Convert to JS code string
js_sites = json.dumps(sites_arr, ensure_ascii=False, indent=2)
js_real_data = json.dumps(real_site_data, ensure_ascii=False)

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace SITES and siteVendors logic
pattern = r'(// ══ 현장 마스터 ══[\s\S]*?)(function genSf\(rd,inst\)\{)'
replacement = f'''// ══ 현장 마스터 (실제 계약 현황 59개 현장) ══
const SITES = {js_sites};
const DIVORD = {{인프라:0, 건축:1, 플랜트:2}};

// ══ 실제 계약 데이터 맵 (총 {len(sites_arr)}개 현장, {len(unique_vendors)}개 협력사) ══
const REAL_SITE_DATA = {js_real_data};

function hash(s){{let h=2166136261;for(let i=0;i<s.length;i++){{h^=s.charCodeAt(i);h=Math.imul(h,16777619);}}return h>>>0;}}
function rng(seed){{let a=seed;return()=>{{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}};}}

const cache={{}};
function siteVendors(site){{
  if(cache[site.name]) return cache[site.name];
  const rawList = REAL_SITE_DATA[site.name] || [];
  const rd = rng(hash(site.name));
  const list = rawList.map(base => {{
    const vRd = rng(hash(site.name + "_" + base.n));
    return {{
      ...base,
      sf: genSf(vRd, base.inst),
      r: genR(vRd)
    }};
  }});
  cache[site.name] = list;
  return list;
}}

\\2'''

new_html = re.sub(pattern, replacement, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('SUCCESSFULLY UPDATED index.html WITH REAL DATA!')
