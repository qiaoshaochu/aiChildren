App({
  globalData: {
    apiBase: 'http://127.0.0.1:5000',
    user: null,
    token: null
  },

  onLaunch() {
    const user = wx.getStorageSync('user')
    if (user) {
      this.globalData.user = user
    }
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.token = token
    }
  }
})

