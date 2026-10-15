const { getKp } = require('../../utils/data.js');

const FAV_KEY = 'favorites';

Page({
  data: { list: [] },
  onShow() {
    const ids = wx.getStorageSync(FAV_KEY) || [];
    this.setData({ list: ids.map(getKp).filter(Boolean) });
  },
  goDetail(e) {
    wx.navigateTo({ url: '/pages/detail/detail?id=' + e.currentTarget.dataset.id });
  }
});
