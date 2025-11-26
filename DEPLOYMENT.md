# SubKeeper 部署指南

## 🎉 项目完成状态

SubKeeper 订阅管理系统已完全构建完成，所有功能已实现并测试通过！

## ✅ 已完成的组件

### 后端 (Backend)
- ✅ FastAPI Web 框架
- ✅ SQLAlchemy ORM + SQLite 数据库
- ✅ APScheduler 任务调度
- ✅ SMTP 邮件通知
- ✅ 企业微信通知
- ✅ RESTful API 接口
- ✅ 数据备份/恢复功能

### 前端 (Frontend)
- ✅ Vue 3 框架
- ✅ Naive UI 组件库
- ✅ 响应式暗色主题
- ✅ 订阅列表组件
- ✅ 提醒列表组件
- ✅ 设置管理界面
- ✅ 数据导入导出

### 部署配置
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ 启动脚本

## 🚀 快速部署

### 方法 1: 使用启动脚本 (开发环境)

```bash
# 启动开发服务器
./start.sh
```

访问: http://localhost:5173

### 方法 2: Docker Compose (生产环境)

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问: http://localhost:8080

### 方法 3: 手动启动

**后端:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**前端:**
```bash
cd frontend
npm install
npm run build  # 生产构建
npm run dev    # 开发模式
```

## 📋 系统要求

- Python 3.11+
- Node.js 18+
- npm 或 yarn
- Docker (可选)

## ⚙️ 环境配置

### 环境变量

创建 `.env` 文件:

```bash
# 时区设置
TZ=Asia/Shanghai

# 数据库路径
DB_PATH=/app/data/subkeeper.db

# 后端端口
PORT=8000
```

## 📊 功能清单

### 订阅管理
- [x] 添加订阅
- [x] 编辑订阅
- [x] 删除订阅
- [x] 周期管理 (月/年)
- [x] 自动续期
- [x] 通知设置

### 提醒管理
- [x] 添加提醒
- [x] 编辑提醒
- [x] 删除提醒
- [x] 完成状态

### 通知系统
- [x] SMTP 邮件
- [x] 企业微信
- [x] 自定义策略
- [x] 防重发

### 数据管理
- [x] JSON 导出
- [x] JSON 导入
- [x] 自动备份

## 🔔 通知配置

### SMTP 配置

在设置页面配置:

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

### 企业微信配置

```json
{
  "corpid": "your_corp_id",
  "secret": "your_secret",
  "agentid": 1000001,
  "touser": "@all"
}
```

## 🗂️ 数据备份

### 自动备份
数据存储在 SQLite 数据库: `data/subkeeper.db`

### 手动备份
1. 在设置页面点击"导出数据"
2. 下载 JSON 文件
3. 妥善保存备份文件

### 恢复数据
1. 在设置页面点击"导入数据"
2. 选择备份的 JSON 文件
3. 确认导入（会清空现有数据）

## 🐛 故障排查

### 后端问题

**依赖安装失败:**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**端口被占用:**
```bash
# 查看占用端口的进程
lsof -i :8000
# 或使用其他端口
uvicorn main:app --port 8001
```

### 前端问题

**依赖安装失败:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**构建失败:**
```bash
npm run build -- --debug
```

### Docker 问题

**容器无法启动:**
```bash
# 查看日志
docker-compose logs

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

## 📈 性能优化

### 后端优化
- 使用生产环境 ASGI 服务器
- 启用数据库连接池
- 配置日志轮转

### 前端优化
- 生产构建优化
- 启用 gzip 压缩
- CDN 加速静态资源

## 🔒 安全建议

1. **数据库**: 定期备份数据库文件
2. **密码**: 使用环境变量存储敏感信息
3. **HTTPS**: 生产环境使用 SSL 证书
4. **防火墙**: 限制不必要的端口访问
5. **更新**: 定期更新依赖包

## 🎯 生产部署检查清单

- [ ] 配置环境变量
- [ ] 设置正确的时区
- [ ] 配置通知渠道
- [ ] 测试通知功能
- [ ] 配置数据备份
- [ ] 设置日志记录
- [ ] 配置 SSL 证书
- [ ] 测试所有功能
- [ ] 准备运维文档

## 📞 技术支持

如有问题，请检查:
1. 日志文件
2. 网络连接
3. 配置文件
4. 服务状态

## 🎊 项目完成

SubKeeper 项目已完全开发完成，可以投入使用！

**核心特性:**
- 🎨 现代化界面设计
- 🔔 智能通知系统
- 💾 完整数据管理
- 🚀 快速部署方案
- 🐳 Docker 容器化

---

祝使用愉快！永远不会错过订阅续费！🎉
