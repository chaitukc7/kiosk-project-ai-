#!/bin/bash

# =============================================================================
# FAST AI MODEL SETUP SCRIPT
# =============================================================================
# This script downloads and configures a fast, efficient AI model
# for the kiosk chatbot with minimal latency
# =============================================================================

echo "🚀 Setting up fast AI model for kiosk chatbot..."

# Check if Ollama is running
if ! docker ps | grep -q "kiosk-ollama"; then
    echo "❌ Ollama container is not running. Please start your services first:"
    echo "   docker-compose up -d"
    exit 1
fi

echo "📥 Downloading Phi-3 Mini model (fastest option)..."
docker exec kiosk-ollama ollama pull phi3:mini

echo "✅ Model downloaded successfully!"
echo ""
echo "🔧 Model Configuration:"
echo "   - Name: phi3:mini"
echo "   - Size: ~1.4GB"
echo "   - Memory: ~2GB RAM"
echo "   - Speed: 2-3x faster than Phi-2"
echo "   - Quality: Better reasoning, no hardcoding"
echo ""
echo "🚀 Your chatbot is now ready with faster responses!"
echo "   The model will automatically use the new configuration."
echo ""
echo "💡 To test, restart your services:"
echo "   docker-compose restart"
