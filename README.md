本项目是一个给家长看的儿童成长产品原型，实现：

- 微信小程序前端（`miniapp`）
- Flask 后端 API（`backend`）
- 简单的用户名密码登录（后端 Session，前端存储 token）
- 核心 7 个页面（首页、数据看板、老师录入、家长记录、Busybook 列表与上传、打卡）

## 本地启动步骤

### 1. 后端（Flask）

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows 用 venv\\Scripts\\activate
pip install -r requirements.txt
flask --app app run --debug
```

默认地址：`http://127.0.0.1:5000`

### 2. 小程序

1. 打开微信开发者工具
2. 选择「导入项目」，目录选到 `miniapp`
3. AppID 可先用测试号 / 体验号，或填「无 AppID」
4. 在小程序端的接口基础地址统一配置为：`http://127.0.0.1:5000`

> 注意：实际真机/预览时，需配置合法域名与 HTTPS，这里只作为本地原型开发。

## 目录结构

- `backend/`：Flask 后端
  - `app.py`：主应用入口和 API 路由
  - `models.py`：简单的 SQLite 模型与封装
  - `auth.py`：登录、注册与用户会话
  - `requirements.txt`：Python 依赖
- `miniapp/`：微信小程序
  - `app.js` / `app.json` / `app.wxss`
  - `pages/home/`：首页（今日任务、课堂摘要、本周成长一句话）
  - `pages/dashboard/`：数据看板
  - `pages/teacher-input/`：老师录入
  - `pages/parent-record/`：家长记录
  - `pages/busybook-list/`：Busybook 列表
  - `pages/busybook-upload/`：Busybook 上传
  - `pages/checkin/`：打卡中心

## 后续可以扩展的方向

- 引入真实的微信登录（`wx.login` + 后端 openid 绑定）
- 真正接通大模型生成周总结与每日任务
- 完善角色权限（老师端、小程序家长端分离）
- 加入通知、定时提醒等

