Page({
  data: {
    works: [
      { id: 1, title: '形状 BusyBook - 圆形篇', age: '3 岁', likes: 12 },
      { id: 2, title: '颜色分类 BusyBook', age: '4 岁', likes: 28 }
    ]
  },

  onUploadTap() {
    console.log('click upload busybook');
    wx.showToast({ title: '上传逻辑待实现', icon: 'none' });
  }
});

