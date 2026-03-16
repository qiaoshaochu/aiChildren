const api = require('../../services/api')

Page({
  data: {
    defaultChild: null,
    lastRecord: null
  },

  onShow() {
    this.loadHome()
  },

  onPullDownRefresh() {
    this.loadHome().then(() => wx.stopPullDownRefresh())
  },

  loadHome() {
    return api.request({ url: '/api/children', method: 'GET', auth: false })
      .then(res => {
        if (res.statusCode !== 200) return
        const list = res.data || []
        const defaultChild = list.length > 0 ? list[0] : null
        this.setData({ defaultChild })
        if (defaultChild) this.loadLastRecord(defaultChild.id)
        else this.setData({ lastRecord: null })
      })
      .catch(() => {
        wx.showToast({ title: '加载失败', icon: 'none' })
      })
  },

  loadLastRecord(childId) {
    return api.request({
      url: '/api/records',
      method: 'GET',
      data: { child_id: childId },
      auth: false
    }).then(res => {
      if (res.statusCode === 200 && Array.isArray(res.data) && res.data.length > 0) {
        this.setData({ lastRecord: res.data[0] })
      } else {
        this.setData({ lastRecord: null })
      }
    }).catch(() => {})
  }
})
