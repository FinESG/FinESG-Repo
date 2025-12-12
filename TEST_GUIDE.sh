#!/bin/bash
# Quick Testing Guide for Fixed Issues

echo "=================================="
echo "ESG Analyst - Testing All Fixes"
echo "=================================="

# 1. Start the backend
echo ""
echo "[Step 1/3] Starting backend server..."
echo "Run this in a terminal: python main.py"
echo "Wait for: 'Uvicorn running on http://127.0.0.1:8080'"
read -p "Press Enter when backend is running..."

# 2. Start frontend
echo ""
echo "[Step 2/3] Starting frontend..."
echo "Run this in another terminal from ./frontend:"
echo "npm run dev"
echo "Wait for: 'Local: http://localhost:3000'"
read -p "Press Enter when frontend is running..."

# 3. Run tests
echo ""
echo "[Step 3/3] Running comprehensive tests..."
python test_fixes.py

# 4. Manual testing
echo ""
echo "=================================="
echo "Manual Testing Checklist"
echo "=================================="
echo ""
echo "□ Open http://localhost:3000"
echo "□ Register with email: test@example.com"
echo "□ Login with same credentials"
echo "□ Ask model: 'hi' - should get coherent response"
echo "□ Ask model: 'What is ESG?' - should get complete answer"
echo "□ Check sidebar - chat should appear in history"
echo "□ Click 'New Chat' - previous chat should stay in sidebar"
echo "□ Type new message - should appear in main view"
echo "□ Click previous chat in sidebar - should load that conversation"
echo "□ Refresh page - chats should persist in sidebar"
echo "□ Dark/Light mode toggle - should work"
echo "□ Sign Out - should return to login"
echo ""
echo "If all items pass, the system is working correctly!"
