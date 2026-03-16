Page({
  onChildManageTap() {
    console.log('click child manage');
    wx.showToast({ title: '跳转孩子管理（占位）', icon: 'none' });
  },
  onMyTasksTap() {
    console.log('click my tasks');
    wx.showToast({ title: '跳转我的任务（占位）', icon: 'none' });
  },
  onMyBusybookTap() {
    console.log('click my busybook');
    wx.showToast({ title: '跳转我的 BusyBook（占位）', icon: 'none' });
  },
  onSettingsTap() {
    console.log('click settings');
    wx.showToast({ title: '跳转设置（占位）', icon: 'none' });
  }
});

