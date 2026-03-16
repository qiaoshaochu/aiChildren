Page({
  data: {
    timeline: [
      { id: 1, date: '2025-03-01', text: '第一次完整说出颜色名称' },
      { id: 2, date: '2025-03-05', text: '和爸爸一起完成 BusyBook 贴纸' }
    ],
    records: [
      { id: 1, date: '2025-03-10', category: 'reading', value: '共读 1 本绘本' },
      { id: 2, date: '2025-03-09', category: 'interaction', value: '陪玩积木 20 分钟' }
    ]
  },

  onGrowthDataTap() {
    console.log('click growth data');
    wx.showToast({ title: '待接入数据看板', icon: 'none' });
  }
});

