const app = getApp()

Page({
  data: {
    todayTasks: [],
    todayClass: null,
    weekSummary: '',
    displayName: '家长',
    todayText: '',
    weekday: '',
    taskBadge: '任务',
    streakDays: 0,
    growthIndex: 82,
    banners: []
  },

  onShow() {
    const user = app.globalData.user || wx.getStorageSync('user')
    if (!user) {
      wx.reLaunch({ url: '/pages/login/index' })
      return
    }
    app.globalData.user = user
    const weekdayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const now = new Date()
    this.setData({
      displayName: (user && user.username) ? user.username : '家长',
      todayText: this.formatToday(now),
      weekday: weekdayNames[now.getDay()]
    })
    this.initBanners()
    this.fetchHome()
    this.fetchCheckin()
  },

  formatToday(d) {
    const date = d || new Date()
    const m = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${m}.${day}`
  },

  initBanners() {
    this.setData({
      banners: [
        {
          id: 1,
          title: '今日陪伴建议',
          desc: '找 3 个生活中的圆形，一起说出它们的名字。',
          tag: '预计 10 分钟'
        },
        {
          id: 2,
          title: 'AI 成长提醒',
          desc: '本周亲子互动较稳定，适合增加 1 次绘本共读。',
          tag: '建议增加绘本共读'
        },
        {
          id: 3,
          title: '热门 Busybook',
          desc: '动物换装主题，2-4 岁孩子最爱模仿的小剧场。',
          tag: '2-4 岁最受欢迎'
        }
      ]
    })
  },

  fetchHome() {
    const token = app.globalData.token || wx.getStorageSync('token')
    const header = token ? { Authorization: `Bearer ${token}` } : {}
    wx.request({
      url: `${app.globalData.apiBase}/api/home`,
      method: 'GET',
      header,
      success: (res) => {
        if (res.statusCode === 200) {
          const tasks = res.data.todayTasks || []
          this.setData({
            todayTasks: tasks,
            todayClass: res.data.todayClass,
            weekSummary: res.data.weekSummary || '',
            taskBadge: tasks.length ? `共 ${tasks.length} 个` : '暂无'
          })
        } else if (res.statusCode === 401) {
          wx.reLaunch({ url: '/pages/login/index' })
        }
      },
      fail: () => {
        wx.showToast({ title: '加载失败', icon: 'none' })
      }
    })
  },

  fetchCheckin() {
    const token = app.globalData.token || wx.getStorageSync('token')
    const header = token ? { Authorization: `Bearer ${token}` } : {}
    wx.request({
      url: `${app.globalData.apiBase}/api/checkin`,
      method: 'GET',
      header,
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            streakDays: res.data.streak || 0
          })
        }
      }
    })
  },

  goDashboard() {
    wx.navigateTo({ url: '/pages/dashboard/index' })
  },

  goParentRecord() {
    wx.navigateTo({ url: '/pages/parent-record/index' })
  },

  goBusybook() {
    wx.navigateTo({ url: '/pages/busybook-list/index' })
  },

  goCheckin() {
    wx.navigateTo({ url: '/pages/checkin/index' })
  }
})

