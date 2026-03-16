const app = typeof getApp === 'function' ? getApp() : null
const { API_BASE } = require('../config/api')

function getBase() {
  if (app && app.globalData && app.globalData.apiBase) return app.globalData.apiBase
  return API_BASE
}

function getAuthHeader() {
  const token = (app && app.globalData && app.globalData.token) || wx.getStorageSync('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

function request({ url, method = 'GET', data = {}, auth = true }) {
  const base = getBase()
  const header = {
    'Content-Type': 'application/json',
    ...(auth ? getAuthHeader() : {})
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${base}${url}`,
      method,
      header,
      data,
      success: (res) => {
        if (res.statusCode === 401 && auth) {
          wx.reLaunch({ url: '/pages/login/index' })
          return
        }
        resolve(res)
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

module.exports = {
  request
}

