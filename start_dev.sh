#!/bin/bash

echo "🚀 Starting SubKeeper Development Environment..."

# Start backend
echo "📦 Starting backend on port 8000..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend on port 3000..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ SubKeeper is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
