# 认证功能说明

## 功能概述

SubKeeper 现已支持登录鉴权功能，采用 JWT (JSON Web Token) 进行身份验证。

## 配置说明

### 环境变量设置

在项目根目录创建 `.env` 文件，参考 `.env.example`：

```bash
# JWT 密钥（生产环境请修改）
JWT_SECRET_KEY=your-secret-key-change-this-in-production

# 管理员密码（必需）
ADMIN_PASSWORD=your-admin-password-here
```

### 重要说明

1. **ADMIN_PASSWORD** 是必需的环境变量，未设置时后端无法启动
2. **JWT_SECRET_KEY** 建议在生产环境中使用强密码
3. 登录凭证有效期为 **30天**

## API 接口

### 登录
```
POST /api/auth/login
Content-Type: application/json

{
  "password": "your-password"
}
```

响应：
```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

### 验证 Token
```
GET /api/auth/verify
Authorization: Bearer <token>
```

### 退出登录
```
POST /api/auth/logout
Authorization: Bearer <token>
```

## 前端使用

### 登录流程
1. 访问应用会自动跳转到登录页面
2. 输入密码进行登录
3. 登录成功后获得 JWT token
4. Token 会自动存储在 localStorage 中
5. 后续请求会自动携带 Authorization header

### Token 管理
- Token 存储在 `localStorage` 中的 `auth_token` 键
- Token 有效期为 30天
- Token 过期或无效时会自动跳转到登录页面
- 支持手动退出登录

## 安全特性

1. **密码哈希**: 使用 SHA-256 对密码进行哈希存储
2. **JWT 签名**: 使用 HS256 算法对 JWT 进行签名
3. **自动过期**: Token 30天后自动过期
4. **请求拦截**: 所有 API 请求都需要有效的 Token
5. **自动跳转**: 未认证用户自动跳转到登录页面

## 受保护的接口

以下所有接口都需要认证：

- `/api/settings/*` - 设置管理
- `/api/subscriptions/*` - 订阅管理  
- `/api/reminders/*` - 提醒管理
- `/api/export` - 数据导出
- `/api/import` - 数据导入

公开接口：
- `/api/health` - 健康检查
- `/api/auth/login` - 登录
- `/api/auth/logout` - 退出
- `/api/auth/verify` - 验证

## 部署注意事项

1. 确保在生产环境中设置强密码作为 `ADMIN_PASSWORD`
2. 修改默认的 `JWT_SECRET_KEY`
3. 考虑使用 HTTPS 保护传输中的 Token
4. 定期更换密码以提高安全性

## 故障排除

### 后端启动失败
检查是否设置了 `ADMIN_PASSWORD` 环境变量。

### 登录失败
1. 检查密码是否正确
2. 确认后端环境变量配置正确
3. 查看浏览器控制台是否有错误信息

### Token 过期
Token 有效期为30天，过期后需要重新登录。