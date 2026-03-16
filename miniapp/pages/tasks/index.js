Page({
  data: {
    tasks: [
      { id: 1, name: '和孩子说 3 次感谢的话', done: false },
      { id: 2, name: '一起读 1 本绘本', done: false },
      { id: 3, name: '睡前 5 分钟聊今天', done: true }
    ]
  },

  onToggleDone(e) {
    const id = e.currentTarget.dataset.id;
    console.log('click task', id);
    wx.showToast({ title: '仅示意，未接入后端', icon: 'none' });
  }
});

