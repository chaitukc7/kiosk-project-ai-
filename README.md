# 🍽️ Smart Kiosk System with Analytics

A modern restaurant kiosk application with intelligent sales analytics, PDF report generation, and conversational assistant functionality. Built with React frontend, Flask microservices, MySQL database, and advanced analytics features.

## 🚀 Features

- **🤖 Intelligent Sales Assistant**: Natural language queries about sales data using advanced analytics
- **📊 PDF Report Generation**: Daily, weekly, and monthly sales reports with detailed analytics
- **🛒 Complete Kiosk System**: Menu browsing, ordering, payment processing, and user management
- **📈 Real-time Analytics**: Live sales tracking, inventory management, and customer insights
- **🏗️ Microservices Architecture**: Scalable, maintainable, and production-ready design
- **🎨 Modern UI**: Beautiful React-based frontend with responsive design
- **🐳 Docker Containerization**: Easy deployment and consistent environment

## 🏗️ System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │ Auth Service│    │Menu Service │
│   (React)   │    │   (Flask)   │    │  (Flask)    │
│   Port 8081 │    │   Port 5004 │    │  Port 5003  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Order Service│    │Payment Svc  │    │ LLM Service │
│  (Flask)    │    │  (Flask)    │    │  (Flask)    │
│ Port 5002   │    │ Port 5006   │    │ Port 5005   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           │            ┌─────────────┐
                           │            │   Ollama    │
                           │            │ (Mistral)   │
                           │            │ Port 11434  │
                           │            └─────────────┘
                           │
                    ┌─────────────┐
                    │   MySQL     │
                    │  Database   │
                    │ Port 3307   │
                    └─────────────┘
```

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Windows, or Linux
- **RAM**: Minimum 16GB (12GB for Docker + 4GB for system)
- **Storage**: At least 10GB free space
- **Docker Desktop**: Latest version with sufficient resources allocated
- **Git**: For cloning the repository

### Docker Memory Allocation (CRITICAL)
**For advanced analytics to work properly:**
1. Open Docker Desktop
2. Go to Settings → Resources → Memory
3. **Set to at least 4GB** (8GB recommended for better performance)
4. Click Apply & Restart
5. Wait for Docker to restart completely

## 🛠️ Quick Start Guide

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd kiosk-app

# Make shell scripts executable
chmod +x *.sh
```

### Step 2: Check System Requirements
```bash
# Check Docker and system requirements
./check-docker.sh
```

### Step 3: Start Services

#### Option A: Basic Mode (No Analytics - Recommended for Testing)
```bash
# Start core services without advanced analytics
./start-basic.sh
```

#### Option B: Full Analytics Mode (Requires 4GB+ Docker Memory)
```bash
# Start all services including advanced analytics
./start.sh
```

### Step 4: Access the Application
- **Frontend**: http://localhost:8081
- **Sales Assistant**: Available in the frontend interface (bottom right corner)

### Step 5: Test Everything
```bash
# Run comprehensive tests on all services
./test-services.sh
```

## 📁 Shell Scripts Overview

### Core Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `start.sh` | Full startup with Phi-2 analytics | When you want full analytics features |
| `start-basic.sh` | Basic startup without analytics | For testing or when you don't need analytics |
| `check-docker.sh` | Check system requirements | Before starting services |
| `test-services.sh` | Test all services | After startup to verify everything works |
| `setup-ollama.sh` | Setup Ollama and Phi-2 model | Manual Ollama setup (rarely needed) |

### What Each Script Does

#### `start.sh` - Full Analytics Startup
- Starts all microservices (Auth, Menu, Order, Payment, LLM)
- Starts MySQL database
- Starts Ollama with Phi-2 model (requires 4GB+ Docker memory)
- Starts React frontend with nginx
- Waits for all services to be healthy
- Downloads Phi-2 model automatically (3-5 minutes first time)

#### `start-basic.sh` - Basic Startup
- Starts all microservices (Auth, Menu, Order, Payment, LLM)
- Starts MySQL database
- Starts React frontend with nginx
- **Skips advanced analytics** (faster startup, less memory)
- Sales assistant will use basic responses instead of Phi-2

#### `check-docker.sh` - System Check
- Verifies Docker is installed and running
- Checks Docker memory allocation
- Validates system requirements
- Provides helpful error messages if requirements not met

#### `test-services.sh` - Service Testing
- Tests database connectivity
- Tests all microservices (health checks)
- Tests frontend accessibility
- Tests sales assistant functionality
- Tests PDF report generation
- Provides summary of what's working/not working

#### `setup-ollama.sh` - Manual Analytics Setup
- Waits for Ollama service to be ready
- Checks if required models are available
- Downloads required models if not present
- Verifies model installation
- Lists available models
- **Note**: This script is automatically called by `start.sh`

## 🐳 Service Details

