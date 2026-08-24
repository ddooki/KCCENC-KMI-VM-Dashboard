import json, re

with open('built_site_data.json', 'r', encoding='utf-8') as f:
    site_bundle = json.load(f)

js_sites = json.dumps(site_bundle['SITES'], ensure_ascii=False, indent=2)
js_real_data = json.dumps(site_bundle['REAL_SITE_DATA'], ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for ts-list (remove scroll, expand all)
html = html.replace('.ts-list{max-height:360px;overflow-y:auto}', '.ts-list{max-height:none;overflow-y:visible}')

# 2. Update summary widgets HTML
old_sec_html = '''  <!-- 상위 10개 요약 위젯 -->
  <div class="top-summaries" id="topSummaries"></div>

  <div class="section">
    <div class="sechead">
      <h2>현장별 업체 상태 현황 (전체)</h2>
      <div class="toolbar">
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
    <div class="tablescroll">
      <table id="gapji">'''

new_sec_html = '''  <!-- 주요 리스크 요약 위젯 -->
  <div class="top-summaries" id="topSummaries"></div>

  <div class="section" id="gapjiSection">
    <div class="sechead">
      <div style="display:flex;align-items:center;gap:12px">
        <h2>현장별 업체 상태 현황 (전체)</h2>
        <button class="btn" id="toggleGapjiBtn" style="padding:5px 13px;font-size:13px;font-weight:700">전체 리스트 펼치기 (59개 현장) ▼</button>
      </div>
      <div class="toolbar" id="gapjiToolbar" style="display:none">
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
    <div class="tablescroll" id="gapjiWrap" style="display:none">
      <table id="gapji">'''

html = html.replace(old_sec_html, new_sec_html)

# 3. Replace Data and Logic in script
pattern = r'(// ══ 현장 마스터[\s\S]*?)(// ══ 전사 현황 도넛 렌더링 ══)'

replacement = f'''// ══ 현장 마스터 (실제 본사 계약 현황 59개 현장) ══
const SITES = {js_sites};
const DIVORD = {{인프라:0, 건축:1, 플랜트:2}};

// ══ 실제 본사 계약 데이터 맵 (총 59개 현장, 총 1,669건 개별 계약 행) ══
const REAL_SITE_DATA = {js_real_data};

function hash(s){{let h=2166136261;for(let i=0;i<s.length;i++){{h^=s.charCodeAt(i);h=Math.imul(h,16777619);}}return h>>>0;}}
function rng(seed){{let a=seed;return()=>{{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}};}}

const cache={{}};
function siteVendors(site){{
  if(cache[site.name]) return cache[site.name];
  const rawList = REAL_SITE_DATA[site.name] || [];
  const list = rawList.map((base, idx) => {{
    const vRd = rng(hash(site.name + "_" + base.n + "_" + (base.cid || idx)));
    return {{
      ...base,
      sf: genSf(vRd, base.inst),
      r: genR(vRd)
    }};
  }});
  cache[site.name] = list;
  return list;
}}

// 현실적인 저위험(정상 대다수) 확률 함수
function genSf(rd, inst){{
  if(!inst) return {{경고:0, 배제:0, 시정:0, 보장:0}};
  const p = rd();
  if(p < 0.94) return {{경고:0, 배제:0, 시정:0, 보장:0}}; // 94% 정상
  if(p < 0.98) return {{경고:1, 배제:0, 시정:0, 보장:0}}; // 4% 주의
  return {{경고:1+Math.floor(rd()*2), 배제:1, 시정:Math.floor(rd()*2), 보장:0}}; // 2% 경보
}}

function genR(rd){{
  const o={{}};
  const isProblem = rd() >= 0.92; // 92% 정상
  const base = Array.from({{length:6}}, () => {{
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
const respScore=(v,q)=> (v.r && v.r[q]) ? v.r[q].reduce((a,x)=>a+PT[x],0) : 0;
function streaks(v,q){{
  const qi=QUARTERS.indexOf(q), out=[];
  if(qi<2 || !v.r) return out;
  for(let j=0;j<6;j++){{
    const q0=QUARTERS[qi], q1=QUARTERS[qi-1], q2=QUARTERS[qi-2];
    if(v.r[q0] && v.r[q1] && v.r[q2] && v.r[q0][j]>0 && v.r[q1][j]>0 && v.r[q2][j]>0) out.push(j);
  }}
  return out;
}}
function respGrade(v,q){{
  const s=respScore(v,q);
  return s>=6?"crit" : s>=3?"warn" : (streaks(v,q).length?"warn":"ok");
}}
function safety(v){{
  if(!v.inst) return {{na:true}};
  const std=TRADE_STD[v.trade]??4;
  const sf=v.sf || {{경고:0,배제:0,시정:0,보장:0}};
  const p=(sf.경고||0)*1+(sf.배제||0)*2+(sf.시정||0)*1+(sf.보장||0)*2;
  const bans=p>std?Math.ceil(p/std)-1:0;
  return {{na:false,std,p,bans,g:bans>=1?"crit":(p>=std*0.75?"warn":"ok")}};
}}
function finance(v){{
  if(!v.fin) return {{g:"ok",crit:false,warn:false}};
  const ci=CREDIT.indexOf(v.fin.c),hi=CASH.indexOf(v.fin.h),r=v.fin.r;
  const crit=ci>=CREDIT.indexOf("B-")||hi>=CASH.indexOf("D")||r>=6;
  const warn=ci>=CREDIT.indexOf("BB-")||hi>=CASH.indexOf("C+")||r>=4;
  return {{g:crit?"crit":warn?"warn":"ok",crit,warn}};
}}
function overall(v,q){{
  const rg=respGrade(v,q);
  const sg=safety(v).na?"ok":safety(v).g;
  const fg=finance(v).g;
  if(rg==="crit"||sg==="crit"||fg==="crit") return "crit";
  if(rg==="warn"||sg==="warn"||fg==="warn") return "warn";
  return "ok";
}}
const GN={{ok:"정상",warn:"주의",crit:"경보"}};
const CLR={{ok:"#6f9463",warn:"#d9a441",crit:"#c25d53"}};

// ══ 상위 요약 위젯 렌더링 ══
function renderTopSummaries(){{
  const wrap = document.getElementById("topSummaries");
  if(!wrap) return;

  // 1. 현장별 통계
  const siteList = SITES.map(s => {{
    const vs = siteVendors(s);
    let critCnt = 0, warnCnt = 0, totalAmt = 0;
    vs.forEach(v => {{
      const ov = overall(v, curQ);
      if(ov === "crit") critCnt++;
      else if(ov === "warn") warnCnt++;
      totalAmt += v.amt;
    }});
    const g = critCnt >= 1 ? "crit" : (warnCnt >= 1 ? "warn" : "ok");
    const score = critCnt * 10 + warnCnt;
    return {{ site: s, vs, critCnt, warnCnt, g, score, totalAmt }};
  }}).sort((a, b) => b.score - a.score || b.totalAmt - a.totalAmt).slice(0, 10);

  // 2. 협력업체별 리스크 목록
  const vendorRiskList = [];
  SITES.forEach(s => {{
    const vs = siteVendors(s);
    vs.forEach(v => {{
      const ov = overall(v, curQ);
      const fg = finance(v).g;
      const rg = respGrade(v, curQ);
      const sg = safety(v).na ? "ok" : safety(v).g;
      let rScore = 0;
      if(ov === "crit") rScore += 100;
      else if(ov === "warn") rScore += 20;
      if(fg === "crit") rScore += 30; else if(fg === "warn") rScore += 10;
      if(rg === "crit") rScore += 30; else if(rg === "warn") rScore += 10;
      if(sg === "crit") rScore += 30; else if(sg === "warn") rScore += 10;

      vendorRiskList.push({{
        site: s,
        v,
        ov,
        fg,
        rg,
        sg,
        rScore,
        amt: v.amt
      }});
    }});
  }});

  vendorRiskList.sort((a, b) => b.rScore - a.rScore || b.amt - a.amt);
  const topVendors = vendorRiskList.slice(0, 10);

  let h1 = `
  <div class="ts-card">
    <div class="ts-head">
      <h3>주요 현장 리스크 현황</h3>
      <span style="font-size:12.5px;color:var(--muted)">리스크 집중도 순</span>
    </div>
    <div class="ts-list">
  `;
  siteList.forEach((item, idx) => {{
    const rankClass = idx < 3 ? "ts-rank top3" : "ts-rank";
    h1 += `
      <div class="ts-item" onclick="openSiteByName('${{item.site.name}}')">
        <span class="${{rankClass}}">${{idx+1}}</span>
        <div class="ts-info">
          <div class="ts-name">${{item.site.name}}</div>
          <div class="ts-sub">${{item.site.div}} · 계약 ${{item.vs.length}}건 · ${{(item.totalAmt/1e8).toFixed(1)}}억원</div>
        </div>
        <div>
          <span class="badge b-${{item.g}}">${{GN[item.g]}}</span>
        </div>
      </div>
    `;
  }});
  h1 += `</div></div>`;

  let h2 = `
  <div class="ts-card">
    <div class="ts-head">
      <h3>중점 모니터링 협력업체</h3>
      <span style="font-size:12.5px;color:var(--muted)">위험도 평가 순</span>
    </div>
    <div class="ts-list">
  `;
  topVendors.forEach((item, idx) => {{
    const rankClass = idx < 3 ? "ts-rank top3" : "ts-rank";
    h2 += `
      <div class="ts-item" onclick="openSiteByName('${{item.site.name}}')">
        <span class="${{rankClass}}">${{idx+1}}</span>
        <div class="ts-info">
          <div class="ts-name">${{item.v.n}}</div>
          <div class="ts-sub">${{item.site.name}} · ${{item.v.item || item.v.cat}}</div>
        </div>
        <div class="ts-tri">
          <span class="ts-tag fin ${{item.fg}}">재무:${{GN[item.fg]}}</span>
          <span class="ts-tag resp ${{item.rg}}">현장:${{GN[item.rg]}}</span>
          <span class="ts-tag safe ${{item.sg}}">안전:${{GN[item.sg]}}</span>
        </div>
        <div>
          <span class="badge b-${{item.ov}}">${{GN[item.ov]}}</span>
        </div>
      </div>
    `;
  }});
  h2 += `</div></div>`;

  wrap.innerHTML = h1 + h2;
}}

\\2'''

html = re.sub(pattern, replacement, html)

# 4. Add Toggle Listener for Gapji Section
gapji_toggle_js = '''
  // Gapji Toggle
  const toggleBtn = document.getElementById("toggleGapjiBtn");
  const gapjiWrap = document.getElementById("gapjiWrap");
  const gapjiToolbar = document.getElementById("gapjiToolbar");
  if(toggleBtn && gapjiWrap){
    toggleBtn.addEventListener("click", () => {
      const isHidden = gapjiWrap.style.display === "none";
      gapjiWrap.style.display = isHidden ? "block" : "none";
      if(gapjiToolbar) gapjiToolbar.style.display = isHidden ? "flex" : "none";
      toggleBtn.textContent = isHidden ? "전체 리스트 접기 ▲" : "전체 리스트 펼치기 (59개 현장) ▼";
    });
  }
'''

if 'toggleGapjiBtn' not in html:
    html = html.replace('renderTopSummaries();', 'renderTopSummaries();\n' + gapji_toggle_js)

# 5. Fix renderTable to use item/cat 1:1 without '外'
html = html.replace('${v.ct.length>1?` · 외 ${v.ct.length-1}건`:""}', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('SUCCESSFULLY GENERATED NEW index.html!')
