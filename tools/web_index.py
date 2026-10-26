# -*- coding: utf-8 -*-
"""网页版首页：按「年级 → 领域 → 知识点」组织的小学数学知识地图。

`__OUTLINE__` 与 `__DATA__` 由 tools/build.py 注入。
"""

WEB_INDEX_CSS = r"""
:root{
  --paper:#f5f2ea; --card:#fffdf8; --ink:#1d2521; --muted:#6c756f;
  --line:#e3ded2; --accent:#2f6f6b; --accent-soft:#e3efec;
  --shadow:0 1px 2px rgba(29,37,33,.04),0 10px 30px rgba(29,37,33,.06);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:136px}
body{
  max-width:none;margin:0;padding:0;background:var(--paper);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;
  line-height:1.6;-webkit-font-smoothing:antialiased;
}
button{font-family:inherit;color:inherit}
a{color:inherit}
[hidden]{display:none!important}
::selection{background:#cfe3df}

/* ---------- 顶栏 ---------- */
.topbar{
  position:sticky;top:0;z-index:60;display:flex;align-items:center;gap:18px;
  padding:11px clamp(16px,3vw,32px);background:rgba(245,242,234,.88);
  -webkit-backdrop-filter:saturate(1.2) blur(16px);backdrop-filter:saturate(1.2) blur(16px);
  border-bottom:1px solid rgba(227,222,210,.85);
}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex:0 0 auto}
.brand-mark{width:34px;height:34px;border-radius:10px;background:var(--ink);color:#fff;display:grid;place-items:center;font-weight:800;font-size:15px;letter-spacing:-.04em}
.brand-text{display:flex;flex-direction:column;font-weight:800;font-size:15px;line-height:1.12;letter-spacing:-.01em}
.brand-text small{font-weight:500;font-size:9px;color:var(--muted);letter-spacing:.2em;margin-top:2px}
.searchbox{position:relative;flex:1;max-width:520px;margin-left:auto}
.searchbox .ico{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:var(--muted);pointer-events:none}
.searchbox input{
  width:100%;height:40px;padding:0 38px 0 39px;border:1px solid var(--line);border-radius:999px;
  background:#fff;font-size:13.5px;color:var(--ink);outline:none;
  transition:border-color .18s,box-shadow .18s;
}
.searchbox input::placeholder{color:#a2aaa3}
.searchbox input::-webkit-search-cancel-button,.searchbox input::-webkit-search-decoration{-webkit-appearance:none;appearance:none}
.searchbox input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.searchbox .clear{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:25px;height:25px;border:0;border-radius:50%;background:#eee9df;color:var(--muted);cursor:pointer;font-size:15px;line-height:1;padding:0}
.repo{font-size:11.5px;color:var(--muted);text-decoration:none;white-space:nowrap;letter-spacing:.02em}
.repo:hover{color:var(--ink)}
.exam-top{color:var(--accent)!important;font-weight:700;margin-right:2px}

/* ---------- Hero ---------- */
.hero{
  max-width:1180px;margin:0 auto;padding:clamp(40px,7vw,80px) clamp(16px,3vw,32px) 26px;
  display:grid;grid-template-columns:minmax(0,1fr) auto;gap:44px;align-items:center;
}
.eyebrow{margin:0 0 13px;font-size:10.5px;font-weight:700;letter-spacing:.24em;color:var(--accent);text-transform:uppercase}
.hero h1{
  margin:0 0 18px;border:0;padding:0;
  font-family:"Songti SC","Noto Serif SC",Georgia,serif;
  font-size:clamp(40px,6.4vw,70px);line-height:1.02;letter-spacing:-.035em;font-weight:700;
}
.hero h1 em{font-style:normal;color:var(--accent)}
.stats{display:flex;flex-wrap:wrap;gap:clamp(18px,3vw,38px);margin-top:28px}
.stat{display:flex;flex-direction:column;gap:1px}
.stat b{font-size:23px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.stat span{font-size:10.5px;color:var(--muted);letter-spacing:.08em}
.hero-side{display:flex;flex-direction:column;align-items:center;gap:12px}
.ring{
  --p:50;width:138px;height:138px;border-radius:50%;position:relative;
  background:conic-gradient(var(--accent) calc(var(--p) * 1%), #e4dfd3 0);
  display:grid;place-items:center;
}
.ring::after{content:"";position:absolute;inset:11px;border-radius:50%;background:var(--paper)}
.ring>div{position:relative;z-index:1;text-align:center;display:flex;flex-direction:column;line-height:1.2}
.ring b{font-size:25px;letter-spacing:-.02em}
.ring span{font-size:9.5px;color:var(--muted);letter-spacing:.1em;margin-top:2px}
.ring-note{margin:0;max-width:170px;text-align:center;font-size:10.5px;line-height:1.6;color:var(--muted)}

/* ---------- 年级导航 ---------- */
#gradeNav{
  position:sticky;top:64px;z-index:50;
  background:rgba(245,242,234,.92);
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
  border-top:1px solid rgba(227,222,210,.55);border-bottom:1px solid var(--line);
}
.nav-inner{max-width:1180px;margin:0 auto;padding:8px clamp(16px,3vw,32px);display:flex;gap:5px;overflow-x:auto;scrollbar-width:none}
.nav-inner::-webkit-scrollbar{display:none}
.grade-tab{
  display:flex;align-items:center;gap:7px;border:0;background:transparent;border-radius:999px;
  padding:8px 13px;cursor:pointer;color:var(--muted);white-space:nowrap;font-size:12px;
  transition:background .16s,color .16s;
}
.grade-tab b{font-size:13px;font-weight:700;color:var(--ink);transition:color .16s}
.grade-tab span{font-size:10px;color:#9aa39d;transition:color .16s}
.grade-tab:hover{background:#ece7dc}
.grade-tab.active{background:var(--ink)}
.grade-tab.active b,.grade-tab.active span{color:#fff}

/* ---------- 筛选条 ---------- */
.toolbar{
  max-width:1180px;margin:0 auto;padding:18px clamp(16px,3vw,32px) 0;
  display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
}
.toolbar p{margin:0;font-size:11.5px;color:var(--muted)}
.seg{display:inline-flex;background:#eae5da;border-radius:999px;padding:3px;gap:2px}
.seg button{border:0;background:transparent;border-radius:999px;padding:6px 12px;font-size:11.5px;color:var(--muted);cursor:pointer;transition:background .16s,color .16s,box-shadow .16s}
.seg button.on{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}

/* ---------- 年级板块 ---------- */
#boards{max-width:1180px;margin:0 auto;padding:0 clamp(16px,3vw,32px) 24px}
.board{padding:38px 0 8px;border-top:1px solid var(--line);scroll-margin-top:128px}
.board:first-child{border-top:0}
.board-head{display:flex;align-items:center;gap:16px;margin-bottom:20px}
.grade-mark{
  width:62px;height:62px;flex:0 0 62px;border-radius:18px;display:grid;place-items:center;
  font-family:"Songti SC","Noto Serif SC",serif;font-size:29px;font-weight:700;
  color:var(--c);border:1.5px solid var(--c);background:#fff;
}
.board-title{min-width:0}
.board-kicker{margin:0 0 1px;font-size:9.5px;font-weight:600;letter-spacing:.2em;color:var(--muted)}
.board-title h2{margin:0;border:0;padding:0;font-size:clamp(22px,2.8vw,29px);line-height:1.2;letter-spacing:-.02em}
.board-title p{margin:3px 0 0;font-size:11.5px;color:var(--muted);line-height:1.55}
.board-meta{margin-left:auto;text-align:right;min-width:150px}
.board-meta>div:first-child{font-size:10.5px;color:var(--muted)}
.board-meta b{font-size:16px;color:var(--ink)}
.board-meta .progress{height:5px;border-radius:99px;background:#e4dfd3;overflow:hidden;margin-top:6px}
.progress i{display:block;height:100%;border-radius:99px;background:var(--c)}

/* ---------- 领域与知识点 ---------- */
.domain{margin:0 0 22px}
.domain h3{display:flex;align-items:center;gap:8px;margin:0 0 10px;font-size:11.5px;font-weight:700;letter-spacing:.07em;color:#59625c}
.domain h3::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--c);flex:0 0 6px}
.domain h3 .n{margin-left:2px;padding:1px 7px;border-radius:99px;background:#ebe6db;color:#9aa39d;font-size:9.5px;font-weight:500;letter-spacing:0}
.topic-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(192px,1fr));gap:8px}
.topic{
  position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:4px;
  min-height:64px;padding:11px 32px 10px 13px;border:1px solid var(--line);
  border-radius:11px;background:var(--card);text-align:left;cursor:pointer;
  transition:transform .15s,border-color .15s,box-shadow .15s;
}
.topic:hover{transform:translateY(-2px);border-color:#cfc8b9;box-shadow:0 7px 20px rgba(29,37,33,.065)}
.topic-title{font-size:13px;font-weight:600;line-height:1.45;letter-spacing:-.005em}
.topic-sub{display:flex;align-items:center;gap:6px;font-size:10px;color:var(--muted)}
.term{display:inline-grid;place-items:center;min-width:16px;height:16px;padding:0 3px;border-radius:4px;background:#efeae0;color:#6f776f;font-size:9px;line-height:1}
.status{display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
.status::before{content:"";width:5px;height:5px;border-radius:50%;background:currentColor}
.status.ready{color:#3f7d5a}
.status.soon{color:#a3aaa4}
.topic .arrow{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:14px;color:#b3ab9d;opacity:0;transition:opacity .15s,transform .15s}
.topic:hover .arrow{opacity:1;transform:translate(2px,-50%)}
.topic.soon{border-style:dashed;background:transparent;color:#768078}
.topic.soon .topic-title{font-weight:500}
.topic.soon:hover{transform:none;border-color:#cfc8b9;box-shadow:none}
.topic.soon .arrow{display:none}
#emptyFilter{max-width:1180px;margin:0 auto;padding:40px clamp(16px,3vw,32px);color:var(--muted);font-size:13px;text-align:center}

/* ---------- 搜索 ---------- */
#searchPanel{max-width:1180px;margin:0 auto;padding:24px clamp(16px,3vw,32px) 44px;min-height:50vh}
.search-head{display:flex;align-items:baseline;gap:10px;margin-bottom:14px}
.search-head h2{margin:0;font-size:20px;letter-spacing:-.01em}
.search-head span{font-size:11.5px;color:var(--muted)}
.hit{
  display:flex;align-items:center;gap:12px;width:100%;padding:13px 14px;
  border:1px solid transparent;border-bottom-color:var(--line);background:transparent;
  text-align:left;cursor:pointer;border-radius:10px;
}
.hit:hover{background:var(--card);border-color:var(--line)}
.hit-main{min-width:0;flex:1;display:flex;flex-direction:column;gap:2px}
.hit-title{font-size:13.5px;font-weight:600}
.hit-meta{font-size:10.5px;color:var(--muted)}
.hit .status{font-size:10px}
.empty{padding:48px 0;color:var(--muted);font-size:13.5px;text-align:center}

/* ---------- 详情 ---------- */
#detailView{min-height:100vh}
.detail-wrap{max-width:900px;margin:0 auto;padding:28px clamp(16px,3vw,32px) 60px}
.detail-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px}
.back{
  border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;
  font-size:11.5px;cursor:pointer;transition:border-color .16s,color .16s;
}
.back:hover{border-color:var(--ink);color:var(--ink)}
.crumbs{font-size:10.5px;color:var(--muted);text-align:right}
.kp-detail{
  background:var(--card);border:1px solid var(--line);border-radius:20px;
  padding:clamp(22px,4vw,40px);box-shadow:var(--shadow);
}
.kp-kicker{font-size:10.5px;font-weight:700;letter-spacing:.12em;color:var(--c,var(--accent))}
.kp-detail h1{margin:8px 0 12px;border:0;padding:0;font-size:clamp(26px,4vw,36px);line-height:1.2;letter-spacing:-.025em}
.kp-meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 24px}
.chip{display:inline-flex;align-items:center;padding:4px 9px;border-radius:99px;background:#f0ece2;color:#5d665f;font-size:10px;letter-spacing:.01em}
.kp-body{max-width:740px;font-size:14.5px;line-height:1.85}
.kp-body h2{font-size:18px;margin:1.6em 0 .6em;padding-bottom:6px;border-bottom:1px solid var(--line)}
.kp-body h3{font-size:14.5px;margin:1.2em 0 .4em}
.kp-body .example{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:14px 0}
.kp-body .problem{background:#f7f4ec;border-radius:8px;padding:8px 12px}
.kp-body img{display:block;max-width:100%;height:auto;margin:18px auto;border-radius:8px}
.kp-body .answer{color:#a4472f}
.kp-body details summary{color:var(--accent);cursor:pointer}
.kp-body .covers{color:#9aa39d}
.kp-skills{display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin-top:26px;padding-top:18px;border-top:1px solid var(--line)}
.detail-foot{margin-top:24px}

/* ---------- 待补充详情 ---------- */
.soon-card{
  background:var(--card);border:1px dashed #cfc8b9;border-radius:20px;
  padding:clamp(28px,5vw,52px);text-align:center;
}
.soon-icon{width:54px;height:54px;border-radius:16px;background:#efeae0;display:grid;place-items:center;margin:0 auto 16px;font-size:21px;color:#8d948c}
.soon-card h2{margin:6px 0 8px;border:0;padding:0;font-size:24px}
.soon-card p{max-width:470px;margin:0 auto;color:var(--muted);font-size:13.5px;line-height:1.8}
.soon-related{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:26px}
.soon-related button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 11px;font-size:10.5px;cursor:pointer}
.soon-related button:hover{border-color:var(--accent);color:var(--accent)}

/* ---------- 页脚与提示 ---------- */
.site-foot{max-width:1180px;margin:0 auto;padding:28px clamp(16px,3vw,32px) 46px;border-top:1px solid var(--line);color:var(--muted);font-size:10.5px;line-height:1.8}
.site-foot p{margin:4px 0}
.site-foot a{color:var(--accent)}
#toast{
  position:fixed;left:50%;bottom:26px;z-index:100;transform:translate(-50%,14px);
  background:var(--ink);color:#fff;padding:9px 15px;border-radius:999px;font-size:11.5px;
  opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;
}
#toast.on{opacity:1;transform:translate(-50%,0)}




/* ---------- 竞赛真题入口 ---------- */
.hero-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:20px}
.hero-link{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;background:var(--accent);color:#fff;font-size:12.5px;font-weight:700;letter-spacing:.04em;text-decoration:none;box-shadow:0 6px 16px rgba(47,111,107,.18)}
.hero-link span{font-size:10.5px;font-weight:500;opacity:.82}
.hero-link:hover{background:#245a56;transform:translateY(-1px)}
.exam-home{max-width:1180px;margin:26px auto 0;padding:0 clamp(16px,3vw,32px)}
.exam-home-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:10px}
.exam-home-head .eyebrow{margin:0 0 2px}
.exam-home-head h2{margin:0;font-size:18px;letter-spacing:-.01em}
.exam-home-head p{margin:2px 0 0;color:var(--muted);font-size:11px}
.exam-home-more{font-size:11px;color:var(--accent);text-decoration:none;font-weight:600;white-space:nowrap}
.exam-home-more:hover{text-decoration:underline}
.exam-home-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}
.exam-home-card{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:11px 13px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--ink);text-decoration:none;transition:border-color .15s,transform .15s}
.exam-home-card:hover{border-color:var(--accent);transform:translateY(-1px)}
.exam-home-card b{font-size:12px;font-weight:700}
.exam-home-card span{font-size:10px;color:var(--muted);white-space:nowrap}

/* ---------- 复习统计 ---------- */
.review-panel{max-width:1180px;margin:16px auto 0;padding:0 clamp(16px,3vw,32px)}
.review-card{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:13px 16px;border:1px solid var(--line);border-radius:16px;background:var(--card)}
.review-stats{display:flex;gap:clamp(14px,2.5vw,30px);flex-wrap:wrap}
.review-stat{display:flex;flex-direction:column;min-width:0}
.review-stat b{font-size:17px;font-weight:800;letter-spacing:-.02em;line-height:1.25;white-space:nowrap}
.review-stat span{font-size:9.5px;color:var(--muted);letter-spacing:.06em}
.review-stat b#reviewTop{max-width:130px;overflow:hidden;text-overflow:ellipsis}
.review-progress{flex:1;min-width:160px}
.review-bar{height:6px;border-radius:99px;background:#e4dfd3;overflow:hidden}
.review-bar i{display:block;height:100%;width:0;border-radius:99px;background:var(--accent);transition:width .3s}
.review-hint{margin:4px 0 0;font-size:9.5px;color:#9aa39d}
.review-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.review-toggle{display:flex;align-items:center;gap:4px;font-size:10.5px;color:var(--muted);cursor:pointer;white-space:nowrap}
.review-toggle input{accent-color:var(--accent);margin:0}
.review-reset{border:0;background:transparent;padding:0;font-size:9.5px;color:#a3aaa4;text-decoration:underline;cursor:pointer;white-space:nowrap}
.review-reset:hover{color:#b5525c}
.view-badge{display:inline-flex;align-items:center;align-self:flex-start;margin-top:3px;padding:1px 7px;border-radius:99px;background:#f1ede4;color:#9aa39d;font-size:9px;line-height:1.65;letter-spacing:.02em}
.view-badge.has{background:#e3efec;color:#2f6f6b;font-weight:600}

/* ---------- 响应式 ---------- */
@media(max-width:860px){
  .hero{grid-template-columns:1fr;gap:24px;padding-top:36px}
  .hero-side{flex-direction:row;justify-content:flex-start;align-items:center;gap:16px}
  .ring{width:94px;height:94px}
  .ring b{font-size:18px}
  .ring-note{text-align:left;max-width:230px}
  .board-head{flex-wrap:wrap}
  .board-meta{margin-left:0;text-align:left;min-width:0;flex:1 1 100%;display:flex;align-items:center;gap:12px}
  .board-meta .progress{flex:1;margin-top:0}
  #gradeNav{position:static}
  html{scroll-padding-top:20px}
}
@media(max-width:720px){
  .topbar{flex-wrap:wrap;padding:10px 16px;gap:9px}
  .searchbox{order:3;flex-basis:100%;max-width:none;margin-left:0}
  .repo{display:none}
  .brand-mark{width:30px;height:30px;font-size:13px}
  .brand-text{font-size:14px}
  .hero{padding:28px 16px 20px}
  .hero h1{font-size:40px}
  .stats{gap:18px}
  .toolbar{padding:14px 16px 0;flex-direction:column;align-items:flex-start;gap:8px}
  #boards{padding:0 16px 16px}
  .topic-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:7px}
  .topic{min-height:58px;padding:9px 27px 9px 11px}
  .topic-title{font-size:12.5px}
  .detail-wrap{padding:18px 14px 40px}
  .crumbs{display:none}
  .board{padding-top:30px;scroll-margin-top:20px}
  .exam-home-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .exam-home{padding:0 16px}
  .hero-actions{margin-top:16px}
}
"""

