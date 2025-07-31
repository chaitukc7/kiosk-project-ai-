#!/bin/bash

# =============================================================================
# SMART KIOSK SYSTEM - DOCKER REQUIREMENTS CHECKER
# =============================================================================
# This script checks if your system meets the requirements to run the kiosk app.
# It verifies Docker installation, memory allocation, and system resources.
# 
# REQUIREMENTS CHECKED:
# - Docker Desktop installation and status
# - Docker memory allocation (critical for Ollama/Mistral)
# - Available disk space
# - Required tools (docker-compose, curl)
# 
# MEMORY REQUIREMENTS:
# - Basic mode: 4GB+ Docker memory
# - Full AI mode: 12GB+ Docker memory (recommended 16GB)
# =============================================================================

echo "🔍 Checking Docker and System Requirements..."
echo "=============================================="

# =============================================================================
# DOCKER INSTALLATION CHECK
# =============================================================================
# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"

# =============================================================================
# DOCKER MEMORY ALLOCATION CHECK
# =============================================================================
# Check Docker memory allocation (cross-platform)
echo ""
echo "💾 Docker Memory Allocation:"

# Try to get memory info in a cross-platform way
if command -v numfmt &> /dev/null; then
    DOCKER_MEM=$(docker system info --format '{{.MemTotal}}' | numfmt --from=iec --to=iec)
    DOCKER_MEM_GB=$(docker system info --format '{{.MemTotal}}' | numfmt --from=iec --to=none)
    DOCKER_MEM_GB=$((DOCKER_MEM_GB / 1024 / 1024 / 1024))
    echo "Docker Memory: $DOCKER_MEM"
else
    # Fallback for macOS and other systems without numfmt
    DOCKER_MEM_RAW=$(docker system info --format '{{.MemTotal}}')
    if [[ $DOCKER_MEM_RAW =~ ^[0-9]+$ ]]; then
        DOCKER_MEM_GB=$((DOCKER_MEM_RAW / 1024 / 1024 / 1024))
        echo "Docker Memory: ${DOCKER_MEM_GB}GB"
    else
        echo "Docker Memory: $DOCKER_MEM_RAW"
        DOCKER_MEM_GB=0
    fi
fi

# Provide recommendations based on memory allocation
if [ $DOCKER_MEM_GB -lt 12 ]; then
    echo "⚠️  WARNING: Docker has less than 12GB allocated ($DOCKER_MEM_GB GB)"
    echo "   The Mistral model requires significant memory. Consider increasing Docker memory limit."
    echo "   Recommended: 12-16GB for optimal performance"
    echo ""
    echo "   To increase Docker memory on macOS:"
    echo "   1. Open Docker Desktop"
    echo "   2. Go to Settings → Resources → Memory"
    echo "   3. Increase to at least 12GB"
    echo "   4. Click Apply & Restart"
else
    echo "✅ Docker memory allocation is sufficient ($DOCKER_MEM_GB GB)"
fi

# =============================================================================
# DISK SPACE CHECK
# =============================================================================
# Check available disk space
echo ""
echo "💿 Disk Space:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    DISK_SPACE=$(df -h . | awk 'NR==2 {print $4}')
else
    # Linux
    DISK_SPACE=$(df -h . | awk 'NR==2 {print $4}')
fi
echo "Available space: $DISK_SPACE"

# =============================================================================
# REQUIRED TOOLS CHECK
# =============================================================================
# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose is available"
else
    echo "❌ docker-compose is not available. Please install it."
    exit 1
fi

# Check if curl is available
if command -v curl &> /dev/null; then
    echo "✅ curl is available"
else
    echo "❌ curl is not available. Please install it."
    exit 1
fi

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================
echo ""
echo "🎯 System Check Complete!"
echo "========================="

if [ $DOCKER_MEM_GB -lt 12 ]; then
    echo "⚠️  Recommendations:"
    echo "   1. Increase Docker memory limit to at least 12GB"
    echo "   2. Restart Docker Desktop after changing memory limit"
    echo "   3. Run this check again before starting services"
    echo ""
    echo "   You can still proceed, but performance may be affected."
    echo "   For basic functionality: ./start-basic.sh"
    echo "   For full AI features: Increase memory first, then ./start.sh"
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ All requirements met! You can now run:"
    echo "   - Basic mode: ./start-basic.sh"
    echo "   - Full AI mode: ./start.sh"
fi 