import json

with open('built_site_data.json', 'r', encoding='utf-8') as f:
    site_bundle = json.load(f)

js_sites = json.dumps(site_bundle['SITES'], ensure_ascii=False, indent=2)
js_real_data = json.dumps(site_bundle['REAL_SITE_DATA'], ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>KCC건설 KMI — 협력업체 관리 대시보드</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet" />
<style>
:root {{
  --bg: #0c110e;
  --panel: #131b16;
  --panel-2: #18241d;
  --panel-3: #1f2f26;
  --line: #27382e;
  --line-soft: #1b2820;
  --text: #e8f0eb;
  --text-2: #bad0c2;
  --muted: #728a7c;
  --sage: #8aa67c;
  --sage-glow: #a4c495;
  --sage-deep: #2e4436;
  --sage-dim: #1f2f25;
  --ok: #6f9463;
  --warn: #d9a441;
  --crit: #c25d53;
  --gold: #d9a441;
  --gold-dim: #5a4520;
  --red: #c25d53;
  --red-dim: #542724;
  --sans: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", monospace;
  --radius: 8px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  padding-bottom: 60px;
}}
.wrap {{
  max-width: 1740px;
  margin: 0 auto;
  padding: 24px 28px;
}}

/* Topbar */
.topbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line);
}}
.topbar h1 {{
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ffffff;
}}
.topbar .site {{
  font-size: 15px;
  color: var(--sage);
  font-weight: 700;
  margin-top: 3px;
}}
.crumb a {{
  color: var(--sage-glow);
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}}
.crumb a:hover {{ text-decoration: underline; }}

.scopetabs {{
  display: flex;
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 3px;
}}
.scopetabs button {{
  background: transparent;
  border: 0;
  color: var(--muted);
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 700;
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: .12s;
}}
.scopetabs button.on {{
  background: var(--sage-deep);
  color: #fff;
}}

/* Stat Cards */
.stat-cards {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}}
@media (max-width: 1200px) {{
  .stat-cards {{ grid-template-columns: repeat(2, 1fr); }}
}}
.scard {{
  background: var(--panel);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.scard-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}}
