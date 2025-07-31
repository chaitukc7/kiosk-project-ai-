#!/bin/bash

# =============================================================================
# SMART KIOSK SYSTEM - BASIC STARTUP SCRIPT
# =============================================================================
# This script starts all core services WITHOUT Ollama/Mistral AI.
# Use this for basic kiosk functionality when you don't need AI features.
# 
# PREREQUISITES:
# - Docker Desktop with 4GB+ memory allocated
# - At least 8GB system RAM
# 
# FEATURES ENABLED:
# - Complete kiosk functionality (orders, payments, menu)
# - PDF report generation
# - Basic conversational responses
# - All microservices with health checks
# 
# FEATURES NOT AVAILABLE:
# - Advanced AI queries about sales data
# - Natural language processing
# - Complex analytics through AI
# =============================================================================

echo "🚀 Starting Smart Kiosk System (Basic Mode - No AI)..."
echo "======================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start core services (without Ollama)
echo "🔨 Starting core services..."
docker-compose up -d mysql auth-service menu-service order-service payment-service llm-service frontend

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check service status
echo "📊 Service Status:"
echo "=================="
docker-compose ps

# Test core functionality
echo ""
echo "🧪 Testing core functionality..."
./test-services.sh

echo ""
echo "✅ Smart Kiosk System is now running in basic mode!"
echo ""
echo "🌐 Frontend: http://localhost:8081"
echo "🔐 Auth Service: http://localhost:5004"
echo "🍽️  Menu Service: http://localhost:5003"
echo "📦 Order Service: http://localhost:5002"
echo "💳 Payment Service: http://localhost:5006"
echo "🤖 LLM Service: http://localhost:5005"
echo "🗄️  Database: localhost:3307"
echo ""
echo "📝 Features Available:"
echo "- ✅ User authentication and registration"
echo "- ✅ Menu browsing and ordering"
echo "- ✅ Payment processing"
echo "- ✅ Basic AI chatbot responses (hello, help, etc.)"
echo "- ✅ PDF report generation (daily/weekly/monthly)"
echo "- ✅ Transaction management"
echo "- ✅ Complete kiosk workflow"
echo ""
echo "📝 Features NOT Available (requires Ollama):"
echo "- ❌ Advanced AI queries about sales data"
echo "- ❌ Natural language processing"
echo "- ❌ Complex analytics through AI"
echo ""
echo "💡 To enable full AI features:"
echo "1. Increase Docker memory to 12GB+ in Docker Desktop"
echo "2. Run: ./start.sh"
echo "3. Wait 5-10 minutes for Mistral model download" 