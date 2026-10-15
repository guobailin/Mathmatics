// utils/render.js —— 把知识点 Markdown 子集渲染成 rich-text 节点
// 支持：##/### 标题、段落、- 列表、**加粗**、$..$ / $$..$$ 公式（样式化文本）、表格（简化为行文本）

function inlineNodes(text) {
  // 先切 $$..$$ 与 $..$，再切 **加粗**
  const nodes = [];
  const mathRe = /\$\$([^$]+)\$\$|\$([^$]+)\$/g;
  let last = 0, m;
  const pushText = (t) => {
    if (!t) return;
    // 处理加粗
    const boldRe = /\*\*([^*]+)\*\*/g;
    let l2 = 0, m2;
    while ((m2 = boldRe.exec(t)) !== null) {
      if (m2.index > l2) nodes.push({ type: 'text', text: t.slice(l2, m2.index) });
      nodes.push({ name: 'span', attrs: { style: 'font-weight:bold;' }, children: [{ type: 'text', text: m2[1] }] });
      l2 = m2.index + m2[0].length;
    }
    if (l2 < t.length) nodes.push({ type: 'text', text: t.slice(l2) });
  };
  while ((m = mathRe.exec(text)) !== null) {
    if (m.index > last) pushText(text.slice(last, m.index));
    const tex = (m[1] || m[2] || '').trim();
    nodes.push({
      name: 'span',
      attrs: { style: 'font-family:monospace;background:#f0f4ff;border-radius:4px;padding:0 6px;color:#1a3a8f;' },
      children: [{ type: 'text', text: tex }]
    });
    last = m.index + m[0].length;
  }
  if (last < text.length) pushText(text.slice(last));
  return nodes;
}

function mdToNodes(md) {
  const lines = md.split('\n');
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    // 表格：连续以 | 开头的行
    if (/^\s*\|/.test(line)) {
      const rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) {
        const cells = lines[i].split('|').slice(1, -1).map(s => s.trim());
        if (!/^[-\s:]+$/.test(cells.join(''))) rows.push(cells); // 跳过分隔行
        i++;
      }
      rows.forEach(r => {
        blocks.push({
          name: 'p',
          attrs: { style: 'margin:2px 0;font-size:14px;' },
          children: inlineNodes(r.join('　|　'))
        });
      });
      continue;
    }
    // 标题
    const h = /^(#{1,4})\s+(.*)$/.exec(line);
    if (h) {
      const size = { 1: '20px', 2: '18px', 3: '16px', 4: '15px' }[h[1].length];
      blocks.push({
        name: 'p',
        attrs: { style: `font-size:${size};font-weight:bold;margin:12px 0 6px;` },
        children: inlineNodes(h[2])
      });
      i++; continue;
    }
    // 列表
    if (/^\s*[-*]\s+/.test(line)) {
      blocks.push({
        name: 'p',
        attrs: { style: 'margin:2px 0 2px 16px;' },
        children: [{ type: 'text', text: '• ' }].concat(inlineNodes(line.replace(/^\s*[-*]\s+/, '')))
      });
      i++; continue;
    }
    // 普通段落：合并连续非空行
    let para = line;
    i++;
    while (i < lines.length && lines[i].trim() && !/^\s*([#\-*|]|\$\$)/.test(lines[i])) {
      para += ' ' + lines[i].trim(); i++;
    }
    blocks.push({ name: 'p', attrs: { style: 'margin:6px 0;line-height:1.8;' }, children: inlineNodes(para) });
  }
  return blocks;
}

module.exports = { mdToNodes };
