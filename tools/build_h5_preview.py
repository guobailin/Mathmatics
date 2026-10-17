#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成小程序 H5 效果预览（近似版本）：单文件、内联数据，模拟手机界面。"""
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "miniprogram" / "data"
OUT_DIR = ROOT / "h5-preview"
KATEX_SRC = ROOT / "assets" / "katex"
os.makedirs(OUT_DIR, exist_ok=True)

manifest = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))
data = {}
for m in manifest:
    data[m["slug"]] = json.loads((DATA_DIR / f'{m["slug"]}.json').read_text(encoding="utf-8"))

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>小学数学知识库 · 小程序效果预览</title>
<link rel="stylesheet" href="katex/katex.min.css">
<script defer src="katex/katex.min.js"></script>
<script defer src="katex/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #2b2f36; font-family: -apple-system,"PingFang SC",sans-serif;
  display: flex; justify-content: center; padding: 24px 8px; }
.phone { width: 390px; max-width: 100%; background: #f5f6fa; border-radius: 28px;
  overflow: hidden; box-shadow: 0 12px 40px rgba(0,0,0,.4); min-height: 780px;
  display: flex; flex-direction: column; }
.navbar { background: #3b6ef6; color: #fff; padding: 14px 16px; font-weight: bold;
  display: flex; align-items: center; gap: 10px; position: sticky; top: 0; z-index: 9; }
