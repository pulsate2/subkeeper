#!/bin/bash

echo "🚀 启动 SubKeeper 开发环境"
echo "================================"

# 检查后端虚拟环境
if [ ! -d "backend/venv" ]; then
    echo "❌ 后端虚拟环境不存在"
    echo "请先运行: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 检查前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend && npm install && cd ..
fi

# 启动后端
echo "🔧 启动后端服务 (端口 8000)..."
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务 (端口 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ SubKeeper 已启动！"
echo "================================"
echo "📍 前端地址: http://localhost:3000"
echo "📍 后端地址: http://localhost:8000"
echo "📍 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "echo ''; echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

wait
