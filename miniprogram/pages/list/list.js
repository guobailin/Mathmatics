const { getModuleKps } = require('../../utils/data.js');

Page({
  data: { kps: [], filtered: [], grades: [], diff: 0, grade: 0 },
  onLoad(opts) {
    const kps = getModuleKps(opts.slug);
    const grades = [...new Set(kps.flatMap(k => k.grade))].sort();
    this.setData({ kps, filtered: kps, grades });
    wx.setNavigationBarTitle({ title: decodeURIComponent(opts.name || '知识点') });
  },
  pickGrade(e) {
    const grade = +e.currentTarget.dataset.g;
    this.setData({ grade }, this.applyFilter);
  },
  pickDiff(e) {
    const diff = +e.currentTarget.dataset.d;
    this.setData({ diff }, this.applyFilter);
  },
  applyFilter() {
    const { kps, grade, diff } = this.data;
    this.setData({
      filtered: kps.filter(k =>
        (!grade || k.grade.includes(grade)) && (!diff || k.difficulty === diff))
    });
  },
  goDetail(e) {
    wx.navigateTo({ url: '/pages/detail/detail?id=' + e.currentTarget.dataset.id });
  }
});
