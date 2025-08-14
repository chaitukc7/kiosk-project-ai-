#!/bin/bash

# =============================================================================
# SMART KIOSK SYSTEM - FULL STARTUP SCRIPT
# =============================================================================
# This script starts all services including Ollama for full functionality.
# 
# PREREQUISITES:
# - Docker Desktop with 4GB+ memory allocated (optimized for t3.large)
# - At least 8GB system RAM
# - 2-4GB free disk space for Phi-2 model
# 
# FEATURES ENABLED:
# - Complete kiosk functionality
# - Sales assistant with natural language processing
# - PDF report generation
# - All microservices with health checks
# =============================================================================

echo "🚀 Starting Smart Kiosk System with Full Analytics Features..."
echo "================================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check available memory
echo "💾 Checking system resources..."
TOTAL_MEM=$(docker system info --format '{{.MemTotal}}' | numfmt --from=iec --to=iec)
echo "Total Docker memory: $TOTAL_MEM"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start all services
echo "🔨 Building and starting all services..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 15

# Check database status
echo "🗄️ Checking database status..."
if docker-compose exec -T mysql mysqladmin ping -h localhost -u root -padmin123 > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready yet, waiting..."
    sleep 10
fi

# Wait for Ollama to start and pull Phi-2 model
echo "🤖 Setting up Ollama and Phi-2 model..."
echo "📥 This may take 3-5 minutes on first run..."
echo "⚠️  Ensure Docker has at least 4GB memory allocated!"
sleep 30

# Check if Phi-2 model is available
echo "🔍 Checking Phi-2 model availability..."
for i in {1..20}; do
    if curl -s http://localhost:11434/api/tags | grep -q "phi"; then
        echo "✅ Phi-2 model is ready"
        break
    else
        echo "⏳ Waiting for Phi-2 model... (attempt $i/20)"
        sleep 30
    fi
done

# Wait for all services to be healthy
echo "⏳ Waiting for all services to be healthy..."
sleep 20

# Check service status
echo "📊 Service Status:"
echo "=================="
docker-compose ps

# Check health of all services
echo ""
echo "🏥 Health Check Results:"
echo "========================"

services=("mysql" "ollama" "auth-service" "menu-service" "order-service" "payment-service" "llm-service" "frontend")
for service in "${services[@]}"; do
    if docker-compose ps $service | grep -q "Up"; then
        echo "✅ $service: Running"
    else
        echo "❌ $service: Not running"
    fi
done

echo ""
echo "✅ Smart Kiosk System is now running with full analytics features!"
echo ""
echo "🌐 Frontend: http://localhost:8081"
echo "🔐 Auth Service: http://localhost:5004"
echo "🍽️  Menu Service: http://localhost:5003"
echo "📦 Order Service: http://localhost:5002"
echo "💳 Payment Service: http://localhost:5006"
echo "🤖 LLM Service: http://localhost:5005"
echo "🗄️  Database: localhost:3307"
echo "🤖 Ollama (Analytics): http://localhost:11434"
echo ""
echo "📝 To view logs: docker-compose logs -f [service-name]"
echo "🛑 To stop: docker-compose down"
echo ""
echo "🎯 Analytics Features Available:"
echo "- Natural language queries about sales data"
echo "- PDF report generation (daily, weekly, monthly)"
echo "- Conversational assistant responses"
echo "- Advanced analytics and insights"
echo ""
echo "💡 Tips:"
echo "- First startup may take 3-5 minutes due to Phi-2 model download"
echo "- Analytics responses may be slow initially as the model loads"
echo "- Check logs if any service fails to start"
echo "- For optimal performance, ensure Docker has 4GB+ memory" 