| Service | Port | Description | Status | Health Check |
|---------|------|-------------|--------|--------------|
| Frontend | 8081 | React app with nginx | ✅ Working | `curl http://localhost:8081` |
| Auth Service | 5004 | User authentication & JWT | ✅ Working | `curl http://localhost:5004/health` |
| Menu Service | 5003 | Menu management | ✅ Working | `curl http://localhost:5003/health` |
| Order Service | 5002 | Order processing | ✅ Working | `curl http://localhost:5002/health` |
| Payment Service | 5006 | Payment processing | ✅ Working | `curl http://localhost:5006/health` |
| LLM Service | 5005 | Sales assistant & reports | ✅ Working | `curl http://localhost:5005/health` |
| MySQL | 3307 | Database | ✅ Working | `docker exec kiosk-mysql mysql -u root -padmin123 -e "SELECT 1;"` |
| Ollama | 11434 | Advanced Analytics | ⚠️ Needs 12GB+ RAM | `curl http://localhost:11434/api/tags` |

## 🤖 Intelligent Features

### Assistant Capabilities
The sales assistant can answer questions about:
- **📊 Sales Analytics**: Revenue, best-selling items, customer spending
- **📦 Inventory**: Stock levels, popular items, trends
- **👥 Customer Insights**: Customer behavior, preferences
- **📈 Financial Reports**: Daily, weekly, monthly summaries

### Example Queries
- "What's the best selling item today?"
- "How much revenue did we make this week?"
- "Show me the top 5 customers by spending"
- "Generate a monthly sales report"
- "hello" (basic conversation)

### Quick Action Buttons
- **Best Selling Item**: Shows top performing items
- **Least Selling Item**: Shows items needing attention
- **Last Month's Sales**: Downloads PDF report
- **Last Week's Sales**: Downloads PDF report
- **Today's Sales**: Downloads PDF report

## 📊 PDF Reports

### Available Reports
- **Daily Report**: Today's sales, top items, order types
- **Weekly Report**: Last week's data (configurable date range)
- **Monthly Report**: This month's comprehensive analytics

### Report Features
- Sales summaries with revenue and order counts
- Top selling items with quantities and revenue
- Customer spending analysis
- Order type breakdowns (Pick Up vs Dine In)
- Daily/weekly sales trends
- Add-ons performance analysis

## 🛒 Kiosk System Features

### Complete User Journey
1. **Home Page**: Choose order type (Pick Up/Dine In)
2. **Menu Browsing**: Browse food items with descriptions and prices
3. **Cart Management**: Add items, modify quantities, view total
4. **Personal Details**: Enter name and phone number
5. **Payment**: Choose payment method and complete transaction
6. **Confirmation**: Receive order confirmation and receipt
7. **Sales Assistant**: Ask questions about sales and generate reports

### Database Features
- **User Management**: Store customer information
- **Order Processing**: Track all transactions
- **Inventory Tracking**: Monitor item sales
- **Analytics**: Real-time sales data

## 🔧 Ollama Setup (For Full Analytics Features)

### Prerequisites
1. **Docker Memory**: Must be set to 4GB+ in Docker Desktop
2. **System RAM**: At least 8GB total system memory
3. **Storage**: 2-4GB free space for Phi-2 model

### Setup Steps
1. **Increase Docker Memory**:
   - Open Docker Desktop
   - Settings → Resources → Memory
   - Set to 4GB or higher
   - Apply & Restart

2. **Start with Ollama**:
   ```bash
   ./start.sh  # Full startup with Ollama
   ```

3. **Wait for Model Download**:
   - First startup takes 3-5 minutes
   - Phi-2 model (~1.5GB) will be downloaded automatically
   - Monitor progress: `docker-compose logs ollama`

4. **Verify Setup**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Troubleshooting Ollama
- **Out of Memory**: Increase Docker memory to 12GB+
- **Model Not Loading**: Check Docker logs with `docker-compose logs ollama`
- **Slow Responses**: Ensure sufficient CPU cores allocated to Docker

## 📝 Development

### Project Structure
```
kiosk-app/
├── services/                 # Backend microservices
│   ├── auth-service/        # User authentication (Flask)
│   ├── menu-service/        # Menu management (Flask)
│   ├── order-service/       # Order processing (Flask)
│   ├── payment-service/     # Payment handling (Flask)
│   └── llm-service/         # Sales assistant & reports (Flask)
├── src/                     # React frontend
│   ├── components/          # React components
│   │   ├── Home.tsx        # Landing page
│   │   ├── Menu.tsx        # Menu browsing
│   │   ├── Cart.tsx        # Shopping cart
│   │   ├── PersonalDetails.tsx # User info form
│   │   ├── Payment.tsx     # Payment processing
│   │   ├── Confirmation.tsx # Order confirmation
│   │   └── NovaAIChatbot.tsx # Sales assistant interface
│   └── ...
├── frontend/                # Nginx configuration
├── docker-compose.yml       # Service orchestration
├── kiosk_schema.sql         # Database schema
├── start.sh                 # Full startup script
├── start-basic.sh           # Basic startup (no Ollama)
├── check-docker.sh          # System requirements checker
├── test-services.sh         # Service testing script
├── setup-ollama.sh          # Manual Ollama setup
├── docker-compose.yml       # Service orchestration
├── package.json             # Frontend dependencies
├── vite.config.ts           # Vite configuration
└── tailwind.config.ts       # Tailwind CSS configuration
```

