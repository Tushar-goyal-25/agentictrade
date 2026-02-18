#!/bin/bash

echo "🚀 Starting Agentic Trading System..."

# Start backend in background
echo "📡 Starting Flask backend on port 5000..."
cd api
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Next.js frontend on port 3000..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ System started!"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
