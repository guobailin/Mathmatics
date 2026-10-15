const { getModules } = require('../../utils/data.js');

Page({
  data: { modules: [] },
  onLoad() {
    this.setData({ modules: getModules() });
  },
  goSearch() { wx.navigateTo({ url: '/pages/search/search' }); },
  goFavorites() { wx.navigateTo({ url: '/pages/favorites/favorites' }); },
  goList(e) {
    const { slug, name } = e.currentTarget.dataset;
    wx.navigateTo({ url: `/pages/list/list?slug=${slug}&name=${encodeURIComponent(name)}` });
  }
});
