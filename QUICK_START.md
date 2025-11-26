# SubKeeper 快速启动指南

## ✅ 项目已完成

SubKeeper 订阅管理系统已经完成开发，所有核心功能已实现并可以运行！

## 🚀 快速启动

### 方式一：一键启动（推荐）

```bash
./start.sh
```

这个脚本会自动：
- 检查后端虚拟环境
- 安装前端依赖（如果需要）
- 启动后端服务（端口 8000）
- 启动前端服务（端口 5173）

访问地址：
- 🎨 前端界面：http://localhost:5173
- 🔧 后端 API：http://localhost:8000
- 📚 API 文档：http://localhost:8000/docs

按 `Ctrl+C` 停止所有服务

### 方式二：分别启动

**启动后端：**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端（新终端）：**
```bash
cd frontend
npm run dev
```

### 方式三：Docker 部署

```bash
docker-compose up -d
```

访问：http://localhost:8080

## 📋 功能清单

### ✅ 已实现功能

1. **订阅管理**
   - ✅ 添加/编辑/删除订阅
   - ✅ 设置周期（月度/年度）
   - ✅ 自动计算下次扣款日期
   - ✅ 全局或自定义通知策略
   - ✅ 通知模式标识（🌍 默认 / ⚙️ 自定义）

2. **提醒管理**
   - ✅ 添加/编辑/删除一次性提醒
   - ✅ 设置具体日期和时间
   - ✅ 完成状态标记

3. **通知系统**
   - ✅ SMTP 邮件通知
   - ✅ 企业微信通知
   - ✅ 每分钟检查待发送通知
   - ✅ 防重发机制（同一天只发一次）
   - ✅ 自定义通知时间和天数

4. **数据管理**
   - ✅ JSON 格式导出
   - ✅ JSON 格式导入
   - ✅ SQLite 数据持久化

5. **界面设计**
   - ✅ 暗色主题
   - ✅ 响应式布局
   - ✅ 左右分栏（订阅列表 + 待办提醒）
   - ✅ 模态框编辑

## ⚙️ 首次使用配置

### 1. 配置通知渠道

点击右上角的设置按钮 ⚙️，在设置页面配置通知方式：

**SMTP 邮件配置示例：**
```json
{
  "host": "smtp.gmail.com",
  "port": 587,
  "username": "your-email@gmail.com",
  "password": "your-app-password",
  "from": "your-email@gmail.com",
  "to": "recipient@example.com",
  "use_tls": true
}
```

**企业微信配置示例：**
```json
{
  "corpid": "your_corp_id",
  "secret": "your_secret",
  "agentid": 1000001,
  "touser": "@all"
}
```

### 2. 设置默认通知策略

在"默认策略"选项卡中设置：
- **默认通知时间**：例如 09:00
- **默认提醒天数**：例如 3,1,0（提前3天、1天和当天）

### 3. 添加订阅

1. 点击"订阅列表"下的"+ 添加订阅"按钮
2. 填写服务名称、价格、周期等信息
3. 选择通知设置：
   - **跟随默认**：使用全局设置
   - **自定义**：为该订阅设置独立的通知策略

### 4. 添加提醒

1. 点击"待办提醒"下的"+ 添加提醒"按钮
2. 填写标题、日期和时间
3. 保存即可

## 🏗️ 项目结构

```
subkeeper/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── models.py       # 数据库模型
│   │   ├── schemas.py      # Pydantic 模型
│   │   ├── database.py     # 数据库配置
│   │   ├── scheduler.py    # APScheduler 调度
│   │   ├── notifier.py     # 通知服务
│   │   └── routes/         # API 路由
│   ├── main.py             # 应用入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── App.vue         # 主组件
│   │   └── main.js         # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js      # Vite 配置
├── Dockerfile              # Docker 镜像
├── docker-compose.yml      # Docker Compose 配置
├── start.sh               # 启动脚本
└── README.md              # 项目说明
```

## 📦 技术栈

**后端：**
- Python 3.13
- FastAPI 0.122.0
- SQLAlchemy 2.0.44
- APScheduler 3.11.1
- Requests（邮件和微信通知）

**前端：**
- Vue 3.5.25
- Naive UI 2.43.2
- Vite 7.2.4
- Axios 1.13.2

## 🔧 核心机制

### 通知调度

1. **每分钟检查**（Cron: `* * * * *`）
   - 遍历所有订阅和提醒
   - 检查是否需要发送通知
   - 防止重复发送

2. **每日续期**（每日 00:01）
   - 检查过期订阅
   - 自动计算下次扣款日期

### 通知策略

- **全局模式**：所有订阅使用统一配置
- **自定义模式**：单个订阅独立配置

## 🎯 使用场景

1. **订阅服务管理**
   - Netflix、Spotify 等流媒体订阅
   - 域名、服务器续费提醒
   - 会员服务到期提醒

2. **待办事项**
   - 重要日期提醒
   - 会议和活动通知
   - 临时任务提醒

## 📝 注意事项

1. **时区设置**：确保环境变量 `TZ=Asia/Shanghai` 正确设置
2. **数据备份**：建议定期导出数据备份
3. **通知测试**：首次配置后建议添加测试订阅验证通知功能
4. **端口占用**：确保 8000 和 5173 端口未被占用

## 🐛 常见问题

### Q: 后端启动失败？
A: 检查 Python 虚拟环境是否正确安装：
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Q: 前端无法访问后端 API？
A: 检查 `frontend/vite.config.js` 中的 proxy 配置是否正确

### Q: 通知没有发送？
A: 
1. 检查通知配置是否正确
2. 查看后端日志输出
3. 确认订阅的提醒日期和时间设置

### Q: Docker 部署失败？
A: 确保 Docker 和 Docker Compose 已正确安装

## 🎉 项目完成状态

- ✅ 后端 API 完整实现
- ✅ 前端界面完整实现
- ✅ 通知功能完整实现
- ✅ 数据备份功能完整实现
- ✅ Docker 部署配置完成
- ✅ 文档完整

**项目已可以正常使用！**

---

如有问题或建议，欢迎反馈！