.navbar .back { cursor: pointer; font-size: 18px; }
.content { flex: 1; overflow-y: auto; padding-bottom: 24px; }
.card { background: #fff; border-radius: 8px; padding: 14px; margin: 10px 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,.05); }
.badge { display: inline-block; background: #eef2ff; color: #3b6ef6; border-radius: 4px;
  padding: 0 6px; font-size: 11px; margin-right: 4px; }
.muted { color: #888; font-size: 12px; }
.search-box { background: #fff; border-radius: 16px; padding: 9px 14px; color: #999;
  font-size: 13px; margin: 10px 12px; cursor: pointer; }
.section-title { margin: 14px 14px 4px; font-weight: bold; font-size: 15px; }
.grid { display: flex; flex-wrap: wrap; padding: 0 6px; }
.grid-item { width: calc(50% - 12px); margin: 6px; background: #fff; border-radius: 8px;
  padding: 14px; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.05); }
.grid-name { font-weight: bold; font-size: 15px; }
.grid-count { font-size: 11px; color: #999; margin-top: 4px; }
.fav-entry { text-align: center; color: #f60; font-weight: bold; cursor: pointer; }
.chip { background: #fff; border: 1px solid #ddd; border-radius: 14px; padding: 4px 11px;
  font-size: 12px; margin: 0 6px 8px 0; color: #555; cursor: pointer; }
.chip.on { background: #3b6ef6; color: #fff; border-color: #3b6ef6; }
.filter { display: flex; flex-wrap: wrap; padding: 10px 12px 0; }
.item-title { font-weight: bold; font-size: 15px; margin-bottom: 4px; }
.clickable { cursor: pointer; }
.problem { background: #f7f8fc; border-radius: 6px; padding: 10px; margin: 8px 0;
  line-height: 1.8; font-size: 14px; }
.toggle { color: #3b6ef6; font-size: 13px; text-align: center; padding: 6px; cursor: pointer; }
.analysis { border-top: 1px dashed #ddd; padding-top: 8px; margin-top: 6px;
  line-height: 1.8; font-size: 14px; }
.answer { color: #b30; font-weight: bold; }
.fav { float: right; color: #f60; cursor: pointer; font-size: 13px; }
.bar { display: flex; padding: 10px 12px; background: #fff; gap: 8px; }
.bar input { flex: 1; background: #f0f1f5; border: none; border-radius: 14px;
  padding: 8px 12px; font-size: 13px; outline: none; }
.bar button { background: #3b6ef6; color: #fff; border: none; border-radius: 8px;
  padding: 0 14px; cursor: pointer; }
.empty { text-align: center; margin-top: 40px; color: #888; font-size: 13px;
  white-space: pre-line; }
.lecture { line-height: 1.9; font-size: 14px; }
.lecture h2, .lecture h3 { margin: 10px 0 6px; }
.math { font-family: monospace; background: #f0f4ff; border-radius: 4px;
  padding: 0 5px; color: #1a3a8f; font-size: 13px; }
.katex-src { font-family: monospace; background: #f0f4ff; border-radius: 4px;
  padding: 0 5px; color: #1a3a8f; font-size: 13px; }
.note { text-align: center; color: #666; font-size: 11px; padding: 8px 0 16px; }
</style></head><body>
<div class="phone">
  <div class="navbar"><span class="back" id="backBtn" style="display:none">‹</span><span id="navTitle">小学数学知识库</span></div>
  <div class="content" id="app"></div>
  <div class="note">H5 近似预览 · 真实小程序需安装微信开发者工具</div>
</div>
<script>
const MANIFEST = __MANIFEST__;
const DATA = __DATA__;
const ALL = Object.values(DATA).flat();
const FAV_KEY = 'mathkb_favs';
const $ = s => document.querySelector(s);
let history = [];
let state = { page: 'home' };

function esc(s){return (s||'').replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function renderMath(root){
  if (window.renderMathInElement && root) renderMathInElement(root,
    {delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]});
}
// 与小程序 render.js 相同的 Markdown 子集 → HTML（公式保留 LaTeX 供 KaTeX 渲染）
function md(text){
  let t = esc(text);
  t = t.replace(/\$\$([^$]+)\$\$/g, '<span class="katex-src">$$$$1$$</span>')
       .replace(/\$([^$]+)\$/g, '<span class="katex-src">$$$1$$</span>')
       .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
  return t.split('\n').map(l => l.trim()).filter(Boolean).map(l => {
    if (/^### /.test(l)) return '<h3>' + l.slice(4) + '</h3>';
    if (/^## /.test(l)) return '<h2>' + l.slice(3) + '</h2>';
    if (/^[-*] /.test(l)) return '<p style="margin-left:14px">• ' + l.slice(2) + '</p>';
    if (/^\|/.test(l)) return /^\|[\s\-|]+\|$/.test(l) ? '' :
      '<p style="font-size:13px">' + l.split('|').slice(1,-1).map(c=>c.trim()).join(' ｜ ') + '</p>';
    return '<p style="margin:4px 0">' + l + '</p>';
  }).join('');
}
function nav(title, showBack){
  $('#navTitle').textContent = title;
  $('#backBtn').style.display = showBack ? '' : 'none';
  $('#app').scrollTop = 0;
}
function go(page, params){ history.push({page: state.page, params: state.params}); state = {page, params}; render(); }
function back(){ const h = history.pop(); state = h || {page:'home'}; render(); }
$('#backBtn').onclick = back;

function stars(d){ return '★'.repeat(d); }
function kpCard(k){
  return `<div class="card clickable" onclick="go('detail',{id:'${k.id}'})">
    <div class="item-title">${esc(k.title)}</div>
    <div class="muted">${k.tags.map(t=>`<span class="badge">${esc(t)}</span>`).join('')}
      ${stars(k.difficulty)} · 年级 ${k.grade.join('/')} · ${k.examples.length} 道例题</div></div>`;
}
const pages = {
  home(){
    nav('小学数学知识库', false);
    $('#app').innerHTML = `
      <div style="background:#3b6ef6;padding:4px 0 10px"><div class="search-box" onclick="go('search')">🔍 搜索知识点、题目关键词…</div></div>
      <div class="section-title">📚 学习模块</div>
      <div class="grid">${MANIFEST.map(m=>`
        <div class="grid-item" onclick="go('list',{slug:'${m.slug}',name:'${esc(m.module)}'})">
          <div class="grid-name">${esc(m.module)}</div><div class="grid-count">${m.count} 个知识点</div></div>`).join('')}
      </div>
      <div class="card fav-entry" onclick="go('favs')">⭐ 我的收藏（标记薄弱知识点）</div>`;
  },
  list(){
    const {slug, name} = state.params;
    nav(name, true);
    const kps = DATA[slug];
    const grades = [...new Set(kps.flatMap(k=>k.grade))].sort();
    state.filter = state.filter || {grade:0, diff:0};
    const f = state.filter;
    const list = kps.filter(k => (!f.grade || k.grade.includes(f.grade)) && (!f.diff || k.difficulty===f.diff));
    $('#app').innerHTML = `
      <div class="filter"><span class="chip ${!f.grade?'on':''}" onclick="setF('grade',0)">全部年级</span>
        ${grades.map(g=>`<span class="chip ${f.grade===g?'on':''}" onclick="setF('grade',${g})">${g}年级</span>`).join('')}</div>
      <div class="filter"><span class="chip ${!f.diff?'on':''}" onclick="setF('diff',0)">全部难度</span>
        <span class="chip ${f.diff===1?'on':''}" onclick="setF('diff',1)">★ 基础</span>
        <span class="chip ${f.diff===2?'on':''}" onclick="setF('diff',2)">★★ 提高</span>
        <span class="chip ${f.diff===3?'on':''}" onclick="setF('diff',3)">★★★ 竞赛</span></div>
      ${list.map(kpCard).join('') || '<div class="empty">没有匹配的知识点</div>'}`;
  },
  detail(){
    const k = ALL.find(x => x.id === state.params.id);
    nav(k.title, true);
    const favs = JSON.parse(localStorage.getItem(FAV_KEY)||'[]');
    const isFav = favs.includes(k.id);
    $('#app').innerHTML = `
      <div class="card"><div class="item-title" style="font-size:18px">${esc(k.title)}</div>
        <div class="muted">${esc(k.module)} · ${stars(k.difficulty)} · 年级 ${k.grade.join('/')}
          <span class="fav" onclick="toggleFav('${k.id}')">${isFav?'★ 已收藏':'☆ 收藏'}</span></div>
        <div class="muted" style="margin-top:4px">子技能：${k.skills.map(s=>`<span class="badge">${esc(s)}</span>`).join('')}</div></div>
      <div class="card lecture"><div class="item-title">📖 讲解</div>${md(k.lecture)}</div>
      ${k.examples.map((e,i)=>`
        <div class="card"><div class="item-title">${esc(e.title)}</div>
          <div class="muted">覆盖点：${e.covers.map(esc).join('、')}</div>
          <div class="problem">${md(e.problem)}</div>
          <div class="toggle" onclick="const a=document.getElementById('a${i}');a.style.display=a.style.display==='none'?'':'none';this.textContent=a.style.display==='none'?'▼ 查看解析与答案':'▲ 收起解析'">▼ 查看解析与答案</div>
          <div class="analysis" id="a${i}" style="display:none">${md(e.analysis)}<p class="answer">答案：${md(e.answer)}</p></div>
        </div>`).join('')}`;
    renderMath($('#app'));
  },
  search(){
    nav('搜索', true);
    $('#app').innerHTML = `
      <div class="bar"><input id="kw" placeholder="如：质数、面积、鸡兔同笼" autofocus>
        <button onclick="doSearch()">搜索</button></div>
      <div id="results"></div>`;
    $('#kw').addEventListener('keydown', e => { if(e.key==='Enter') doSearch(); });
  },
  favs(){
    nav('我的收藏', true);
    const favs = JSON.parse(localStorage.getItem(FAV_KEY)||'[]');
    const list = favs.map(id => ALL.find(x=>x.id===id)).filter(Boolean);
    $('#app').innerHTML = list.map(kpCard).join('') ||
      '<div class="empty">还没有收藏。\n在知识点详情页点「☆ 收藏」，把薄弱知识点加到这里。</div>';
  }
};
window.setF = (k,v)=>{ state.filter[k]=v; pages.list(); };
window.toggleFav = (id)=>{ let f=JSON.parse(localStorage.getItem(FAV_KEY)||'[]');
  const i=f.indexOf(id); i>=0?f.splice(i,1):f.push(id);
  localStorage.setItem(FAV_KEY, JSON.stringify(f)); pages.detail(); };
window.doSearch = ()=>{
  const kw = $('#kw').value.trim(); if(!kw) return;
  const hits = ALL.filter(k => [k.title,k.module,...(k.tags||[]),...(k.skills||[]),k.lecture,
    ...k.examples.map(e=>e.problem)].join(' ').includes(kw));
  $('#results').innerHTML = hits.map(kpCard).join('') || `<div class="empty">没有找到「${esc(kw)}」相关的知识点</div>`;
};
window.go = go;
function render(){ pages[state.page](); }
// 支持 ?page=detail&id=xxx / ?page=list&slug=m08 / ?kw=关键词 直达，便于分享与截图
(function(){
  const q = new URLSearchParams(location.search);
  if (q.get('id')) state = {page:'detail', params:{id:q.get('id')}};
  else if (q.get('slug')) { const m = MANIFEST.find(x=>x.slug===q.get('slug'));
    state = {page:'list', params:{slug:q.get('slug'), name:m?m.module:''}}; }
  else if (q.get('kw')) { state = {page:'search'}; setTimeout(()=>{ const i=$('#kw'); if(i){i.value=q.get('kw'); doSearch();} },0); }
  render();
})();
</script></body></html>"""

html = HTML.replace("__MANIFEST__", json.dumps(manifest, ensure_ascii=False))
html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
out = OUT_DIR / "index.html"
out.write_text(html, encoding="utf-8")
shutil.copytree(KATEX_SRC, OUT_DIR / "katex", dirs_exist_ok=True)
print(f"OK {out} ({out.stat().st_size} bytes)")