### Adding New Features
1. **Backend Services**: Add new Flask services in `services/`
2. **Frontend**: Extend React components in `src/components/`
3. **Database**: Update schema in `kiosk_schema.sql`

## 🧪 Testing

### Automated Testing
```bash
# Test all services comprehensively
./test-services.sh
```

### Manual Testing Commands
```bash
# Test PDF generation
curl -X POST http://localhost:5005/generate-daily-report
curl -X POST http://localhost:5005/generate-weekly-report
curl -X POST http://localhost:5005/generate-monthly-report

# Test sales assistant
curl -X POST http://localhost:5005/ai-query \
  -H "Content-Type: application/json" \
  -d '{"question": "hello"}'

# Test frontend
curl http://localhost:8081

# Test database
docker exec kiosk-mysql mysql -u root -padmin123 -e "USE kiosk; SELECT COUNT(*) FROM transactions;"

# Test order processing
curl -X POST http://localhost:5002/transaction \
  -H "Content-Type: application/json" \
  -d '{"user":{"name":"Test User","phone":"1234567890"},"order":{"items":[{"name":"Test Item","quantity":1,"price":10.00}],"total":10.00,"orderType":"Pick Up"},"paymentTime":"2025-07-31T20:30:00.000Z"}'
```

### Frontend Testing
1. **Open**: http://localhost:8081
2. **Complete Order Flow**: Home → Menu → Cart → Personal Details → Payment → Confirmation
3. **Test Sales Assistant**: Click assistant icon (bottom right) and try queries
4. **Generate Reports**: Use quick action buttons in sales assistant

## 🚨 Troubleshooting

### Common Issues

#### 1. Out of Memory Error
```bash
# Error: "Out of memory" or "Cannot allocate memory"
# Solution: Increase Docker memory to 4GB+
```
- Open Docker Desktop → Settings → Resources → Memory
- Set to 4GB or higher
- Apply & Restart

#### 2. Services Not Starting
```bash
# Check service logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]

# Check all service status
docker-compose ps
```

#### 3. Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Check if nginx is running
docker exec kiosk-frontend nginx -t

# Restart frontend
docker-compose restart frontend
```

#### 4. Database Connection Issues
```bash
# Check database logs
docker-compose logs mysql

# Test database connection
docker exec kiosk-mysql mysql -u root -padmin123 -e "SELECT 1;"

# Reset database (WARNING: This will delete all data)
docker-compose down -v && ./start-basic.sh
```

#### 5. PDF Generation Fails
```bash
# Check LLM service logs
docker-compose logs llm-service

# Ensure database has data
docker exec kiosk-mysql mysql -u root -padmin123 -e "USE kiosk; SELECT COUNT(*) FROM transactions;"

# Test PDF generation directly
curl -X POST http://localhost:5005/generate-daily-report
```

#### 6. Sales Assistant Not Working
```bash
# Check if Ollama is running
docker-compose ps ollama

# Check Ollama logs
docker-compose logs ollama

# Test Ollama API
curl http://localhost:11434/api/tags

# If Ollama is not working, use basic mode
./start-basic.sh
```

### Useful Commands
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f [service-name]

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Stop and remove all data (WARNING: Deletes all data)
docker-compose down -v

# Check service health
docker-compose ps

# Complete reset (WARNING: Deletes all data)
docker-compose down -v && ./start-basic.sh

# Check Docker memory usage
docker stats

# Check system resources
top
htop  # if available
```

## 📞 Support

### Getting Help
1. **Check this README** for common issues and solutions
2. **Run diagnostic commands**:
   ```bash
   ./check-docker.sh
   ./test-services.sh
   docker-compose ps
   ```
3. **Check service logs** for specific errors
4. **Open an issue** on GitHub with:
   - Error messages
   - System information
   - Steps to reproduce

### System Information
- **Docker Version**: Check with `docker --version`
- **System Memory**: Check with `free -h` (Linux) or Activity Monitor (macOS)
- **Docker Memory**: Check in Docker Desktop settings

## 🎯 Quick Reference

### Essential Commands
```bash
# Basic startup (recommended for testing)
./start-basic.sh

# Full startup with analytics (requires 12GB+ Docker memory)
./start.sh

# Test everything
./test-services.sh

# Check requirements
./check-docker.sh

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

### Access Points
- **Frontend**: http://localhost:8081
- **Database**: localhost:3307 (root/admin123)
- **Sales Assistant**: Available in frontend (bottom right corner)

### Important Notes
- **First startup with Ollama** may take 3-5 minutes due to Phi-2 model download
- **Docker memory** must be 4GB+ for full analytics features
- **All services** are containerized and will start automatically
- **Database** is persistent and will retain data between restarts
- **Frontend** uses nginx for serving and API proxying

---

**🎉 Your Smart Kiosk System is ready to use!**

For questions or issues, check the troubleshooting section or open an issue on GitHub.
# kiosk-ai
