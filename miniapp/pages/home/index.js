const api = require('../../services/api')

Page({
  data: { list: [] },
  onShow() { this.loadList() },
  onPullDownRefresh() { this.loadList().then(() => wx.stopPullDownRefresh()) },
  loadList() {
    return api.request({ url: '/api/children', method: 'GET', auth: false })
      .then(res => {
        if (res.statusCode === 200) this.setData({ list: res.data || [] })
      })
      .catch(() => wx.showToast({ title: '加载失败', icon: 'none' }))
  },
  onChildTap(e) {
    const id = e.currentTarget.dataset.id
    if (id) wx.navigateTo({ url: `/pages/growth-report/index?child_id=${id}` })
  }
})
