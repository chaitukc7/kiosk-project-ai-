#!/bin/bash

echo "🤖 Setting up Ollama and Mistral Model..."
echo "=========================================="

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama service to start..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama service is ready"
        break
    else
        echo "⏳ Waiting for Ollama... (attempt $i/30)"
        sleep 10
    fi
done

# Check if Mistral model is already available
echo "🔍 Checking if Mistral model is available..."
if curl -s http://localhost:11434/api/tags | grep -q "mistral"; then
    echo "✅ Mistral model is already available"
else
    echo "📥 Pulling Mistral model..."
    echo "⚠️  This may take 5-10 minutes depending on your internet connection..."
    
    # Pull the Mistral model
    curl -X POST http://localhost:11434/api/pull -d '{"name": "mistral"}'
    
    # Wait for the model to be ready
    echo "⏳ Waiting for Mistral model to be ready..."
    for i in {1..60}; do
        if curl -s http://localhost:11434/api/tags | grep -q "mistral"; then
            echo "✅ Mistral model is ready!"
            break
        else
            echo "⏳ Waiting for Mistral model... (attempt $i/60)"
            sleep 10
        fi
    done
fi

# List available models
echo ""
echo "📋 Available Models:"
curl -s http://localhost:11434/api/tags | jq '.models[] | {name: .name, size: .size}' 2>/dev/null || curl -s http://localhost:11434/api/tags

echo ""
echo "🎉 Ollama setup complete!" 