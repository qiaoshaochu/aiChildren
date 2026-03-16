const api = require('../../services/api')

Page({
  data: { child_id: '', record_date: '', category: '', value: '', notes: '', loading: false },
  onLoad(q) { if (q.child_id) this.setData({ child_id: q.child_id }) },
  onChildIdInput(e) { this.setData({ child_id: e.detail.value }) },
  onDateInput(e) { this.setData({ record_date: e.detail.value }) },
  onCategoryInput(e) { this.setData({ category: e.detail.value }) },
  onValueInput(e) { this.setData({ value: e.detail.value }) },
  onNotesInput(e) { this.setData({ notes: e.detail.value }) },
  onSubmit() {
    const { child_id, record_date, category, value, notes } = this.data
    if (!child_id.trim()) return wx.showToast({ title: '请填写孩子 ID', icon: 'none' })
    if (!category.trim()) return wx.showToast({ title: '请填写类别', icon: 'none' })
    if (!value.trim()) return wx.showToast({ title: '请填写内容', icon: 'none' })
    this.setData({ loading: true })
    const data = { child_id: child_id.trim(), category: category.trim(), value: value.trim() }
    if (record_date.trim()) data.record_date = record_date.trim()
    if (notes.trim()) data.notes = notes.trim()
    api.request({ url: '/api/records', method: 'POST', data, auth: false })
      .then(res => {
        if (res.statusCode === 201) {
          wx.showToast({ title: '保存成功', icon: 'success' })
          setTimeout(() => wx.navigateBack(), 1500)
        } else if (res.data && res.data.error) wx.showToast({ title: res.data.error, icon: 'none' })
      })
      .catch(() => wx.showToast({ title: '请求失败', icon: 'none' }))
      .finally(() => this.setData({ loading: false }))
  }
})
