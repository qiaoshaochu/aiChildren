const app = getApp()

Page({
  data: {
    stats: {
      days: 0,
      interactionDays: 0,
      readingDays: 0
    },
    aiSummary: '',
    teacherData: [],
    parentData: [],
    peerReference: {}
  },

  onShow() {
    this.fetchDashboard()
  },

  fetchDashboard() {
    const token = app.globalData.token || wx.getStorageSync('token')
    const header = token ? { Authorization: `Bearer ${token}` } : {}

    wx.request({
      url: `${app.globalData.apiBase}/api/dashboard`,
      method: 'GET',
      header,
      success: (res) => {
        if (res.statusCode === 200) {
          const teacher = res.data.teacherData || []
          const parent = res.data.parentData || []
          const aiSummary = res.data.aiSummary || ''
          const peer = res.data.peerReference || {}

          const daysSet = new Set()
          let interactionDays = 0
          let readingDays = 0
          parent.forEach((p) => {
            daysSet.add(p.date)
            if (p.interaction) interactionDays += 1
            if (p.reading) readingDays += 1
          })

          this.setData({
            stats: {
              days: daysSet.size || teacher.length || 0,
              interactionDays,
              readingDays
            },
            aiSummary,
            teacherData: teacher,
            parentData: parent,
            peerReference: peer
          })
        } else if (res.statusCode === 401) {
          wx.reLaunch({ url: '/pages/login/index' })
        }
      },
      fail: () => {
        wx.showToast({ title: '数据加载失败', icon: 'none' })
      },
      complete: () => {
        wx.stopPullDownRefresh()
      }
    })
  },

  onPullDownRefresh() {
    this.fetchDashboard()
  }
})