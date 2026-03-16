const api = require('../../services/api')

Page({
  data: { name: '', birth_date: '', gender: '', loading: false },
  onNameInput(e) { this.setData({ name: e.detail.value }) },
  onBirthInput(e) { this.setData({ birth_date: e.detail.value }) },
  onGenderInput(e) { this.setData({ gender: e.detail.value }) },
  onSubmit() {
    const { name, birth_date, gender } = this.data
    if (!name.trim()) return wx.showToast({ title: '请填写姓名', icon: 'none' })
    this.setData({ loading: true })
    api.request({ url: '/api/children', method: 'POST', data: { name: name.trim(), birth_date: birth_date.trim() || undefined, gender: gender.trim() || undefined }, auth: false })
      .then(res => {
        if (res.statusCode === 201) {
          wx.showToast({ title: '添加成功', icon: 'success' })
          setTimeout(() => wx.navigateBack(), 1500)
        } else if (res.data && res.data.error) wx.showToast({ title: res.data.error, icon: 'none' })
      })
      .catch(() => wx.showToast({ title: '请求失败', icon: 'none' }))
      .finally(() => this.setData({ loading: false }))
  }
})
