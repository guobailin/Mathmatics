// utils/data.js —— 数据加载层：manifest + 按模块懒加载 JSON
const manifest = require('../data/manifest.json');

const moduleCache = {};

function getModules() {
  return manifest; // [{slug, module, count, file}]
}

function getModuleKps(slug) {
  if (!moduleCache[slug]) {
    moduleCache[slug] = require('../data/' + slug + '.json');
  }
  return moduleCache[slug];
}

function getKp(id) {
  for (const m of manifest) {
    const hit = getModuleKps(m.slug).find(k => k.id === id);
    if (hit) return hit;
  }
  return null;
}

function search(keyword) {
  const kw = keyword.trim();
  if (!kw) return [];
  const hits = [];
  for (const m of manifest) {
    for (const k of getModuleKps(m.slug)) {
      const text = [k.title, k.module, ...(k.tags || []), ...(k.skills || []),
        k.lecture, ...k.examples.map(e => e.problem)].join(' ');
      if (text.includes(kw)) hits.push(k);
    }
  }
  return hits;
}

module.exports = { getModules, getModuleKps, getKp, search };