.stitle {{ font-size: 15px; font-weight: 800; color: #fff; }}
.ssub {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}
.scard-total {{
  font-family: var(--mono);
  font-size: 26px;
  font-weight: 800;
  color: var(--text);
  line-height: 1;
}}
.scard-total .unit {{ font-size: 13px; font-weight: 600; color: var(--muted); margin-left: 2px; }}
.scard-badges {{ display: flex; gap: 8px; }}
.sbadge {{
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}}
.sbadge.crit {{ background: rgba(194,93,83,.18); color: var(--red); border: 1px solid var(--red-dim); }}
.sbadge.warn {{ background: rgba(217,164,65,.18); color: var(--gold); border: 1px solid var(--gold-dim); }}
.sbadge.ok {{ background: rgba(111,148,99,.15); color: var(--ok); border: 1px solid var(--sage-deep); }}
.sbadge .num {{ font-family: var(--mono); font-weight: 800; }}

/* 요약 위젯 */
.top-summaries {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 22px;
}}
@media (max-width: 1100px) {{
  .top-summaries {{ grid-template-columns: 1fr; }}
}}
.ts-card {{
  background: var(--panel);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  overflow: hidden;
}}
.ts-head {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 18px;
  background: var(--panel-2);
  border-bottom: 1px solid var(--line-soft);
}}
.ts-head h3 {{ font-size: 15.5px; font-weight: 800; color: #ffffff; }}
.ts-list {{ max-height: none; overflow-y: visible; }}
.ts-item {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  border-bottom: 1px solid var(--line-soft);
  font-size: 13.5px;
  cursor: pointer;
  transition: .12s;
}}
.ts-item:hover {{ background: var(--panel-2); }}
.ts-item:last-child {{ border-bottom: 0; }}
.ts-rank {{
  width: 24px;
  font-family: var(--mono);
  font-weight: 800;
  font-size: 13px;
  color: var(--muted);
}}
.ts-rank.top3 {{ color: var(--gold); }}
.ts-info {{ flex: 1; min-width: 0; padding: 0 12px; }}
.ts-name {{ font-weight: 700; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.ts-sub {{ font-size: 12px; color: var(--muted); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.ts-tri {{ display: flex; gap: 5px; align-items: center; margin-right: 12px; }}
.ts-tag {{ font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 4px; white-space: nowrap; }}
.ts-tag.fin {{ border: 1px solid #3f5570; color: #9bbde3; background: rgba(122,150,190,.12); }}
.ts-tag.resp {{ border: 1px solid var(--sage-deep); color: var(--sage-glow); background: rgba(138,166,124,.12); }}
.ts-tag.safe {{ border: 1px solid var(--gold-dim); color: var(--gold); background: rgba(217,164,65,.12); }}
.ts-tag.crit {{ border-color: var(--red-dim); color: var(--red); background: rgba(194,93,83,.2); }}
.ts-tag.warn {{ border-color: var(--gold-dim); color: var(--gold); background: rgba(217,164,65,.2); }}
.ts-tag.ok {{ border-color: var(--sage-deep); color: var(--ok); background: rgba(111,148,99,.15); }}

/* Sections & Toolbars */
.section {{
  background: var(--panel);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 22px;
}}
.sechead {{
  padding: 14px 18px;
  background: var(--panel-2);
  border-bottom: 1px solid var(--line-soft);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}}
.sechead h2 {{ font-size: 16.5px; font-weight: 800; color: #ffffff; }}
.toolbar {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}

.search-wrap {{ position: relative; display: flex; align-items: center; }}
.search-wrap svg {{ position: absolute; left: 10px; width: 14px; height: 14px; color: var(--muted); }}
.search-input {{
  background: var(--bg);
  border: 1px solid var(--line);
  border-radius: 6px;
  color: var(--text);
  font-family: inherit;
  font-size: 13.5px;
  padding: 6px 10px 6px 30px;
  width: 220px;
  outline: none;
}}
.search-input:focus {{ border-color: var(--sage-glow); }}

.filters {{ display: flex; gap: 4px; }}
.chip {{
  background: var(--bg);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: .12s;
}}
.chip.on {{ background: var(--sage-deep); color: #fff; border-color: var(--sage); }}
.sel-q {{
  background: var(--bg);
  border: 1px solid var(--line);
  border-radius: 6px;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  padding: 5px 10px;
  outline: none;
}}
.btn {{
  background: var(--panel-3);
  border: 1px solid var(--line);
  color: var(--text);
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: .12s;
}}
.btn:hover {{ background: var(--sage-deep); color: #fff; border-color: var(--sage); }}
.btn-primary {{
  background: var(--sage-deep);
  color: #fff;
  border-color: var(--sage);
}}
.btn-primary:hover {{ background: var(--sage); }}

/* Tables */
.tablescroll {{ width: 100%; overflow-x: auto; }}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
  text-align: center;
}}
thead tr.g th {{ background: var(--panel-3); color: var(--text-2); font-weight: 700; padding: 7px 4px; }}
thead tr th {{
  background: var(--panel-2);
  color: var(--muted);
  font-size: 12.5px;
  font-weight: 700;
  padding: 7px 4px;
  border-bottom: 1px solid var(--line);
  white-space: nowrap;
}}
thead th.srt {{ cursor: pointer; user-select: none; }}
thead th.srt:hover {{ color: var(--text); background: var(--panel-3); }}
thead th.srt.act {{ color: var(--sage-glow); }}
.ar {{ font-size: 10px; margin-left: 2px; color: var(--muted); }}
th.act .ar {{ color: var(--sage-glow); }}

/* Header Group Colors */
.grp-fin {{ background: #182230 !important; color: #a4c2e6 !important; border-bottom: 2px solid #3d5a80 !important; }}
.grp-resp {{ background: #1b261c !important; color: #b2d4a5 !important; border-bottom: 2px solid #496b4c !important; }}
.grp-safe {{ background: #292418 !important; color: #e5c37d !important; border-bottom: 2px solid #7d6534 !important; }}

tbody tr {{ border-bottom: 1px solid var(--line-soft); transition: .1s; }}
tbody tr:hover {{ background: rgba(138,166,124,.05); }}
tbody td {{ padding: 8px 4px; vertical-align: middle; }}
.divl {{ border-left: 1px solid var(--line-soft); }}
.num {{ font-family: var(--mono); font-size: 13px; color: var(--text-2); text-align: right; padding-right: 8px !important; }}
.empty {{ padding: 36px 20px; text-align: center; color: var(--muted); font-size: 14px; }}

/* Gapji */
.slink {{ font-weight: 700; font-size: 14.5px; cursor: pointer; color: var(--text); display: block; }}
.slink:hover {{ color: var(--sage-glow); text-decoration: underline; }}
.dvtag {{ display: inline-block; font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }}
.dv-인프라 {{ background: rgba(122,150,190,.14); color: #8fb0d4; border: 1px solid #3f5570; }}
.dv-건축 {{ background: rgba(138,166,124,.14); color: var(--sage); border: 1px solid var(--sage-deep); }}
.dv-플랜트 {{ background: rgba(184,140,200,.13); color: #b78ec8; border: 1px solid #5d4468; }}
.cw {{ font-family: var(--mono); font-size: 13.5px; font-weight: 700; }}
.cw .c {{ color: var(--red); }} .cw .w {{ color: var(--gold); }} .cw .s {{ color: #4d5f54; font-weight: 400; margin: 0 2px; }}
.cw.zero {{ color: #4d5f54; font-weight: 400; }}

/* Vtable - Detail Table (No horizontal scroll!) */
#vtable {{ width: 100%; min-width: 1340px; }}
.vname {{
  font-weight: 700; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 6px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.vname:hover {{ color: var(--sage-glow); }}
.vsub {{ font-size: 12px; color: var(--muted); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.pill {{ font-size: 11px; font-weight: 700; padding: 1px 6px; border-radius: 4px; flex: none; }}
.pill.install {{ background: rgba(217,164,65,.16); color: var(--gold); border: 1px solid var(--gold-dim); }}
.pill.supply {{ background: rgba(138,166,124,.14); color: var(--sage); border: 1px solid var(--sage-deep); }}

/* 현장평가 상시 클릭 셀 */
.cell {{
  width: 28px; height: 26px; margin: 0 auto; border: 1px solid var(--line); border-radius: 4px;
  display: flex; align-items: center; justify-content: center; font-size: 13.5px; font-weight: 800;
  background: var(--panel-2); color: transparent; cursor: pointer; user-select: none; transition: .12s;
}}
.cell:hover {{ border-color: var(--sage-glow); transform: scale(1.1); }}
.cell.lv1 {{ background: rgba(217,164,65,.22); border-color: var(--gold-dim); color: var(--gold); }}
.cell.lv2 {{ background: rgba(194,93,83,.25); border-color: var(--red-dim); color: var(--red); }}

/* 안전평가 넘버패드 인풋 */
.safe-num-input {{
  width: 38px; height: 26px; text-align: center; background: var(--panel-2);
  border: 1px solid var(--line); border-radius: 4px; color: var(--text-2);
  font-family: var(--mono); font-size: 13px; font-weight: 700;
  outline: none; transition: .12s; -moz-appearance: textfield;
}}
.safe-num-input::-webkit-outer-spin-button,
.safe-num-input::-webkit-inner-spin-button {{ margin: 0; }}
.safe-num-input:focus {{
  border-color: var(--gold); color: #fff; background: var(--panel);
  box-shadow: 0 0 6px rgba(217,164,65,.4); transform: scale(1.06);
}}
.safe-num-input.active {{
  background: rgba(217,164,65,.15); border-color: var(--gold-dim); color: var(--gold);
}}

/* Badges & Scores */
.badge {{ display: inline-block; font-size: 12px; font-weight: 700; padding: 2px 7px; border-radius: 4px; white-space: nowrap; }}
.b-ok {{ background: rgba(111,148,99,.16); color: var(--ok); border: 1px solid var(--sage-deep); }}
.b-warn {{ background: rgba(217,164,65,.16); color: var(--gold); border: 1px solid var(--gold-dim); }}
.b-crit {{ background: rgba(194,93,83,.18); color: var(--red); border: 1px solid var(--red-dim); }}
.b-na {{ background: transparent; color: #5d6c63; border: 1px dashed var(--line); }}
.score {{ font-family: var(--mono); font-weight: 800; font-size: 14.5px; }}
.score.ok {{ color: var(--ok); }} .score.warn {{ color: var(--gold); }} .score.crit {{ color: var(--red); }}
.gr {{ font-family: var(--mono); font-size: 13px; font-weight: 700; }}
.gr.ok {{ color: var(--text-2); }} .gr.warn {{ color: var(--gold); }} .gr.crit {{ color: var(--red); }}
.star {{ color: var(--gold); font-weight: 800; }}
.del-btn {{
  background: transparent; border: 0; color: var(--muted); cursor: pointer; font-size: 15px; padding: 2px 6px;
  border-radius: 4px; transition: .1s;
}}
.del-btn:hover {{ color: var(--red); background: rgba(194,93,83,.15); }}

/* Modals */
.modal-overlay {{
  position: fixed; inset: 0; background: rgba(8,12,10,.78); backdrop-filter: blur(5px);
  z-index: 9999; display: none; align-items: center; justify-content: center; padding: 20px;
}}
.modal-overlay.open {{ display: flex; }}
.modal-window {{
  background: var(--panel); border: 1px solid var(--sage-deep); border-radius: 12px;
  width: 100%; max-width: 1240px; max-height: 88vh; display: flex; flex-direction: column;
  box-shadow: 0 16px 48px rgba(0,0,0,.7); overflow: hidden;
}}
.modal-head {{
  padding: 16px 22px; border-bottom: 1px solid var(--line);
  display: flex; justify-content: space-between; align-items: center;
  background: linear-gradient(90deg, rgba(138,166,124,.15), transparent);
}}
.modal-head h3 {{ font-size: 18px; font-weight: 800; color: #fff; }}
.modal-body {{ padding: 16px 22px; overflow-y: auto; flex: 1; }}
.modal-foot {{
  padding: 14px 22px; border-top: 1px solid var(--line);
  display: flex; justify-content: space-between; align-items: center;
}}
.close {{
  background: transparent; border: 1px solid var(--line); color: var(--muted);
  width: 30px; height: 30px; border-radius: 6px; cursor: pointer; font-size: 18px;
}}
.close:hover {{ color: #fff; border-color: var(--sage); }}

/* Detail Drawer */
.detail {{
  background: var(--panel); border: 1px solid var(--sage-deep); border-radius: var(--radius);
  margin-bottom: 18px; overflow: hidden; display: none;
}}
.detail.show {{ display: block; }}
.dhead {{
  padding: 14px 18px; border-bottom: 1px solid var(--line-soft);
  display: flex; justify-content: space-between; align-items: center;
  background: linear-gradient(90deg, rgba(138,166,124,.10), transparent);
}}
.dhead h3 {{ font-size: 18px; font-weight: 800; }}
.dhead .meta {{ font-size: 13px; color: var(--muted); margin-top: 3px; }}
.dbody {{ display: grid; grid-template-columns: 1fr 1.2fr 1fr; }}
@media(max-width: 1100px) {{ .dbody {{ grid-template-columns: 1fr; }} }}
.dcol {{ padding: 16px 18px; border-right: 1px solid var(--line-soft); }}
.dcol:last-child {{ border-right: 0; }}
.dcol h4 {{ font-size: 14px; font-weight: 800; color: var(--sage-glow); margin-bottom: 12px; }}
.qgrid {{ width: 100%; border-collapse: collapse; }}
.qgrid th {{ font-size: 12px; color: var(--muted); padding: 4px; text-align: center; border: 0; }}
.qgrid td {{ padding: 4px; text-align: center; border: 0; }}
.qgrid td.lbl {{ text-align: left; font-size: 12.5px; color: var(--text-2); }}
.mini {{
  width: 25px; height: 22px; border-radius: 4px; border: 1px solid var(--line);
  background: var(--panel-2); display: inline-flex; align-items: center; justify-content: center;
  font-size: 12.5px; font-weight: 800; color: transparent;
}}
.mini.lv1 {{ background: rgba(217,164,65,.2); border-color: var(--gold-dim); color: var(--gold); }}
.mini.lv2 {{ background: rgba(194,93,83,.25); border-color: var(--red-dim); color: var(--red); }}
.kv {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed var(--line-soft); font-size: 13px; }}
.kv:last-child {{ border-bottom: 0; }}
.kv .k {{ color: var(--muted); }}
.kv .v {{ font-family: var(--mono); font-weight: 700; color: var(--text-2); }}
.calcbox {{
  background: var(--panel-2); border: 1px solid var(--line-soft); border-radius: 6px;
  padding: 10px 12px; margin-top: 10px; font-size: 12.5px; color: var(--muted);
}}
.calcbox b {{ color: var(--text-2); }}
.calcbox .res {{ margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--line-soft); color: var(--text); font-weight: 700; }}

/* Page Routing */
.page {{ display: none; }}
.page.on {{ display: block; }}
.ftr {{
  margin-top: 22px; padding-top: 14px; border-top: 1px solid var(--line-soft);
  font-size: 12.5px; color: var(--muted); line-height: 1.8;
}}
</style>
</head>
<body>
<div class="wrap">

<!-- ══════════ 갑지 (전사 현황) ══════════ -->
<div class="page on" id="pgTop">
  <div class="topbar">
    <div>
      <h1>협력업체 관리 대시보드</h1>
      <div class="site">■ 전사 현황</div>
    </div>
    <div class="scopetabs" id="scopeTop">
      <button class="on" data-s="all">종합</button>
      <button data-s="sub">외주</button>
      <button data-s="mat">자재</button>
    </div>
  </div>

  <div class="stat-cards" id="topDonuts"></div>

  <!-- 주요 리스크 요약 위젯 -->
  <div class="top-summaries" id="topSummaries"></div>

  <div class="section" id="gapjiSection">
    <div class="sechead">
      <div style="display:flex;align-items:center;gap:12px">
        <h2>현장별 업체 상태 현황 (전체)</h2>
        <button class="btn" id="toggleGapjiBtn" style="padding:5px 13px;font-size:13px;font-weight:700">전체 리스트 접기 ▲</button>
      </div>
      <div class="toolbar" id="gapjiToolbar">
        <div class="search-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" class="search-input" id="siteSearch" placeholder="현장명 검색..." />
        </div>
        <div class="filters" id="sfilters">
          <button class="chip on" data-f="all">전체</button>
          <button class="chip" data-f="인프라">인프라</button>
          <button class="chip" data-f="건축">건축</button>
          <button class="chip" data-f="플랜트">플랜트</button>
        </div>
        <select class="sel-q" id="qselTop"></select>
      </div>
    </div>
    <div class="tablescroll" id="gapjiWrap">
      <table id="gapji">
        <colgroup>
          <col style="width:88px"><col style="width:auto"><col style="width:85px"><col style="width:115px">
          <col style="width:120px"><col style="width:120px"><col style="width:120px">
          <col style="width:110px"><col style="width:96px">
        </colgroup>
        <thead>
          <tr class="g">
            <th class="srt" data-k="div" rowspan="2">구분<span class="ar">▲▼</span></th>
            <th class="name srt" data-k="name" rowspan="2">현장명<span class="ar">▲▼</span></th>
            <th class="srt" data-k="cnt" rowspan="2">계약수<span class="ar">▲▼</span></th>
            <th class="srt" data-k="amt" rowspan="2">계약금액<span class="ar">▲▼</span></th>
            <th class="grp-fin divl" colspan="1">재무평가</th>
            <th class="grp-resp" colspan="1">현장평가</th>
            <th class="grp-safe" colspan="1">안전평가</th>
            <th class="divl srt" data-k="risk" rowspan="2">위험계약<br>합계<span class="ar">▲▼</span></th>
            <th class="srt" data-k="grade" rowspan="2">현장<br>판정<span class="ar">▲▼</span></th>
          </tr>
          <tr>
            <th class="divl srt" data-k="f">경보 · 주의<span class="ar">▲▼</span></th>
            <th class="srt" data-k="r">경보 · 주의<span class="ar">▲▼</span></th>
            <th class="srt" data-k="s">경보 · 주의<span class="ar">▲▼</span></th>
          </tr>
        </thead>
        <tbody id="gapjiBody"></tbody>
      </table>
    </div>
  </div>

  <div class="ftr">
    현장 판정 — 위험계약(경보) 1건 이상이면 경보, 주의 업체만 있으면 주의, 없으면 정상.<br>
    전사 계약 현황 데이터는 본사 승인 전자계약(외주 926건 + 본사 자재 743건) 기준입니다.
  </div>
</div>

<!-- ══════════ 현장 상세 ══════════ -->
<div class="page" id="pgSite">
  <div class="topbar">
    <div>
      <div class="crumb"><a id="backLink">← 전체리스트 보기</a></div>
      <h1>협력업체 관리 대시보드</h1>
      <div class="site" id="siteName"></div>
    </div>
    <div class="scopetabs" id="scopeSite">
      <button class="on" data-s="all">종합</button>
      <button data-s="sub">외주</button>
      <button data-s="mat">자재</button>
    </div>
  </div>

  <div class="stat-cards" id="donuts"></div>

  <!-- 상세 패널 (드러워) -->
  <div class="detail" id="detail"></div>

  <div class="section">
    <div class="sechead">
      <h2>관리 대상 협력업체 평가 현황</h2>
      <div class="toolbar">
        <div class="search-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" class="search-input" id="vendorSearch" placeholder="업체명, 품목 검색..." />
        </div>
        <select class="sel-q" id="qsel"></select>
        <div class="filters" id="filters">
          <button class="chip on" data-f="all">전체</button>
          <button class="chip" data-f="install">설치계약</button>
          <button class="chip" data-f="supply">납품계약</button>
        </div>
        <button class="btn btn-primary" id="openModalBtn">+ 전체 계약현황 조회 / 추가</button>
      </div>
    </div>
    <div class="tablescroll">
      <table id="vtable">
        <colgroup>
          <col style="width:260px"><col style="width:105px">
          <!-- 재무평가 4열 -->
          <col style="width:60px"><col style="width:70px"><col style="width:60px"><col style="width:75px">
          <!-- 현장평가 7열 (5개 항목 + 점수 + 판정) -->
          <col style="width:58px"><col style="width:50px"><col style="width:58px"><col style="width:58px"><col style="width:68px"><col style="width:60px"><col style="width:75px">
          <!-- 안전평가 8열 -->
          <col style="width:110px"><col style="width:48px"><col style="width:46px"><col style="width:46px"><col style="width:46px"><col style="width:46px"><col style="width:52px"><col style="width:80px">
          <!-- 종합 및 제외 -->
          <col style="width:78px"><col style="width:44px">
        </colgroup>
        <thead>
          <tr class="g">
            <th class="name srt" data-k="name" rowspan="2">협력업체 / 계약품목<span class="ar">▲▼</span></th>
            <th class="srt" data-k="amt" rowspan="2">계약금액<span class="ar">▲▼</span></th>
            <th class="grp-fin divl" colspan="4">재무평가</th>
            <th class="grp-resp divl" colspan="7">현장평가</th>
            <th class="grp-safe divl" colspan="8">안전평가</th>
            <th class="divl srt" data-k="og" rowspan="2">종합<br>판정<span class="ar">▲▼</span></th>
            <th rowspan="2" style="font-size:11px">제외</th>
          </tr>
          <tr>
            <!-- 재무 -->
            <th class="divl srt" data-k="fc">신용<span class="ar">▲▼</span></th>
            <th class="srt" data-k="fh">현금흐름<span class="ar">▲▼</span></th>
            <th class="srt" data-k="fr">R-MIS<span class="ar">▲▼</span></th>
            <th class="srt" data-k="fg">재무판정<span class="ar">▲▼</span></th>
            <!-- 현장 (5개 항목) -->
            <th class="divl srt" data-k="r0">사전협의<span class="ar">▲▼</span></th>
            <th class="srt" data-k="r1">납기<span class="ar">▲▼</span></th>
            <th class="srt" data-k="r2">설계변경<span class="ar">▲▼</span></th>
            <th class="srt" data-k="r3">품질대응<span class="ar">▲▼</span></th>
            <th class="srt" data-k="r4">정산클레임<span class="ar">▲▼</span></th>
            <th class="srt" data-k="sc">지적점수<span class="ar">▲▼</span></th>
            <th class="srt" data-k="rg">현장판정<span class="ar">▲▼</span></th>
            <!-- 안전 (8열) -->
            <th class="divl srt" data-k="trade">공종<span class="ar">▲▼</span></th>
            <th class="srt" data-k="sstd">기준<span class="ar">▲▼</span></th>
            <th class="srt" data-k="sf0">경고<br><span style="font-size:9.5px;color:var(--muted)">1점</span></th>
            <th class="srt" data-k="sf1">배제<br><span style="font-size:9.5px;color:var(--muted)">2점</span></th>
            <th class="srt" data-k="sf2">시정<br><span style="font-size:9.5px;color:var(--muted)">1점</span></th>
            <th class="srt" data-k="sf3">보장<br><span style="font-size:9.5px;color:var(--muted)">2점</span></th>
            <th class="srt" data-k="sp">누적벌점<span class="ar">▲▼</span></th>
            <th class="srt" data-k="sg">제재판정<span class="ar">▲▼</span></th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- ══════════ 전체 계약현황 조회 및 추가 팝업 모달 ══════════ -->
<div class="modal-overlay" id="contractModal">
  <div class="modal-window">
    <div class="modal-head">
      <h3 id="modalTitle">전체 계약현황 조회 / 추가</h3>
      <button class="close" id="closeModal">×</button>
    </div>
    <div style="padding:14px 22px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap">
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" class="search-input" id="modalSearch" placeholder="자재명, 공종, 업체명 검색..." style="width:260px" />
      </div>
      <div class="filters" id="modalFilters">
        <button class="chip on" data-mf="all">전체 계약</button>
        <button class="chip" data-mf="risk">재무 주의/경보</button>
        <button class="chip" data-mf="install">설치계약</button>
        <button class="chip" data-mf="supply">납품계약</button>
      </div>
    </div>
    <div class="modal-body">
      <div class="tablescroll">
        <table id="modalTable">
          <colgroup>
            <col style="width:45px"><col style="width:75px"><col style="width:230px"><col style="width:240px">
            <col style="width:120px"><col style="width:65px"><col style="width:75px"><col style="width:65px"><col style="width:80px">
          </colgroup>
          <thead>
            <tr>
              <th><input type="checkbox" id="modalSelectAll" title="전체 선택" /></th>
              <th>구분</th><th>협력업체명</th><th>계약 품목 / 공종</th><th>계약금액</th>
              <th>신용</th><th>현금흐름</th><th>R-MIS</th><th>재무판정</th>
            </tr>
          </thead>
          <tbody id="modalBody"></tbody>
        </table>
      </div>
    </div>
    <div class="modal-foot">
      <div style="font-size:13px;color:var(--muted)">선택한 계약을 현재 분기(<span id="modalCurQ"></span>) 관리 대상 목록에 추가합니다.</div>
      <div style="display:flex;gap:10px">
        <button class="btn btn-primary" id="addSelectedBtn">선택한 계약 추가하기 (<span id="selCount">0</span>건)</button>
        <button class="btn" id="closeModalBtn">닫기</button>
      </div>
    </div>
  </div>
</div>

</div>

<script>
const QUARTERS = ["25년 4분기", "26년 1분기", "26년 2분기", "26년 3분기"];
const ITEMS = ["사전협의", "납기", "설계변경", "품질대응", "정산·클레임"];
const MARK = ["", "△", "✕"], PT = [0, 1, 3];
const TRADE_STD = {{
  "전기":11, "통신":4, "콘테이너":4, "샤워부스":4, "렌지후드":4,
  "보일러(관류형)":4, "사다리":4, "기계설비 기타":4, "FAN":4, "에어컨(가설용)":4,
  "주차관제,주차유도설비":4, "지하주차장 환기시스템":4, "출입통제설비":4,
  "전동식빨래건조대":4, "위생도기":4, "철근콘크리트":90, "토공구조물공":39,
  "철골공사":32, "석공사":20, "일반건축":20, "토공(건축)":17, "파일":14,
  "습식":13, "방수":7, "도장":10, "조경식재":12, "포장":12
}};
const CREDIT = ["AAA","AA+","AA0","AA-","A+","A0","A-","BBB+","BBB0","BBB-","BB+","BB0","BB-","B+","B0","B-","CCC","CC","C","D"];
const CASH = ["A+","A0","A-","B+","B0","B-","C+","C0","C-","D","E"];
const Z = [0, 0, 0, 0, 0];

// ══ 현장 마스터 (실제 본사 계약 현황 59개 현장) ══
const SITES = {js_sites};
const DIVORD = {{인프라:0, 건축:1, 플랜트:2}};

// ══ 실제 본사 계약 데이터 맵 (총 59개 현장, 총 1,669건 개별 계약 행) ══
const REAL_SITE_DATA = {js_real_data};

function hash(s){{let h=2166136261;for(let i=0;i<s.length;i++){{h^=s.charCodeAt(i);h=Math.imul(h,16777619);}}return h>>>0;}}
function rng(seed){{let a=seed;return()=>{{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}};}}

// ══ 현장별·분기별 관리 대상 계약 풀 (기본값: 공란) ══
const siteManagedMap = {{}};
SITES.forEach(s => {{
  siteManagedMap[s.name] = {{}};
  QUARTERS.forEach(q => {{
    siteManagedMap[s.name][q] = []; // 모든 현장 디폴트 공란
  }});
}});

// 오퍼스 한강 스위첸만 데모 확인용으로 문제 있는 3개 계약을 기본 탑재
if (siteManagedMap["오퍼스 한강 스위첸"]) {{
  const opContracts = REAL_SITE_DATA["오퍼스 한강 스위첸"] || [];
  const riskContracts = opContracts.filter(c => c.fin && (c.fin.r >= 4 || CREDIT.indexOf(c.fin.c) >= CREDIT.indexOf("BB-")));
  QUARTERS.forEach(q => {{
    siteManagedMap["오퍼스 한강 스위첸"][q] = riskContracts.slice(0, 3).map(c => c.cid);
  }});
}}

const evalCache = {{}};
function getEvalData(siteName, c, idx){{
  const key = siteName + "_" + c.cid + "_" + (c.cid || idx);
  if(evalCache[key]) return evalCache[key];
  const vRd = rng(hash(key));
  const obj = {{
    ...c,
    sf: genSf(vRd, c.inst),
    r: genR(vRd)
  }};
  evalCache[key] = obj;
  return obj;
}}

function siteAllVendors(site){{
  const rawList = REAL_SITE_DATA[site.name] || [];
  return rawList.map((c, idx) => getEvalData(site.name, c, idx));
}}

// 현장 상세 페이지에서 관리 중인 업체 목록 반환
function siteManagedVendors(site, q){{
  const cids = (siteManagedMap[site.name] && siteManagedMap[site.name][q]) ? siteManagedMap[site.name][q] : [];
  const all = siteAllVendors(site);
  return all.filter(v => cids.includes(v.cid));
}}

function genSf(rd, inst){{
  if(!inst) return {{경고:0, 배제:0, 시정:0, 보장:0}};
  const p = rd();
  if(p < 0.93) return {{경고:0, 배제:0, 시정:0, 보장:0}};
  if(p < 0.98) return {{경고:1, 배제:0, 시정:0, 보장:0}};
  return {{경고:1+Math.floor(rd()*2), 배제:1, 시정:Math.floor(rd()*2), 보장:0}};
}}

function genR(rd){{
  const o={{}};
  const isProblem = rd() >= 0.92;
  const base = Array.from({{length:5}}, () => {{
    if(!isProblem) return 0;
    const r = rd();
    return r < 0.7 ? 0 : (r < 0.9 ? 1 : 2);
  }});
  QUARTERS.forEach((q, qi) => {{
    o[q] = base.map(b => b === 0 ? (rd()<0.02?1:0) : (qi<1&&rd()<0.4?0:b));
  }});
  return o;
}}

// ══ 판정 ══
const respScore = (v, q) => (v.r && v.r[q]) ? v.r[q].reduce((a,x)=>a+PT[x],0) : 0;
function streaks(v, q){{
  const qi = QUARTERS.indexOf(q), out = [];
  if(qi < 2 || !v.r) return out;
  for(let j=0; j<5; j++){{
    const q0 = QUARTERS[qi], q1 = QUARTERS[qi-1], q2 = QUARTERS[qi-2];
    if(v.r[q0] && v.r[q1] && v.r[q2] && v.r[q0][j]>0 && v.r[q1][j]>0 && v.r[q2][j]>0) out.push(j);
  }}
  return out;
}}
function respGrade(v, q){{
  const s = respScore(v, q);
  return s >= 6 ? "crit" : s >= 3 ? "warn" : (streaks(v, q).length ? "warn" : "ok");
}}
function safety(v){{
  if(!v.inst) return {{na:true}};
  const std = TRADE_STD[v.trade] ?? 4;
  const sf = v.sf || {{경고:0, 배제:0, 시정:0, 보장:0}};
  const p = (sf.경고||0)*1 + (sf.배제||0)*2 + (sf.시정||0)*1 + (sf.보장||0)*2;
  const bans = p > std ? Math.ceil(p/std)-1 : 0;
  return {{na:false, std, p, bans, g:bans>=1?"crit":(p>=std*0.75?"warn":"ok")}};
}}
function finance(v){{
  if(!v.fin) return {{g:"ok", crit:false, warn:false}};
  const ci = CREDIT.indexOf(v.fin.c), hi = CASH.indexOf(v.fin.h), r = v.fin.r;
  const crit = ci >= CREDIT.indexOf("B-") || hi >= CASH.indexOf("D") || r >= 6;
  const warn = ci >= CREDIT.indexOf("BB-") || hi >= CASH.indexOf("C+") || r >= 4;
  return {{g:crit?"crit":warn?"warn":"ok", crit, warn}};
}}
function overall(v, q){{
  const rg = respGrade(v, q);
  const sg = safety(v).na ? "ok" : safety(v).g;
  const fg = finance(v).g;
  if(rg==="crit" || sg==="crit" || fg==="crit") return "crit";
  if(rg==="warn" || sg==="warn" || fg==="warn") return "warn";
  return "ok";
}}

const GN = {{ok:"정상", warn:"주의", crit:"경보"}};
const CLR = {{ok:"#6f9463", warn:"#d9a441", crit:"#c25d53"}};
const won = n => (n/100000000).toFixed(2)+"억";
const wonS = n => n>=1e12 ? (n/1e12).toFixed(2)+"조" : Math.round(n/100000000).toLocaleString()+"억";

// ══ 상태 변수 ══
let curQ = "26년 3분기";
let scopeTop = "all", scope = "all";
let filter = "all", sfilter = "all";
let siteSearchTerm = "", vendorSearchTerm = "", modalSearchTerm = "";
let modalFilter = "all";
let curSite = null, selected = null;
let sortT = {{k:null, d:1}}, sortV = {{k:null, d:1}};

const inScope = (v, sc) => sc==="all" ? true : sc==="sub" ? v.scope==="sub" : v.scope==="mat";

// ══ 통계 카드 ══
function statCard(c, total, label, sub, unit){{
  return `<div class="scard">
    <div class="scard-head">
      <div>
        <div class="stitle">${{label}}</div>
        <div class="ssub">${{sub}}</div>
      </div>
      <div class="scard-total">${{total}}<span class="unit">${{unit}}</span></div>
    </div>
    <div class="scard-badges">
      <span class="sbadge crit">경보 <span class="num">${{c.crit}}</span></span>
      <span class="sbadge warn">주의 <span class="num">${{c.warn}}</span></span>
      <span class="sbadge ok">정상 <span class="num">${{c.ok}}</span></span>
    </div>
  </div>`;
}}
function tally(list, fn){{const c={{ok:0,warn:0,crit:0}};list.forEach(v=>{{const g=fn(v);if(g)c[g]++;}});return c;}}

// ══════════ 갑지 (전사 현황) ══════════
function siteStats(site){{
  const L = siteAllVendors(site).filter(v=>inScope(v,scopeTop));
  const r = tally(L, v=>respGrade(v,curQ));
  const s = tally(L.filter(v=>v.inst), v=>safety(v).g);
  const f = tally(L, v=>finance(v).g);
  const o = tally(L, v=>overall(v,curQ));
  return {{
    site, list:L, cnt:L.length, amt:L.reduce((a,v)=>a+v.amt,0),
    r, s, f, o, risk:o.crit+o.warn, grade:o.crit?"crit":o.warn?"warn":"ok"
  }};
}}

function renderTopSummaries(stats){{
  const topSites = [...stats]
    .sort((a,b)=> (b.o.crit - a.o.crit) || (b.o.warn - a.o.warn) || (b.risk - a.risk) || (b.amt - a.amt))
    .slice(0, 10);

  const allVendors = stats.flatMap(x=> x.list.map(v=> ({{
    ...v,
    siteName: x.site.name,
    siteDiv: x.site.div,
    og: overall(v, curQ),
    fg: finance(v).g,
    rg: respGrade(v, curQ),
    sg: safety(v).na ? "ok" : safety(v).g,
    safeNa: safety(v).na
  }})));

  const GO = {{crit:0, warn:1, ok:2}};
  const topVendors = allVendors
    .sort((a,b)=> GO[a.og] - GO[b.og] || b.amt - a.amt)
    .slice(0, 10);

  const siteItems = topSites.map((x, idx)=>{{
    return `<div class="ts-item" data-site="${{x.site.name}}">
      <span class="ts-rank ${{idx<3?'top3':''}}">${{idx+1}}</span>
      <div class="ts-info">
        <div class="ts-name">${{x.site.name}}</div>
        <div class="ts-sub">${{x.site.div}} · 계약 ${{x.cnt}}건 · ${{wonS(x.amt)}}</div>
      </div>
      <div>
        <span class="badge b-${{x.grade}}">${{GN[x.grade]}}</span>
      </div>
    </div>`;
  }}).join("");

  const vendorItems = topVendors.map((v, idx)=>{{
    return `<div class="ts-item" data-vsite="${{v.siteName}}" data-vn="${{v.n}}">
      <span class="ts-rank ${{idx<3?'top3':''}}">${{idx+1}}</span>
      <div class="ts-info">
        <div class="ts-name">${{v.n}}</div>
        <div class="ts-sub">${{v.siteName}} · ${{v.item || v.cat}}</div>
      </div>
      <div class="ts-tri">
        <span class="ts-tag fin ${{v.fg}}">재무 ${{GN[v.fg]}}</span>
        <span class="ts-tag resp ${{v.rg}}">현장 ${{GN[v.rg]}}</span>
        <span class="ts-tag safe ${{v.safeNa?'ok':v.sg}}">안전 ${{v.safeNa?'—':GN[v.sg]}}</span>
      </div>
      <div>
        <span class="badge b-${{v.og}}">${{GN[v.og]}}</span>
      </div>
    </div>`;
  }}).join("");

  document.getElementById("topSummaries").innerHTML = `
    <div class="ts-card">
      <div class="ts-head">
        <h3>주요 현장 리스크 현황</h3>
        <span style="font-size:12.5px;color:var(--muted)">리스크 집중도 순</span>
      </div>
      <div class="ts-list">${{siteItems || '<div class="empty">위험 현장이 없습니다.</div>'}}</div>
    </div>
    <div class="ts-card">
      <div class="ts-head">
        <h3>중점 모니터링 협력업체</h3>
        <span style="font-size:12.5px;color:var(--muted)">위험도 평가 순</span>
      </div>
      <div class="ts-list">${{vendorItems || '<div class="empty">위험 업체가 없습니다.</div>'}}</div>
    </div>
  `;
}}

function renderTop(){{
  const stats = SITES.map(siteStats).filter(x=>x.cnt>0);
  const sc = {{ok:0, warn:0, crit:0}}; stats.forEach(x=>sc[x.grade]++);
  const all = stats.flatMap(x=>x.list);
  const inst = all.filter(v=>v.inst);

  document.getElementById("topDonuts").innerHTML =
    statCard(sc, stats.length, "종합 판정", `전사 ${{stats.length}}개 현장 · ${{curQ}}`, "현장") +
    statCard(tally(all, v=>finance(v).g), all.length, "재무평가", `전체 ${{all.length}}건 계약 (외부 연동)`, "건") +
    statCard(tally(all, v=>respGrade(v,curQ)), all.length, "현장평가", `전체 ${{all.length}}건 계약 (분기 평가)`, "건") +
    statCard(tally(inst, v=>safety(v).g), inst.length, "안전평가", `설치·외주 ${{inst.length}}건 한정 (벌점제)`, "건");

  renderTopSummaries(stats);

  let rows = stats.filter(x=>{{
    const matchDiv = sfilter==="all" || x.site.div===sfilter;
    const matchSearch = !siteSearchTerm || x.site.name.toLowerCase().includes(siteSearchTerm);
    return matchDiv && matchSearch;
  }});

  const GO = {{crit:0, warn:1, ok:2}};
  const key = {{
    div:x=>DIVORD[x.site.div], name:x=>x.site.name, cnt:x=>x.cnt, amt:x=>x.amt,
    f:x=>x.f.crit*100+x.f.warn, r:x=>x.r.crit*100+x.r.warn, s:x=>x.s.crit*100+x.s.warn,
    risk:x=>x.risk, grade:x=>GO[x.grade]
  }};
  if(sortT.k){{
    const kf = key[sortT.k];
    rows.sort((a,b)=>{{
      const A = kf(a), B = kf(b);
      return (typeof A==="string" ? A.localeCompare(B,"ko") : A-B) * sortT.d;
    }});
  }} else {{
    rows.sort((a,b)=>DIVORD[a.site.div]-DIVORD[b.site.div] || a.site.name.localeCompare(b.site.name,"ko"));
  }}

  const cw = (o) => o.crit+o.warn===0 ? `<span class="cw zero">—</span>`
    : `<span class="cw"><span class="c">${{o.crit}}</span><span class="s">·</span><span class="w">${{o.warn}}</span></span>`;

  document.getElementById("gapjiBody").innerHTML = rows.length ? rows.map(x=>`
    <tr>
      <td><span class="dvtag dv-${{x.site.div}}">${{x.site.div}}</span></td>
      <td class="name"><span class="slink" data-site="${{x.site.name}}">${{x.site.name}}</span></td>
      <td class="num" style="text-align:center;padding-right:6px!important">${{x.cnt}}</td>
      <td class="num">${{wonS(x.amt)}}</td>
      <td class="divl">${{cw(x.f)}}</td><td>${{cw(x.r)}}</td><td>${{cw(x.s)}}</td>
      <td class="divl"><span class="cw ${{x.risk?'':'zero'}}" style="color:${{x.risk?'var(--text)':''}}">${{x.risk||"—"}}</span></td>
      <td><span class="badge b-${{x.grade}}">${{GN[x.grade]}}</span></td>
    </tr>`).join("") : `<tr><td colspan="9" class="empty">해당 조건의 현장이 없습니다.</td></tr>`;
  markSort("#gapji", sortT);
}}

function markSort(sel, st){{
  document.querySelectorAll(sel+" th.srt").forEach(th=>{{
    th.classList.toggle("act", th.dataset.k===st.k);
    const ar = th.querySelector(".ar");
    if(ar) ar.textContent = th.dataset.k===st.k ? (st.d===1?"▲":"▼") : "▲▼";
  }});
}}

// ══════════ 현장 상세 ══════════
const curList = () => curSite ? siteManagedVendors(curSite, curQ).filter(v=>inScope(v,scope)) : [];

function renderDonuts(){{
  const L = curList(), inst = L.filter(v=>v.inst);
  document.getElementById("donuts").innerHTML =
    statCard(tally(L, v=>overall(v,curQ)), L.length, "종합 판정", `관리 대상 ${{L.length}}건 · ${{curQ}}`, "건") +
    statCard(tally(L, v=>finance(v).g), L.length, "재무평가", `관리 대상 ${{L.length}}건`, "건") +
    statCard(tally(L, v=>respGrade(v,curQ)), L.length, "현장평가", `관리 대상 ${{L.length}}건`, "건") +
    statCard(tally(inst, v=>safety(v).g), inst.length, "안전평가", `설치·외주 ${{inst.length}}건`, "건");
}}

function renderTable(){{
  let rows = curList().map((v, idx)=>({{v, g:overall(v,curQ), origIdx: idx}}))
    .filter(o=>{{
      const matchFilter = filter==="all" ? true : filter==="install" ? o.v.inst : !o.v.inst;
      const matchSearch = !vendorSearchTerm || o.v.n.toLowerCase().includes(vendorSearchTerm) || o.v.cat.toLowerCase().includes(vendorSearchTerm) || (o.v.item && o.v.item.toLowerCase().includes(vendorSearchTerm));
      return matchFilter && matchSearch;
    }});

  const GO = {{crit:0, warn:1, ok:2}};
  const key = {{
    name:o=>o.v.n, amt:o=>o.v.amt,
    fc:o=>CREDIT.indexOf(o.v.fin.c), fh:o=>CASH.indexOf(o.v.fin.h), fr:o=>o.v.fin.r, fg:o=>GO[finance(o.v).g],
    r0:o=>o.v.r[curQ][0], r1:o=>o.v.r[curQ][1], r2:o=>o.v.r[curQ][2], r3:o=>o.v.r[curQ][3], r4:o=>o.v.r[curQ][4],
    sc:o=>respScore(o.v,curQ), rg:o=>GO[respGrade(o.v,curQ)],
    trade:o=>o.v.trade||"힣힣힣", sstd:o=>safety(o.v).na?-1:safety(o.v).std,
    sf0:o=>safety(o.v).na?-1:o.v.sf.경고, sf1:o=>safety(o.v).na?-1:o.v.sf.배제, sf2:o=>safety(o.v).na?-1:o.v.sf.시정, sf3:o=>safety(o.v).na?-1:o.v.sf.보장,
    sp:o=>safety(o.v).na?-1:safety(o.v).p, sg:o=>safety(o.v).na?9:GO[safety(o.v).g],
    og:o=>GO[o.g]
  }};

  if(sortV.k){{
    const kf = key[sortV.k];
    rows.sort((a,b)=>{{
      const A = kf(a), B = kf(b);
      return (typeof A==="string" ? A.localeCompare(B,"ko") : A-B) * sortV.d;
    }});
  }} else {{
    rows.sort((a,b)=>GO[a.g]-GO[b.g] || b.v.amt-a.v.amt);
  }}

  const tb = document.getElementById("tbody");
  if(!curList().length){{
    tb.innerHTML = `<tr>
      <td colspan="21" class="empty">
        <div style="font-size:15px;color:var(--text-2);font-weight:700;margin-bottom:6px">현재 분기 등록된 관리 대상 협력업체가 없습니다.</div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:14px">분기별 리스크 점검이 필요한 업체를 전체 계약에서 선택하여 추가하세요.</div>
        <button class="btn btn-primary" onclick="openModal()">+ 전체 계약현황 조회 / 추가</button>
      </td>
    </tr>`;
    markSort("#vtable", sortV);
    return;
  }}

  if(!rows.length){{
    tb.innerHTML = `<tr><td colspan="21" class="empty">검색/필터 조건에 일치하는 업체가 없습니다.</td></tr>`;
    markSort("#vtable", sortV);
    return;
  }}

  const L = curList();
  tb.innerHTML = rows.map(({{v, g, origIdx}})=>{{
    const i = origIdx;
    const sc = respScore(v, curQ), rg = respGrade(v, curQ), st = streaks(v, curQ);
    const s = safety(v), f = finance(v);
    
    const ci = CREDIT.indexOf(v.fin.c), hi = CASH.indexOf(v.fin.h);
    const cg = ci >= CREDIT.indexOf("B-") ? "crit" : ci >= CREDIT.indexOf("BB-") ? "warn" : "ok";
    const hg = hi >= CASH.indexOf("D") ? "crit" : hi >= CASH.indexOf("C+") ? "warn" : "ok";
    const rr = v.fin.r >= 6 ? "crit" : v.fin.r >= 4 ? "warn" : "ok";

    const finCells = `
      <td class="divl"><span class="gr ${{cg}}">${{v.fin.c}}</span></td>
      <td><span class="gr ${{hg}}">${{v.fin.h}}</span></td>
      <td><span class="gr ${{rr}}">R-${{v.fin.r}}</span></td>
      <td><span class="badge b-${{f.g}}">${{GN[f.g]}}</span></td>`;

    const respCells = v.r[curQ].map((x, j)=>
      `<td class="${{j===0?'divl':''}}"><div class="cell ${{x===1?'lv1':x===2?'lv2':''}}" data-v="${{i}}" data-j="${{j}}" title="클릭: 상태 변경 (공란→△→✕)">${{MARK[x]}}</div></td>`).join("");

    const safeCells = s.na
      ? `<td class="divl" colspan="8"><span class="badge b-na">납품계약 · 현장작업 없음 (해당없음)</span></td>`
      : `<td class="divl" style="font-size:11.5px;color:var(--text-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${{v.trade}}</td>
         <td class="num" style="text-align:center;padding-right:4px!important">${{s.std}}</td>
         <td><input type="number" min="0" max="99" class="safe-num-input ${{v.sf.경고>0?'active':''}}" value="${{v.sf.경고}}" data-v="${{i}}" data-sf="경고" title="숫자 직접 입력 가능" /></td>
         <td><input type="number" min="0" max="99" class="safe-num-input ${{v.sf.배제>0?'active':''}}" value="${{v.sf.배제}}" data-v="${{i}}" data-sf="배제" title="숫자 직접 입력 가능" /></td>
         <td><input type="number" min="0" max="99" class="safe-num-input ${{v.sf.시정>0?'active':''}}" value="${{v.sf.시정}}" data-v="${{i}}" data-sf="시정" title="숫자 직접 입력 가능" /></td>
         <td><input type="number" min="0" max="99" class="safe-num-input ${{v.sf.보장>0?'active':''}}" value="${{v.sf.보장}}" data-v="${{i}}" data-sf="보장" title="숫자 직접 입력 가능" /></td>
         <td class="num" style="text-align:center;padding-right:4px!important;color:${{s.p>s.std?'var(--red)':'var(--text-2)'}};font-weight:700">${{s.p}}</td>
         <td>${{s.bans>=1 ? `<span class="badge b-crit">입찰제한 ${{s.bans}}회</span>`
           : s.g==="warn" ? `<span class="badge b-warn">기준 근접</span>` : `<span class="badge b-ok">정상</span>`}}</td>`;

    return `<tr class="${{selected===i?'sel':''}}">
      <td class="name">
        <div class="vname" data-open="${{i}}"><span style="overflow:hidden;text-overflow:ellipsis">${{v.n}}</span>
          <span class="pill ${{v.inst?'install':'supply'}}">${{v.scope==="sub"?"외주":v.inst?"설치":"납품"}}</span></div>
        <div class="vsub">${{v.item || v.cat}}</div></td>
      <td class="num">${{won(v.amt)}}</td>
      ${{finCells}}
      ${{respCells}}
      <td><span class="score ${{rg}}">${{sc}}</span></td>
      <td><span class="badge b-${{rg}}">${{GN[rg]}}${{st.length?'<span class="star">*</span>':''}}</span></td>
      ${{safeCells}}
      <td class="divl"><span class="badge b-${{g}}">${{GN[g]}}</span></td>
      <td><button class="del-btn" data-del="${{v.cid}}" title="관리 목록에서 제외">×</button></td>
    </tr>`;
  }}).join("");
  markSort("#vtable", sortV);
}}

function renderDetail(){{
  const d = document.getElementById("detail");
  const L = curList();
  if(selected===null || !L[selected]){{ d.className = "detail"; d.innerHTML = ""; return; }}
  const v = L[selected], s = safety(v), f = finance(v);
  const sc = respScore(v, curQ), rg = respGrade(v, curQ), st = streaks(v, curQ), g = overall(v, curQ);
  
  const qtable = `<table class="qgrid">
    <tr><th></th>${{QUARTERS.map(q=>`<th style="${{q===curQ?'color:var(--sage-glow)':''}}">${{q}}</th>`).join("")}}</tr>
    ${{ITEMS.map((it,j)=>`<tr class="${{st.includes(j)?'streak':''}}"><td class="lbl">${{it}}${{st.includes(j)?' <span class="star">*3분기 연속</span>':''}}</td>${{
      QUARTERS.map(q=>{{const x=v.r[q][j];return `<td><span class="mini ${{x===1?'lv1':x===2?'lv2':''}}">${{MARK[x]}}</span></td>`;}}).join("")}}</tr>`).join("")}}
    <tr><td class="lbl" style="font-weight:700;padding-top:6px">지적 점수</td>${{
      QUARTERS.map(q=>`<td style="padding-top:6px"><span class="score ${{respGrade(v,q)}}" style="font-size:13px">${{respScore(v,q)}}</span></td>`).join("")}}</tr></table>`;
  
  const safeBlock = s.na
    ? `<p style="font-size:12.5px;color:var(--muted)">납품계약 전용 업체로 현장 작업이 없어 안전 벌점 평가 대상에서 제외됩니다.</p>`
    : `<div class="kv"><span class="k">해당 공종</span><span class="v">${{v.trade}}</span></div>
       <div class="kv"><span class="k">제재기준 벌점</span><span class="v">${{s.std}}점</span></div>
       <div class="kv"><span class="k">경고 (1점)</span><span class="v">${{v.sf.경고}}건 · ${{v.sf.경고}}점</span></div>
       <div class="kv"><span class="k">작업배제 (2점)</span><span class="v">${{v.sf.배제}}건 · ${{v.sf.배제*2}}점</span></div>
       <div class="kv"><span class="k">시정조치 (1점)</span><span class="v">${{v.sf.시정}}건 · ${{v.sf.시정}}점</span></div>
       <div class="kv"><span class="k">안전보장 (2점)</span><span class="v">${{v.sf.보장}}건 · ${{v.sf.보장*2}}점</span></div>
       <div class="calcbox">누적 벌점 <b>${{s.p}}점</b> ÷ 기준 <b>${{s.std}}점</b> = <b>${{(s.p/s.std).toFixed(2)}}배</b>
         <div class="res">${{s.bans>=1 ? `기준 ${{s.bans}}배 초과 → <span style="color:var(--red)">차년도 입찰제한 ${{s.bans}}회</span>`
           : s.g==="warn" ? `기준 미달이나 75% 이상 도달 → <span style="color:var(--gold)">사전 경고 대상</span>` : "기준 이내 → 제재 없음"}}</div></div>`;

  const rr = v.fin.r>=6 ? "위험" : v.fin.r>=4 ? "주의" : "정상";
  d.className = "detail show";
  d.innerHTML = `
  <div class="dhead">
    <div><h3>${{v.n}} <span class="pill ${{v.inst?'install':'supply'}}">${{v.scope==="sub"?"외주계약":v.inst?"설치계약":"납품계약"}}</span></h3>
      <div class="meta">${{v.item || v.cat}} · ${{won(v.amt)}} · ${{curSite.name}} · ${{curQ}}</div></div>
    <div style="display:flex;gap:10px;align-items:center">
      <span class="badge b-${{g}}" style="font-size:13.5px;padding:5px 14px">종합 ${{GN[g]}}</span>
      <button class="close" id="closeD">×</button></div></div>
  <div class="dbody">
    <div class="dcol"><h4>재무평가</h4>
      <div class="kv"><span class="k">신용등급</span><span class="v">${{v.fin.c}}</span></div>
      <div class="kv"><span class="k">현금흐름등급</span><span class="v">${{v.fin.h}}</span></div>
      <div class="kv"><span class="k">R-MIS 등급</span><span class="v">R-${{v.fin.r}} · ${{rr}}</span></div>
      <div class="calcbox">판정 <b>${{GN[f.g]}}</b>
        <div class="res">${{f.crit ? "신용 B- 이하 · 현금흐름 D/E · R-6 이상 중 하나 이상 해당"
          : f.warn ? "신용 BB-~B0 또는 현금흐름 C계열 또는 R-4~R-5" : "3개 등급 모두 기준 이내"}}</div></div></div>
    <div class="dcol"><h4>현장평가</h4>${{qtable}}
      <div class="calcbox">현재 분기 지적 <b>${{sc}}점</b> — ${{GN[rg]}}
        <div class="res">${{st.length ? "동일 항목 3분기 연속 지적 → 자동 주의 승격" : "0~2점 정상 · 3~5점 주의 · 6점 이상 경보"}}</div></div></div>
    <div class="dcol"><h4>안전평가</h4>${{safeBlock}}</div></div>`;
  document.getElementById("closeD").onclick = () => {{ selected = null; renderTable(); renderDetail(); }};
}}

function renderSite(){{ renderDonuts(); renderTable(); renderDetail(); }}

// ══ 모달 팝업: 전체 계약현황 조회 및 선택 추가 ══
function renderModalTable(){{
  if(!curSite) return;
  const allContracts = siteAllVendors(curSite);
  const managedCids = (siteManagedMap[curSite.name] && siteManagedMap[curSite.name][curQ]) ? siteManagedMap[curSite.name][curQ] : [];
  
  document.getElementById("modalTitle").textContent = `[${{curSite.name}}] 전체 계약현황 조회 / 관리 대상 추가 (총 ${{allContracts.length}}건)`;
  document.getElementById("modalCurQ").textContent = curQ;
  
  let rows = allContracts.filter(v=>{{
    const f = finance(v);
    const matchFilter = modalFilter==="all" ? true 
      : modalFilter==="risk" ? f.g!=="ok"
      : modalFilter==="install" ? v.inst : !v.inst;
    const matchSearch = !modalSearchTerm || v.n.toLowerCase().includes(modalSearchTerm) || (v.item && v.item.toLowerCase().includes(modalSearchTerm)) || v.cat.toLowerCase().includes(modalSearchTerm);
    return matchFilter && matchSearch;
  }});

  const tb = document.getElementById("modalBody");
  if(!rows.length){{
    tb.innerHTML = `<tr><td colspan="9" class="empty">해당 조건의 계약이 없습니다.</td></tr>`;
    return;
  }}

  tb.innerHTML = rows.map(v=>{{
    const f = finance(v);
    const isManaged = managedCids.includes(v.cid);
    return `<tr>
      <td><input type="checkbox" class="mchk" data-cid="${{v.cid}}" ${{isManaged ? 'checked' : ''}} /></td>
      <td><span class="pill ${{v.inst?'install':'supply'}}">${{v.scope==="sub"?"외주":v.inst?"설치":"납품"}}</span></td>
      <td style="font-weight:700;text-align:left">${{v.n}}</td>
      <td style="text-align:left;color:var(--text-2)">${{v.item || v.cat}}</td>
      <td class="num">${{won(v.amt)}}</td>
      <td><span class="gr ${{f.crit&&CREDIT.indexOf(v.fin.c)>=CREDIT.indexOf('B-')?'crit':'ok'}}">${{v.fin.c}}</span></td>
      <td><span class="gr ${{f.crit&&CASH.indexOf(v.fin.h)>=CASH.indexOf('D')?'crit':'ok'}}">${{v.fin.h}}</span></td>
      <td><span class="gr ${{f.crit&&v.fin.r>=6?'crit':'ok'}}">R-${{v.fin.r}}</span></td>
      <td><span class="badge b-${{f.g}}">${{GN[f.g]}}</span></td>
    </tr>`;
  }}).join("");

  updateModalSelCount();
}}

function updateModalSelCount(){{
  const chks = document.querySelectorAll(".mchk:checked");
  const countSpan = document.getElementById("selCount");
  if(countSpan) countSpan.textContent = chks.length;
}}

function openModal(){{
  modalFilter = "all"; modalSearchTerm = "";
  const ms = document.getElementById("modalSearch"); if(ms) ms.value = "";
  document.querySelectorAll("#modalFilters .chip").forEach(c=>c.classList.toggle("on", c.dataset.mf==="all"));
  const sa = document.getElementById("modalSelectAll"); if(sa) sa.checked = false;
  renderModalTable();
  document.getElementById("contractModal").classList.add("open");
}}
function closeModal(){{
  document.getElementById("contractModal").classList.remove("open");
}}

function openSite(name, targetVendorName=null){{
  curSite = SITES.find(s=>s.name===name);
  if(!curSite) return;
  selected = null; filter = "all"; sortV = {{k:null, d:1}}; scope = scopeTop; vendorSearchTerm = "";
  const vs = document.getElementById("vendorSearch"); if(vs) vs.value = "";
  document.querySelectorAll("#filters .chip").forEach(c=>c.classList.toggle("on", c.dataset.f==="all"));
  document.querySelectorAll("#scopeSite button").forEach(b=>b.classList.toggle("on", b.dataset.s===scope));
  document.getElementById("siteName").textContent = "■ 현장명 : " + name;
  document.getElementById("pgTop").classList.remove("on");
  document.getElementById("pgSite").classList.add("on");
  window.scrollTo(0,0);
  renderSite();
  if(targetVendorName){{
    const L = curList();
    const vi = L.findIndex(x=>x.n===targetVendorName);
    if(vi!==-1){{
      selected = vi; renderTable(); renderDetail();
      setTimeout(()=>{{const el=document.getElementById("detail");if(el)el.scrollIntoView({{behavior:"smooth",block:"nearest"}});}}, 100);
    }}
  }}
}}

function backTop(){{
  document.getElementById("pgSite").classList.remove("on");
  document.getElementById("pgTop").classList.add("on");
  window.scrollTo(0,0);
  renderTop();
}}

// ══ 이벤트 바인딩 ══
["qsel","qselTop"].forEach(id=>{{
  const el = document.getElementById(id);
  el.innerHTML = QUARTERS.map(q=>`<option value="${{q}}" ${{q===curQ?'selected':''}}>${{q}}</option>`).join("");
  el.addEventListener("change", e=>{{
    curQ = e.target.value;
    document.getElementById("qsel").value = curQ;
    document.getElementById("qselTop").value = curQ;
    renderTop(); if(curSite) renderSite();
  }});
}});

document.getElementById("scopeTop").addEventListener("click", e=>{{
  const b = e.target.closest("button[data-s]"); if(!b) return;
  scopeTop = b.dataset.s;
  document.querySelectorAll("#scopeTop button").forEach(x=>x.classList.toggle("on", x===b));
  renderTop();
}});
document.getElementById("scopeSite").addEventListener("click", e=>{{
  const b = e.target.closest("button[data-s]"); if(!b) return;
  scope = b.dataset.s; selected = null;
  document.querySelectorAll("#scopeSite button").forEach(x=>x.classList.toggle("on", x===b));
  renderSite();
}});

document.getElementById("siteSearch").addEventListener("input", e=>{{
  siteSearchTerm = e.target.value.trim().toLowerCase();
  renderTop();
}});
document.getElementById("vendorSearch").addEventListener("input", e=>{{
  vendorSearchTerm = e.target.value.trim().toLowerCase();
  renderTable();
}});

document.getElementById("sfilters").addEventListener("click", e=>{{
  const b = e.target.closest("button[data-f]"); if(!b) return;
  sfilter = b.dataset.f;
  document.querySelectorAll("#sfilters .chip").forEach(c=>c.classList.toggle("on", c===b));
  renderTop();
}});
document.getElementById("filters").addEventListener("click", e=>{{
  const b = e.target.closest("button[data-f]"); if(!b) return;
  filter = b.dataset.f;
  document.querySelectorAll("#filters .chip").forEach(c=>c.classList.toggle("on", c===b));
  renderTable();
}});

document.getElementById("gapji").addEventListener("click", e=>{{
  const th = e.target.closest("th.srt");
  if(th){{ sortT = sortT.k===th.dataset.k ? {{k:th.dataset.k, d:-sortT.d}} : {{k:th.dataset.k, d:1}}; renderTop(); return; }}
  const a = e.target.closest("[data-site]");
  if(a) openSite(a.dataset.site);
}});

document.getElementById("topSummaries").addEventListener("click", e=>{{
  const sItem = e.target.closest("[data-site]");
  if(sItem){{ openSite(sItem.dataset.site); return; }}
  const vItem = e.target.closest("[data-vsite]");
  if(vItem){{ openSite(vItem.dataset.vsite, vItem.dataset.vn); }}
}});

// 상세 테이블 인터랙션: 정렬, 현장평가 셀 클릭, 안전평가 인풋 수정, 관리 제외, 상세 열기
document.getElementById("vtable").addEventListener("click", e=>{{
  const th = e.target.closest("th.srt");
  if(th){{ sortV = sortV.k===th.dataset.k ? {{k:th.dataset.k, d:-sortV.d}} : {{k:th.dataset.k, d:1}}; renderTable(); return; }}

  // 현장평가 셀 클릭 (상시 순환)
  const cell = e.target.closest(".cell");
  if(cell){{
    const i = +cell.dataset.v, j = +cell.dataset.j;
    const v = curList()[i];
    v.r[curQ][j] = (v.r[curQ][j] + 1) % 3;
    renderDonuts(); renderTable(); if(selected===i) renderDetail();
    return;
  }}

  // 관리 목록에서 제외
  const delBtn = e.target.closest("[data-del]");
  if(delBtn){{
    const cid = delBtn.dataset.del;
    if(siteManagedMap[curSite.name] && siteManagedMap[curSite.name][curQ]){{
      siteManagedMap[curSite.name][curQ] = siteManagedMap[curSite.name][curQ].filter(id => id !== cid);
      selected = null;
      renderSite();
    }}
    return;
  }}

  const op = e.target.closest("[data-open]");
  if(op){{
    const i = +op.dataset.open;
    selected = (selected===i) ? null : i;
    renderTable(); renderDetail();
    if(selected!==null) document.getElementById("detail").scrollIntoView({{behavior:"smooth", block:"nearest"}});
  }}
}});

// 안전평가 인풋 이벤트 (실시간 넘버패드 및 타이핑)
document.getElementById("vtable").addEventListener("input", e=>{{
  const numInput = e.target.closest(".safe-num-input");
  if(numInput){{
    const i = +numInput.dataset.v, sfKey = numInput.dataset.sf;
    const v = curList()[i];
    let val = parseInt(numInput.value) || 0;
    if(val < 0) val = 0;
    v.sf[sfKey] = val;
    numInput.classList.toggle("active", val > 0);
    renderDonuts(); renderTable(); if(selected===i) renderDetail();
  }}
}});

// 전체 리스트 토글
const toggleBtn = document.getElementById("toggleGapjiBtn");
const gapjiWrap = document.getElementById("gapjiWrap");
const gapjiToolbar = document.getElementById("gapjiToolbar");
if(toggleBtn && gapjiWrap){{
  toggleBtn.addEventListener("click", ()=>{{
    const isHidden = gapjiWrap.style.display === "none";
    gapjiWrap.style.display = isHidden ? "block" : "none";
    if(gapjiToolbar) gapjiToolbar.style.display = isHidden ? "flex" : "none";
    toggleBtn.textContent = isHidden ? "전체 리스트 접기 ▲" : "전체 리스트 펼치기 (59개 현장) ▼";
  }});
}}

// 모달 이벤트
document.getElementById("openModalBtn").addEventListener("click", openModal);
document.getElementById("closeModal").addEventListener("click", closeModal);
document.getElementById("closeModalBtn").addEventListener("click", closeModal);
document.getElementById("modalSearch").addEventListener("input", e=>{{
  modalSearchTerm = e.target.value.trim().toLowerCase();
  renderModalTable();
}});
document.getElementById("modalFilters").addEventListener("click", e=>{{
  const b = e.target.closest("button[data-mf]"); if(!b) return;
  modalFilter = b.dataset.mf;
  document.querySelectorAll("#modalFilters .chip").forEach(c=>c.classList.toggle("on", c===b));
  renderModalTable();
}});

// 전체 선택
document.getElementById("modalSelectAll").addEventListener("change", e=>{{
  const checked = e.target.checked;
  document.querySelectorAll(".mchk").forEach(chk => chk.checked = checked);
  updateModalSelCount();
}});

document.getElementById("modalTable").addEventListener("change", e=>{{
  if(e.target.classList.contains("mchk")) updateModalSelCount();
}});

// 선택한 항목 추가하기
document.getElementById("addSelectedBtn").addEventListener("click", ()=>{{
  if(!curSite) return;
  const checkedChks = Array.from(document.querySelectorAll(".mchk:checked"));
  const selectedCids = checkedChks.map(c => c.dataset.cid);
  
  if(!siteManagedMap[curSite.name]) siteManagedMap[curSite.name] = {{}};
  siteManagedMap[curSite.name][curQ] = selectedCids;
  
  closeModal();
  selected = null;
  renderSite();
}});

document.getElementById("backLink").addEventListener("click", backTop);

renderTop();
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('SUCCESSFULLY GENERATED V8 index.html!')
