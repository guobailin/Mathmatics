const { search } = require('../../utils/data.js');

Page({
  data: { kw: '', hits: [], searched: false },
  onInput(e) { this.setData({ kw: e.detail.value }); },
  onSearch() {
    this.setData({ hits: search(this.data.kw), searched: true });
  },
  goDetail(e) {
    wx.navigateTo({ url: '/pages/detail/detail?id=' + e.currentTarget.dataset.id });
  }
});
