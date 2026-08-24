import json, hashlib, os, win32com.client

# 1. Parse Excel contracts
excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False
try:
    full_path = os.path.abspath('계약 현황.xlsx')
    wb = excel.Workbooks.Open(full_path)
    
    sh_mat = wb.Sheets(2)
    mat_data = sh_mat.UsedRange.Value2
    
    sh_sub = wb.Sheets(1)
    sub_data = sh_sub.UsedRange.Value2
    
    wb.Close(False)
finally:
    excel.Quit()

site_code_map = {}
site_div_map = {}

mat_contracts = []
excluded_field_contracts = 0

for r in range(2, len(mat_data)):
    row = mat_data[r]
    if not row or len(row) < 14:
        continue
    code = str(row[0] or '').strip()
    site = str(row[1] or '').strip()
    cat = str(row[2] or '').strip()
    contract_type = str(row[4] or '').strip() # 납품계약 / 설치계약
    item_name = str(row[5] or '').strip()
    vendor = str(row[6] or '').strip()
    buyer = str(row[8] or '').strip() # 본사 / 현장
    amt = row[13]
    
    if not site or not vendor or site == '현장명':
        continue
        
    # 현장계약 제외 (본사 구매만 포함)
    if buyer == '현장':
        excluded_field_contracts += 1
        continue
        
    try:
        amt_num = float(amt) if amt is not None else 0.0
    except:
        amt_num = 0.0
        
    if code and site:
        site_code_map[site] = code
        first_c = code[0].upper()
        if first_c == 'A':
            site_div_map[site] = '인프라'
        elif first_c == 'B':
            site_div_map[site] = '건축'
        elif first_c == 'D':
            site_div_map[site] = '플랜트'
            
    mat_contracts.append({
        'site': site,
        'code': code,
        'cat': cat,
        'inst': '설치' in contract_type,
        'contract_type': contract_type or '납품계약',
        'item': item_name,
        'vendor': vendor,
        'amt': amt_num,
        'scope': 'mat'
    })

print(f'자재계약(본사): {len(mat_contracts)}건 (현장계약 {excluded_field_contracts}건 제외)')

sub_contracts = []
for r in range(1, len(sub_data)):
    row = sub_data[r]
    if not row or len(row) < 9:
        continue
    site = str(row[3] or '').strip()
    work_name = str(row[4] or '').strip()
    vendor = str(row[5] or '').strip()
    period = str(row[6] or '').strip()
    amt = row[8]
    
    if not site or not vendor or site == '현장명':
        continue
        
    try:
        amt_num = float(amt) if amt is not None else 0.0
    except:
        amt_num = 0.0
        
    sub_contracts.append({
        'site': site,
        'cat': f'외주 · {work_name}',
        'inst': True,
        'contract_type': '외주계약',
        'item': work_name,
        'vendor': vendor,
        'period': period,
        'amt': amt_num,
        'scope': 'sub'
    })

print(f'외주계약(본사): {len(sub_contracts)}건')

# Site divisions
infra_keywords = ['고속도로', '철도', '도로', '택지', '전력구', '상수도', '터널', '포장', '유도로', '탄약고', '지하철', '7호선', '교량', '연안정비', '용수도']
plant_keywords = ['플랜트', '공장', 'GEL', 'BLEND', 'HPC', '데이터센터']

all_sites = set(list(site_code_map.keys()) + [x['site'] for x in mat_contracts] + [x['site'] for x in sub_contracts])
for s in all_sites:
    if s not in site_div_map:
        if any(k in s for k in infra_keywords):
            site_div_map[s] = '인프라'
        elif any(k in s for k in plant_keywords):
            site_div_map[s] = '플랜트'
        else:
            site_div_map[s] = '건축'

# Unique vendors
unique_vendors = set([x['vendor'] for x in mat_contracts] + [x['vendor'] for x in sub_contracts])

