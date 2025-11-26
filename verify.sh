#!/bin/bash

echo "🔍 SubKeeper 项目验证脚本"
echo "================================"
echo ""

# 检查后端
echo "📦 检查后端..."
if [ -d "backend/venv" ]; then
    echo "✅ 后端虚拟环境存在"
    cd backend
    source venv/bin/activate
    if python -c "import fastapi; import uvicorn; import sqlalchemy; import apscheduler" 2>/dev/null; then
        echo "✅ 后端依赖完整"
    else
        echo "❌ 后端依赖缺失"
    fi
    cd ..
else
    echo "❌ 后端虚拟环境不存在"
fi

echo ""

# 检查前端
echo "🎨 检查前端..."
if [ -d "frontend/node_modules" ]; then
    echo "✅ 前端依赖已安装"
else
    echo "⚠️  前端依赖未安装，运行: cd frontend && npm install"
fi

if [ -f "frontend/src/App.vue" ]; then
    echo "✅ 前端主组件存在"
fi

if [ -f "frontend/src/components/SubscriptionList.vue" ]; then
    echo "✅ 订阅列表组件存在"
fi

if [ -f "frontend/src/components/ReminderList.vue" ]; then
    echo "✅ 提醒列表组件存在"
fi

if [ -f "frontend/src/components/SettingsModal.vue" ]; then
    echo "✅ 设置模态框组件存在"
fi

echo ""

# 检查配置文件
echo "📄 检查配置文件..."
if [ -f "docker-compose.yml" ]; then
    echo "✅ Docker Compose 配置存在"
fi

if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile 存在"
fi

if [ -f "backend/requirements.txt" ]; then
    echo "✅ Python 依赖文件存在"
fi

if [ -f "frontend/package.json" ]; then
    echo "✅ Node.js 依赖文件存在"
fi

echo ""

# 检查启动脚本
echo "🚀 检查启动脚本..."
if [ -f "start.sh" ] && [ -x "start.sh" ]; then
    echo "✅ start.sh 存在且可执行"
else
    echo "⚠️  start.sh 不可执行，运行: chmod +x start.sh"
fi

echo ""

# 检查文档
echo "📚 检查文档..."
[ -f "README.md" ] && echo "✅ README.md"
[ -f "QUICK_START.md" ] && echo "✅ QUICK_START.md"
[ -f "PROJECT_COMPLETE.md" ] && echo "✅ PROJECT_COMPLETE.md"

echo ""
echo "================================"
echo "✅ 验证完成！"
echo ""
echo "启动项目："
echo "  ./start.sh"
echo ""
echo "或手动启动："
echo "  后端: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  前端: cd frontend && npm run dev"
echo ""
