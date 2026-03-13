const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },

  onUsernameInput(e) {
    this.setData({ username: e.detail.value })
  },

  onPasswordInput(e) {
    this.setData({ password: e.detail.value })
  },

  onLoginTap() {
    const { username, password } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请填写用户名和密码', icon: 'none' })
      return
    }

    this.authWith(username, password)
  },

  // 一键体验：直接用固定账号“安安爸爸”
  onQuickLogin() {
    const username = '安安爸爸'
    const password = 'demo123'
    this.setData({ username, password })
    this.authWith(username, password)
  },

  authWith(username, password) {
    if (this.data.loading) return

    this.setData({ loading: true })

    // 先尝试注册，如果已存在则忽略错误，再登录
    const apiBase = app.globalData.apiBase

    const doLogin = () => {
      wx.request({
        url: `${apiBase}/api/auth/login`,
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        data: { username, password },
        success: (res) => {
          const ok = res.statusCode >= 200 && res.statusCode < 300 && res.data && res.data.user
          if (ok) {
            const user = res.data.user
            const token = res.data.token
            app.globalData.user = user
            app.globalData.token = token
            wx.setStorageSync('user', user)
            if (token) wx.setStorageSync('token', token)
            wx.showToast({ title: '登录成功', icon: 'success' })
            wx.reLaunch({ url: '/pages/home/index' })
          } else {
            const msg = (res.data && res.data.error) ? res.data.error : `登录失败 (${res.statusCode})`
            wx.showToast({ title: msg, icon: 'none' })
          }
        },
        fail: (err) => {
          const detail = err && err.errMsg ? err.errMsg : 'unknown'
          wx.showToast({
            title: `请求失败：${detail}\n检查后端是否启动、apiBase 是否正确、以及开发者工具是否已关闭“请求合法域名校验”`,
            icon: 'none',
            duration: 4000
          })
        },
        complete: () => {
          this.setData({ loading: false })
        }
      })
    }

    wx.request({
      url: `${apiBase}/api/auth/register`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: { username, password, role: 'parent' },
      fail: (err) => {
        const detail = err && err.errMsg ? err.errMsg : 'unknown'
        wx.showToast({
          title: `注册请求失败：${detail}\n检查后端是否启动、apiBase 是否正确、以及开发者工具是否已关闭“请求合法域名校验”`,
          icon: 'none',
          duration: 4000
        })
      },
      complete: () => {
        // 无论注册成功或失败，都尝试登录
        doLogin()
      }
    })
  }
})

