# SubKeeper - 订阅管理系统

一个简单易用的订阅和待办管理系统，支持周期订阅、一次性提醒、双通道通知。

## 功能特性

- 📅 **周期订阅管理**: 管理各类订阅服务，自动计算下次扣款日期
- ⏰ **待办提醒**: 一次性提醒事项
- 📧 **双通道通知**: 支持邮件和企业微信通知
- ⚙️ **灵活配置**: 全局和自定义通知策略
- 💾 **数据备份**: JSON 格式导入导出

## 技术栈

- **前端**: Vue 3 + Naive UI
- **后端**: Python FastAPI
- **数据库**: SQLite
- **调度**: APScheduler
- **部署**: Docker

## 快速开始

### 使用 Docker Compose (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd subkeeper

# 启动服务
docker-compose up -d

# 访问应用
# http://localhost:8080
```

### 本地开发

#### 后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## 配置说明

### 环境变量

- `TZ`: 时区设置 (默认: Asia/Shanghai)
- `DB_PATH`: 数据库路径 (默认: /app/data/subkeeper.db)

### 通知配置

#### SMTP 邮件

```json
{
  "host": "smtp.example.com",
  "port": 587,
  "username": "your_email",
  "password": "your_password",
  "from": "sender@example.com",
  "to": "receiver@example.com",
  "use_tls": true
}
```

#### 企业微信

```json
{
  "corpid": "your_corpid",
  "secret": "your_secret",
  "agentid": 1000001,
  "touser": "@all"
}
```

## 数据备份

在设置页面中可以导出和导入数据，数据格式为 JSON。

## 许可证

MIT