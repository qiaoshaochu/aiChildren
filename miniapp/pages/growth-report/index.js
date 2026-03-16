const api = require('../../services/api')

Page({
  data: { child_id: '', list: [] },
  onLoad(q) { this.setData({ child_id: q.child_id || '' }) },
  onShow() { if (this.data.child_id) this.loadList() },
  onPullDownRefresh() { this.loadList().then(() => wx.stopPullDownRefresh()) },
  loadList() {
    const cid = this.data.child_id
    if (!cid) return Promise.resolve()
    return api.request({ url: '/api/records', method: 'GET', data: { child_id: cid }, auth: false }).then(res => {
      if (res.statusCode === 200) this.setData({ list: res.data || [] })
    }).catch(() => wx.showToast({ title: '加载失败', icon: 'none' }))
  }
})
