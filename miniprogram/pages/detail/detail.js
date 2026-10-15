const { getKp } = require('../../utils/data.js');
const { mdToNodes } = require('../../utils/render.js');

const FAV_KEY = 'favorites';

Page({
  data: { kp: null, lectureNodes: [], examples: [], fav: false },
  onLoad(opts) {
    const kp = getKp(opts.id);
    if (!kp) { wx.showToast({ title: '知识点不存在', icon: 'none' }); return; }
    const examples = kp.examples.map(e => ({
      ...e,
      open: false,
      problemNodes: mdToNodes(e.problem),
      analysisNodes: mdToNodes(e.analysis + '\n\n**答案**：' + e.answer)
    }));
    const favs = wx.getStorageSync(FAV_KEY) || [];
    this.setData({
      kp,
      lectureNodes: mdToNodes(kp.lecture),
      examples,
      fav: favs.includes(kp.id)
    });
    wx.setNavigationBarTitle({ title: kp.title });
  },
  toggleAnswer(e) {
    const i = e.currentTarget.dataset.i;
    this.setData({ [`examples[${i}].open`]: !this.data.examples[i].open });
  },
  toggleFav() {
    const favs = wx.getStorageSync(FAV_KEY) || [];
    const id = this.data.kp.id;
    const idx = favs.indexOf(id);
    if (idx >= 0) favs.splice(idx, 1); else favs.push(id);
    wx.setStorageSync(FAV_KEY, favs);
    this.setData({ fav: idx < 0 });
    wx.showToast({ title: idx < 0 ? '已收藏' : '已取消', icon: 'none' });
  }
});