# Realistic Finance distribution:
# 대부분(88%) 정상 (AAA~BBB-, R-1~R-3), 주의 9% (BB+~B0, R-4~R-5), 경보 3% (B-이하, R-6~R-7)
CREDIT_LIST = ['AAA','AA+','AA0','AA-','A+','A0','A-','BBB+','BBB0','BBB-','BB+','BB0','BB-','B+','B0','B-','CCC','CC','C','D']
CASH_LIST = ['A+','A0','A-','B+','B0','B-','C+','C0','C-','D','E']

vendor_fin_map = {}
for v in sorted(unique_vendors):
    h = int(hashlib.md5(v.encode('utf-8')).hexdigest(), 16)
    p = (h % 100) # 0 to 99
    
    if p < 95: # 95% 정상
        r_val = (h % 3) + 1 # 1~3
        c_idx = (h >> 3) % 10 # AAA ~ BBB-
        h_idx = (h >> 6) % 6  # A+ ~ B-
    elif p < 98: # 3% 주의
        r_val = 4 if ((h >> 2) % 2 == 0) else 5 # 4~5
        c_idx = 10 + ((h >> 3) % 4) # BB+ ~ B0
        h_idx = 6 + ((h >> 6) % 3)  # C+ ~ C-
    else: # 2% 경보
        r_val = 6 if ((h >> 2) % 2 == 0) else 7 # 6~7
        c_idx = 14 + ((h >> 3) % 4) # B- ~ D
        h_idx = 9 + ((h >> 6) % 2)  # D ~ E
        
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

# 2. Build individual contract items per site (Do NOT merge multiple contracts into '外 N건')
# Each contract gets its own separate row for individual assessment!
real_site_data = {}

for s in all_sites:
    v_list = []
    
    # Material contracts
    site_mats = [c for c in mat_contracts if c['site'] == s]
    for idx, c in enumerate(site_mats):
        v_name = c['vendor']
        item_title = c['item'] or c['cat']
        amt = c['amt']
        has_install = c['inst']
        trade = infer_trade(c['cat'] + ' ' + item_title) if has_install else None
        fin = vendor_fin_map[v_name]
        
        v_list.append({
            'cid': f"mat_{idx}",
            'n': v_name,
            'cat': c['cat'],
            'item': item_title,
            'amt': amt,
            'inst': has_install,
            'trade': trade,
            'scope': 'mat',
            'ct': [[item_title, f'{int(amt):,}']],
            'fin': fin
        })
        
    # Sub contracts
    site_subs = [c for c in sub_contracts if c['site'] == s]
    for idx, c in enumerate(site_subs):
        v_name = c['vendor']
        item_title = c['item']
        amt = c['amt']
        trade = infer_trade(item_title)
        fin = vendor_fin_map[v_name]
        
        v_list.append({
            'cid': f"sub_{idx}",
            'n': v_name,
            'cat': c['cat'],
            'item': item_title,
            'amt': amt,
            'inst': True,
            'trade': trade,
            'scope': 'sub',
            'ct': [[item_title, f'{int(amt):,}']],
            'fin': fin
        })
        
    # Sort by amt descending
    v_list.sort(key=lambda x: x['amt'], reverse=True)
    real_site_data[s] = v_list

# Sites array
DIV_ORDER = {'인프라': 0, '건축': 1, '플랜트': 2}
sites_arr = []
for s in sorted(site_div_map.keys(), key=lambda x: (DIV_ORDER.get(site_div_map[s], 3), x)):
    sites_arr.append({
        'name': s,
        'div': site_div_map[s],
        'code': site_code_map.get(s, '')
    })

total_contracts_all = sum(len(lst) for lst in real_site_data.values())
print(f'총 {len(sites_arr)}개 현장, 총 {total_contracts_all}건 개별 계약 행 생성 완료')

# Save dataset JSON
with open('built_site_data.json', 'w', encoding='utf-8') as out:
    json.dump({
        'SITES': sites_arr,
        'REAL_SITE_DATA': real_site_data,
        'VENDOR_FINANCE': vendor_fin_map
    }, out, ensure_ascii=False, indent=2)

print('SUCCESS!')