WEB_INDEX_BODY = r"""
<header class="topbar">
  <a class="brand" href="#/" onclick="event.preventDefault();goHome()" aria-label="返回知识地图">
    <span class="brand-mark">M</span>
    <span class="brand-text">小学数学<small>知识地图</small></span>
  </a>
  <div class="searchbox">
    <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.6-3.6"></path>
    </svg>
    <input id="q" type="search" placeholder="搜索知识点、年级或关键词…" autocomplete="off" aria-label="搜索知识点">
    <button id="clearSearch" class="clear" type="button" aria-label="清空搜索" hidden>×</button>
  </div>
  <a class="repo exam-top" href="exam/index.html">真题</a>
  <a class="repo" href="https://github.com/guobailin/Mathmatics" target="_blank" rel="noreferrer">GitHub ↗</a>
</header>

<main id="app">
  <section class="hero" id="hero">
    <div class="hero-copy">
      <p class="eyebrow">1–6 年级 · 课内 + 奥数</p>
      <h1>小学数学<br><em>知识地图</em></h1>
      <div class="stats">
        <div class="stat"><b>6</b><span>年级</span></div>
        <div class="stat"><b>7</b><span>大板块</span></div>
        <div class="stat"><b id="statTotal">216</b><span>知识点</span></div>
        <div class="stat"><b id="statOnline">107</b><span>已更新</span></div>
      </div>
      <div class="hero-actions">
        <a class="hero-link" href="exam/index.html">竞赛真题 <span>全部真题 →</span></a>
      </div>
    </div>
    <div class="hero-side">
      <div class="ring" id="coverageRing" style="--p:50"><div><b id="coverageNum">50%</b><span>内容覆盖</span></div></div>
      <p class="ring-note">按人教版 2024 教材 12 册<br>与奥数七大模块整理</p>
    </div>
  </section>

  <nav id="gradeNav" aria-label="年级导航">
    <div class="nav-inner" id="gradeTabs"></div>
  </nav>

  <div class="toolbar">
    <p id="mapSummary">正在加载知识地图…</p>
    <div class="seg" role="group" aria-label="内容状态筛选">
      <button data-f="all" class="on" onclick="setFilter('all')">全部</button>
      <button data-f="online" onclick="setFilter('online')">已更新</button>
      <button data-f="soon" onclick="setFilter('soon')">待补充</button>
    </div>
  </div>


  <section class="review-panel" id="reviewPanel" aria-label="复习统计">
    <div class="review-card">
      <div class="review-stats">
        <div class="review-stat"><b id="reviewTotal">0</b><span>总复习次数</span></div>
        <div class="review-stat"><b id="reviewedCount">0</b><span>已复习知识点</span></div>
        <div class="review-stat"><b id="reviewRate">0%</b><span>复习覆盖率</span></div>
        <div class="review-stat"><b id="reviewTop">—</b><span>最常复习</span></div>
      </div>
      <div class="review-progress">
        <div class="review-bar"><i id="reviewBar"></i></div>
        <p class="review-hint" id="reviewHint">点击知识点即计一次，统计保存在本机浏览器。</p>
      </div>
      <div class="review-actions">
        <label class="review-toggle"><input type="checkbox" id="onlyUnreviewed" onchange="setOnlyUnreviewed(this.checked)"> 只看未复习</label>
        <button type="button" class="review-reset" onclick="resetViews()">清空统计</button>
      </div>
    </div>
  </section>

  <div id="boards"></div>
  <div id="emptyFilter" hidden>当前筛选下暂无知识点，切换到“全部”看看完整地图。</div>

  __EXAM_HOME__

  <div id="searchPanel" hidden></div>

  <footer class="site-foot">
    <p>课程大纲依据人教版（2024）小学数学 1–6 年级 12 册，以及小学奥数计算、数论、计数、几何、行程、应用题、组合七大模块整理。</p>
    <p>内容来自仓库 <code>content/</code>；标为“待补充”的知识点已列入建设清单。 · <a href="https://github.com/guobailin/Mathmatics" target="_blank" rel="noreferrer">GitHub 仓库 ↗</a></p>
  </footer>
</main>

<section id="detailView" hidden></section>
<div id="toast" role="status" aria-live="polite"></div>

<script>
const OUTLINE = __OUTLINE__;
const DATA = __DATA__;
const BOARDS = OUTLINE.boards;
const STATS = OUTLINE.stats;
const DATA_BY_ID = Object.fromEntries(DATA.map(d => [d.id, d]));
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const stars = n => '★'.repeat(n || 0) + '☆'.repeat(Math.max(0, 3 - (n || 0)));
let currentFilter = 'all';
let restoreY = 0;
let searchTimer = 0;
let observer = null;

const LOC = {};
for (const b of BOARDS) {
  for (const dm of b.domains) {
    for (const t of dm.topics) {
      if (t.content) LOC[t.content] = { board: b, domain: dm.name, term: t.term };
    }
  }
}



const VIEW_KEY = 'mathkb_review_v1';
function loadViews() {
  try {
    const obj = JSON.parse(localStorage.getItem(VIEW_KEY) || '{}');
    return obj && typeof obj === 'object' ? obj : {};
  } catch (e) { return {}; }
}
let VIEWS = loadViews();
let onlyUnreviewed = false;
function saveViews() {
  try { localStorage.setItem(VIEW_KEY, JSON.stringify(VIEWS)); } catch (e) { /* 隐私模式忽略 */ }
}
function viewCount(id) { return id ? (Number(VIEWS[id]) || 0) : 0; }
function reviewLabel(id) { const n = viewCount(id); return n ? `复习 ${n} 次` : '未复习'; }
function recordView(id) {
  if (!id) return;
  VIEWS[id] = viewCount(id) + 1;
  saveViews();
}


function setHash(h) {
  try { history.replaceState(null, '', h); } catch (e) { /* file:// 下忽略 */ }
}

function scrollToY(y, instant) {
  if (!instant) {
    try { window.scrollTo({ top: y, behavior: 'smooth' }); }
    catch (e) { window.scrollTo(0, y); }
    return;
  }
  const html = document.documentElement;
  const prev = html.style.scrollBehavior;
  html.style.scrollBehavior = 'auto';
  window.scrollTo(0, y);
  html.style.scrollBehavior = prev;
}

function renderIndex() {
  $('#gradeTabs').innerHTML = BOARDS.map(b => `
    <button class="grade-tab" data-key="${esc(b.key)}" onclick="jump('${esc(b.key)}')">
      <b>${esc(b.label)}</b><span>${b.online}/${b.count}</span>
    </button>`).join('');
  $('#boards').innerHTML = BOARDS.map(boardHTML).join('');
  $('#statTotal').textContent = STATS.total;
  $('#statOnline').textContent = STATS.online;
  const pct = STATS.total ? Math.round(STATS.online / STATS.total * 100) : 0;
  $('#coverageRing').style.setProperty('--p', pct);
  $('#coverageNum').textContent = pct + '%';
  $('#mapSummary').textContent = `共 ${STATS.total} 个知识点 · 已更新 ${STATS.online} 个 · 待补充 ${STATS.stubs} 个`;
  refreshReviewUI();
  applyFilter();
  observeBoards();
}

function boardHTML(b) {
  const pct = b.count ? Math.round(b.online / b.count * 100) : 0;
  return `<section class="board" id="board-${esc(b.key)}" style="--c:${esc(b.color)}">
    <div class="board-head">
      <div class="grade-mark">${esc(b.short)}</div>
      <div class="board-title">
        <p class="board-kicker">${b.kind === 'olympiad' ? '专题拓展' : '课内同步'}</p>
        <h2>${esc(b.label)}</h2>
        <p>${esc(b.intro)}</p>
      </div>
      <div class="board-meta">
        <div><b>${b.online}</b> / ${b.count} 已更新</div>
        <div class="progress"><i style="width:${pct}%"></i></div>
      </div>
    </div>
    ${b.domains.map(dm => domainHTML(b, dm)).join('')}
  </section>`;
}

function domainHTML(b, dm) {
  return `<div class="domain">
    <h3>${esc(dm.name)}<span class="n" data-total="${dm.topics.length}">${dm.topics.length}</span></h3>
    <div class="topic-grid">${dm.topics.map(t => topicHTML(b, dm, t)).join('')}</div>
  </div>`;
}

function topicHTML(b, dm, t) {
  const ready = !!t.content;
  const d = ready ? DATA_BY_ID[t.content] : null;
  return `<button class="topic ${ready ? 'ready' : 'soon'}"
      data-board="${esc(b.key)}" data-domain="${esc(dm.name)}"
      data-title="${esc(t.title)}" data-content="${esc(t.content || '')}"
      onclick="openTopic(this)">
    <span class="topic-title">${esc(t.title)}</span>
    <span class="topic-sub">${t.term ? `<span class="term">${t.term}</span>` : ''}<span class="status ${ready ? 'ready' : 'soon'}">${ready ? '更新 ' + (d && d.updated ? d.updated.slice(5) : '已更新') : '待补充'}</span></span>
    ${ready ? `<span class="view-badge ${viewCount(t.content) ? 'has' : ''}" data-view="${esc(t.content)}">${reviewLabel(t.content)}</span>` : ''}
    <span class="arrow">→</span>
  </button>`;
}

function openTopic(el) {
  const cid = el.dataset.content;
  if (cid) openContent(cid);
  else openSoon(el.dataset.board, el.dataset.domain, el.dataset.title);
}

function openContent(id) {
  const d = DATA_BY_ID[id];
  if (!d) { toast('内容未找到'); return; }
  recordView(id);
  const reviewCount = viewCount(id);
  const loc = LOC[id] || { board: { label: d.module, color: '#2F6F6B' }, domain: '', term: '' };
  restoreY = window.scrollY;
  const tags = (d.tags || []).map(t => `<span class="chip">${esc(t)}</span>`).join('');
  const skills = (d.skills || []).map(s => `<span class="chip">${esc(s)}</span>`).join('');
  $('#detailView').innerHTML = `<div class="detail-wrap">
    <div class="detail-top">
      <button class="back" onclick="goHome()">← 知识地图</button>
      <div class="crumbs">${esc(loc.board.label)} / ${esc(loc.domain)}${loc.term ? ' / ' + loc.term : ''}</div>
    </div>
    <article class="kp-detail" style="--c:${loc.board.color || '#2F6F6B'}">
      <div class="kp-kicker">${esc(loc.board.label)} · ${esc(loc.domain)}${loc.term ? ' · ' + loc.term + '册' : ''}</div>
      <h1>${esc(d.title)}</h1>
      <div class="kp-meta">
        <span class="chip">难度 ${stars(d.difficulty)}</span>
        <span class="chip">适用年级 ${d.grade.join('、')}</span>
        <span class="chip">更新于 ${esc(d.updated || '')}</span>
        <span class="chip" id="reviewChip">已复习 ${reviewCount} 次</span>
        ${tags}
      </div>
      <div class="kp-body">${d.html}</div>
      ${skills ? `<div class="kp-skills"><span class="chip">覆盖技能</span>${skills}</div>` : ''}
    </article>
    <div class="detail-foot"><button class="back" onclick="goHome()">← 返回知识地图</button></div>
  </div>`;
  $('#app').hidden = true;
  $('#detailView').hidden = false;
  refreshReviewUI();
  scrollToY(0, true);
  renderMath($('#detailView'));
  document.title = `${d.title} · 小学数学知识地图`;
  setHash('#/topic/' + encodeURIComponent(id));
}

function openSoon(boardKey, domain, title) {
  const b = BOARDS.find(x => x.key === boardKey) || { label: '', color: '#2F6F6B', domains: [] };
  const related = (b.domains.find(x => x.name === domain)?.topics || [])
    .filter(t => t.content && t.title !== title).slice(0, 6);
  restoreY = window.scrollY;
  $('#detailView').innerHTML = `<div class="detail-wrap">
    <div class="detail-top">
      <button class="back" onclick="goHome()">← 知识地图</button>
      <div class="crumbs">${esc(b.label)} / ${esc(domain)}</div>
    </div>
    <div class="soon-card" style="--c:${b.color}">
      <div class="soon-icon">✎</div>
      <div class="kp-kicker">${esc(b.label)} · ${esc(domain)}</div>
      <h2>${esc(title)}</h2>
      <p>这个知识点已经列入知识地图，讲解与 ★3 / ★4 / ★5 例题正在补充中。可以先看看同领域已更新的内容。</p>
      ${related.length ? `<div class="soon-related">${related.map(t => `<button data-content="${esc(t.content)}" onclick="openContent(this.dataset.content)">${esc(t.title)}</button>`).join('')}</div>` : ''}
    </div>
    <div class="detail-foot"><button class="back" onclick="goHome()">← 返回知识地图</button></div>
  </div>`;
  $('#app').hidden = true;
  $('#detailView').hidden = false;
  scrollToY(0, true);
  document.title = `${title} · 小学数学知识地图`;
  setHash('#/');
}

function goHome() {
  $('#detailView').hidden = true;
  $('#app').hidden = false;
  document.title = '小学数学知识地图';
  setHash('#/');
  if ($('#q').value.trim()) {
    runSearch();
  } else {
    showMap();
  }
  scrollToY(restoreY || 0, true);
  restoreY = 0;
}

function showMap() {
  $('#app').hidden = false;
  $('#detailView').hidden = true;
  $('#hero').hidden = false;
  $('#gradeNav').hidden = false;
  $('.toolbar').hidden = false;
  $('#boards').hidden = false;
  $('.review-panel').hidden = false;
  $('.exam-home').hidden = false;
  $('#searchPanel').hidden = true;
  $('#searchPanel').innerHTML = '';
  refreshReviewUI();
  applyFilter();
}

function runSearch() {
  const q = $('#q').value.trim().toLowerCase();
  $('#clearSearch').hidden = !$('#q').value;
  if (!q) { showMap(); return; }
  $('#app').hidden = false;
  $('#detailView').hidden = true;
  $('#hero').hidden = true;
  $('#gradeNav').hidden = true;
  $('.toolbar').hidden = true;
  $('#boards').hidden = true;
  $('.review-panel').hidden = true;
  $('.exam-home').hidden = true;
  $('#searchPanel').hidden = false;
  const hits = [];
  BOARDS.forEach((b, order) => {
    for (const dm of b.domains) {
      for (const t of dm.topics) {
        const d = t.content ? DATA_BY_ID[t.content] : null;
        if (currentFilter === 'online' && !d) continue;
        if (currentFilter === 'soon' && d) continue;
        if (onlyUnreviewed && d && viewCount(d.id) > 0) continue;
        const title = t.title.toLowerCase();
        const hay = [t.title, b.label, dm.name, t.term || '', d ? (d.text || '') : '',
                     d ? (d.tags || []).join(' ') : ''].join(' ').toLowerCase();
        let score = 0;
        if (title === q) score = 120;
        else if (title.includes(q)) score = 100;
        else if ((d ? (d.tags || []) : []).some(x => x.toLowerCase().includes(q))) score = 60;
        else if (dm.name.toLowerCase().includes(q) || b.label.toLowerCase().includes(q)) score = 30;
        else if (hay.includes(q)) score = 10;
        if (score) hits.push({ b, dm, t, d, score, order });
      }
    }
  });
  hits.sort((a, b) => b.score - a.score || a.order - b.order);
  $('#searchPanel').innerHTML = `<div class="search-head"><h2>搜索结果</h2><span>${hits.length} 个知识点</span></div>` +
    (hits.length ? hits.map(hitHTML).join('') :
      `<p class="empty">没有找到与“${esc(q)}”相关的知识点，试试“分数”“面积”或“数论”。</p>`);
  scrollToY(0, true);
}

function hitHTML({ b, dm, t, d }) {
  return `<button class="hit" data-content="${esc(t.content || '')}"
      data-board="${esc(b.key)}" data-domain="${esc(dm.name)}"
      data-title="${esc(t.title)}" onclick="openTopic(this)">
    <span class="hit-main">
      <span class="hit-title">${esc(t.title)}</span>
      <span class="hit-meta">${esc(b.label)} · ${esc(dm.name)}${t.term ? ' · ' + t.term + '册' : ''}${d ? ' · 难度 ' + stars(d.difficulty) + ' · ' + reviewLabel(d.id) : ''}</span>
    </span>
    <span class="status ${d ? 'ready' : 'soon'}">${d ? '更新 ' + (d.updated ? d.updated.slice(5) : '已更新') : '待补充'}</span>
  </button>`;
}

function jump(key, instant) {
  if ($('#q').value.trim()) {
    $('#q').value = '';
    $('#clearSearch').hidden = true;
    showMap();
  }
  const el = document.getElementById('board-' + key);
  if (el && !el.hidden) {
    const y = el.getBoundingClientRect().top + window.scrollY - 128;
    scrollToY(y, !!instant);
  }
  $$('.grade-tab').forEach(b => b.classList.toggle('active', b.dataset.key === key));
  setHash('#/grade/' + key);
}

function setFilter(f) {
  currentFilter = f;
  $$('.seg button').forEach(b => b.classList.toggle('on', b.dataset.f === f));
  if ($('#q').value.trim()) runSearch();
  else applyFilter();
}

function applyFilter() {
  $$('#boards .topic').forEach(el => {
    const ready = el.classList.contains('ready');
    const viewed = el.dataset.content ? viewCount(el.dataset.content) : 0;
    el.hidden = (currentFilter === 'online' && !ready) || (currentFilter === 'soon' && ready) ||
                (onlyUnreviewed && viewed > 0);
  });
  $$('#boards .domain').forEach(dm => {
    const topics = Array.from(dm.querySelectorAll('.topic'));
    const shown = topics.filter(t => !t.hidden).length;
    const n = dm.querySelector('.n');
    if (n) n.textContent = shown;
    dm.hidden = topics.length > 0 && shown === 0;
  });
  $$('#boards .board').forEach(bd => {
    const domains = Array.from(bd.querySelectorAll('.domain'));
    bd.hidden = domains.length > 0 && domains.every(d => d.hidden);
  });
  const visible = $$('#boards .board').filter(b => !b.hidden).length;
  const empty = $('#emptyFilter');
  if (empty) empty.hidden = visible > 0 || $('#boards').hidden;
}


function setOnlyUnreviewed(value) {
  onlyUnreviewed = !!value;
  if ($('#q').value.trim()) runSearch();
  else applyFilter();
}

function refreshReviewUI() {
  const total = Object.values(VIEWS).reduce((sum, n) => sum + (Number(n) || 0), 0);
  const reviewed = Object.keys(VIEWS).filter(id => viewCount(id) > 0).length;
  const top = Object.entries(VIEWS).filter(([, n]) => Number(n) > 0)
    .sort((a, b) => Number(b[1]) - Number(a[1]))[0];
  const rawRate = STATS.total ? reviewed / STATS.total * 100 : 0;
  const rate = reviewed ? Math.max(1, Math.round(rawRate)) : 0;
  const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
  set('reviewTotal', total);
  set('reviewedCount', reviewed);
  set('reviewRate', rate + '%');
  set('reviewTop', top ? (DATA_BY_ID[top[0]]?.title || '—') : '—');
  const bar = document.getElementById('reviewBar');
  if (bar) bar.style.width = rawRate + '%';
  set('reviewHint', `已复习 ${reviewed} / ${STATS.total} 个知识点 · 统计保存在本机浏览器`);
  $$('.view-badge[data-view]').forEach(badge => {
    const n = viewCount(badge.dataset.view);
    badge.textContent = n ? `复习 ${n} 次` : '未复习';
    badge.classList.toggle('has', n > 0);
  });
}

function resetViews() {
  if (!confirm('确定清空全部复习统计吗？此操作不可撤销。')) return;
  VIEWS = {};
  saveViews();
  refreshReviewUI();
  const chip = document.getElementById('reviewChip');
  if (chip) chip.textContent = '已复习 0 次';
  applyFilter();
}

window.addEventListener('storage', event => {
  if (event.key !== VIEW_KEY) return;
  VIEWS = loadViews();
  refreshReviewUI();
  applyFilter();
});


function observeBoards() {
  if (observer) observer.disconnect();
  if (!('IntersectionObserver' in window)) return;
  observer = new IntersectionObserver(entries => {
    const visible = entries.filter(e => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    const key = visible.target.id.replace('board-', '');
    $$('.grade-tab').forEach(b => b.classList.toggle('active', b.dataset.key === key));
  }, { rootMargin: '-130px 0px -55% 0px', threshold: [0, .1, .5] });
  $$('.board').forEach(el => observer.observe(el));
}

function renderMath(root) {
  if (!window.renderMathInElement) return;
  try {
    window.renderMathInElement(root, { delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '$', right: '$', display: false }
    ] });
  } catch (e) { /* KaTeX 尚未就绪时由 load 事件补渲染 */ }
}

function toast(msg) {
  const el = $('#toast');
  el.textContent = msg;
  el.classList.add('on');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('on'), 1800);
}

function route() {
  const h = decodeURIComponent(location.hash.replace(/^#/, ''));
  if (h.startsWith('/topic/')) {
    const id = h.slice('/topic/'.length);
    if (DATA_BY_ID[id]) { openContent(id); return; }
  }
  if (h.startsWith('/grade/')) {
    goHome();
    const key = h.slice('/grade/'.length);
    setTimeout(() => jump(key, true), 0);
    return;
  }
  goHome();
}

$('#q').addEventListener('input', () => {
  const v = $('#q').value;
  $('#clearSearch').hidden = !v;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { if (v.trim()) runSearch(); else showMap(); }, 120);
});
$('#clearSearch').addEventListener('click', () => {
  $('#q').value = '';
  $('#clearSearch').hidden = true;
  showMap();
  $('#q').focus();
});
document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    $('#q').focus();
  }
  if (e.key === 'Escape') {
    if ($('#q').value) {
      $('#q').value = '';
      $('#clearSearch').hidden = true;
      showMap();
    } else if (!$('#detailView').hidden) {
      goHome();
    }
  }
});
window.addEventListener('hashchange', route);
window.addEventListener('load', () => {
  if (!$('#detailView').hidden) renderMath($('#detailView'));
});

renderIndex();
if (location.hash && location.hash !== '#/') route();
else showMap();
</script>
"""
