# Kiosk App - Full-Stack Restaurant Ordering System

A comprehensive full-stack kiosk ordering system with a modern React frontend, a Python Flask backend, and a MySQL database. Features an AI-powered chatbot that uses Mistral LLM to answer questions about sales data and generate downloadable PDF reports.

## 🚀 Features

### Core Ordering System
- **User-friendly React frontend** with modern UI components
- **Complete ordering workflow**: Sign In → Menu Selection → Cart → Personal Details → Payment → Confirmation
- **Real-time order processing** with MySQL database storage
- **Business logic implementation**: Dine In requires seat number, Pick Up doesn't
- **Receipt generation** with discount and tax calculations

### AI-Powered Analytics
- **Natural language queries** about sales data using Mistral LLM
- **Real-time database insights** through conversational interface
- **Predefined quick actions** for common queries
- **User-friendly responses** instead of raw database output
- **Smart conversational handling** for greetings and casual chat

### PDF Report Generation
- **Daily reports** - Today's sales, top items, recent transactions
- **Weekly reports** - Last week's performance with daily breakdown
- **Monthly reports** - Comprehensive monthly analytics
- **Automatic downloads** with proper file naming

### Technical Features
- **Cross-origin communication** between frontend and backend
- **Robust error handling** with user-friendly messages
- **Database schema optimization** for efficient queries
- **Modular code structure** with comprehensive documentation
- **Advanced prompt engineering** for accurate SQL generation

## 📁 Project File Structure

### **Root Directory Files**
- **`README.md`** → This file! Contains setup instructions, documentation, and troubleshooting guide
- **`package.json`** → Frontend dependencies and scripts (React, Vite, etc.)
- **`kiosk_schema.sql`** → Database structure - creates tables for users, transactions, orders, and add-ons
- **`tailwind.config.ts`** → Styling configuration for the modern UI design
- **`vite.config.ts`** → Build tool configuration for fast development and production builds

### **Frontend Files (`src/` folder)**
- **`src/App.tsx`** → Main React application that connects all the pages together
- **`src/components/`** → All the user interface components:
  - **`Home.tsx`** → Welcome page where users start their ordering journey
  - **`Menu.tsx`** → Displays food items, lets users add items to cart
  - **`Cart.tsx`** → Shows selected items, quantities, and total price
  - **`PersonalDetails.tsx`** → Collects customer name and phone number
  - **`Payment.tsx`** → Handles payment processing and sends order to backend
  - **`Confirmation.tsx`** → Shows order receipt and confirmation
  - **`NovaAIChatbot.tsx`** → AI chatbot interface for asking business questions
  - **`SignIn.tsx`** → Customer sign-in page (if needed)

### **Backend Files (`backend/` folder)**
- **`app.py`** → Main server file - handles all web requests and coordinates between different services
- **`database.py`** → Talks to MySQL database - runs queries, gets data, saves information
- **`ai_service.py`** → Handles AI chatbot - converts questions to SQL, gets answers from Mistral
- **`transaction_service.py`** → Processes orders - validates data, saves transactions, handles business rules
- **`pdf_reports.py`** → Creates PDF reports - daily, weekly, and monthly sales summaries
- **`schema_prompt.txt`** → Instructions for AI on how to write SQL queries for our database
- **`requirements.txt`** → List of Python packages needed (Flask, MySQL connector, etc.)

### **Configuration Files**
- **`tsconfig.json`** → TypeScript settings for better code quality
- **`components.json`** → shadcn/ui component library configuration
- **`.gitignore`** → Tells Git which files to ignore (node_modules, build files, etc.)

## 🛠️ Technologies Used

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **shadcn/ui** for modern UI components
- **Tailwind CSS** for styling
- **Lucide React** for icons

### Backend
- **Python 3.13** with Flask framework
- **MySQL** for data persistence
- **Flask-CORS** for cross-origin requests
- **Requests** library for AI communication
- **FPDF** for PDF generation

### AI & Database
- **Mistral LLM** via Ollama for natural language processing
- **MySQL** for relational data storage
- **SQL query generation** from natural language

## 📋 Prerequisites

Before running this project, ensure you have:

- **Node.js** (v18 or higher)
- **Python 3.13** or higher
- **MySQL** server running locally
- **Git** for version control

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd kiosk-app
```

### 2. Set Up the Database

#### Option A: Using MySQL Workbench
1. Open MySQL Workbench
2. Create a new database:
   ```sql
   CREATE DATABASE kiosk;
   ```
3. Select the `kiosk` database
4. Run the schema file:
   ```sql
   SOURCE kiosk_schema.sql;
   ```

#### Option B: Using Command Line
```bash
mysql -u root -p
CREATE DATABASE kiosk;
USE kiosk;
SOURCE kiosk_schema.sql;
```

### 3. Set Up Ollama and Mistral AI

#### Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 4. Start Ollama and Download Mistral
```bash
# Start Ollama service
ollama serve

# In a new terminal, download Mistral model
ollama pull mistral
```

### 5. Set Up Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 6. Set Up Frontend
```bash
# In a new terminal (from project root)
npm install
npm run dev
```



#### Start Ollama and Download Mistral
```bash
# Start Ollama service
ollama serve

# In a new terminal, download Mistral model
ollama pull mistral
```

### 4. Set Up the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python app.py
```

The backend will start on `http://localhost:5001`

### 5. Set Up the Frontend

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:8080`

## 🎯 How It Works

### Order Processing Flow
1. **User places order** in React frontend
2. **Frontend sends data** to Flask backend via POST `/transaction`
3. **Backend processes and stores** data in MySQL database
4. **Receipt and confirmation** shown in frontend

### AI Chatbot Flow
1. **User asks question** → Frontend sends to `/ai-query` endpoint
2. **Backend processes** → Sends question to Mistral via Ollama
3. **Mistral generates SQL** → Based on database schema
4. **Backend executes SQL** → Runs query against MySQL
5. **Results formatted** → Converted to natural language
6. **Response displayed** → Shows answer in chatbot

### PDF Generation Flow
1. **User clicks report button** → Frontend sends to PDF endpoint
2. **Backend generates PDF** → Queries database and creates report
3. **PDF file returned** → Sent as downloadable file
4. **Browser downloads** → Automatic file download

## 🤖 AI Chatbot Features

### Predefined Questions
- **Best Selling Item** - Shows the most popular menu item
- **Least Selling Item** - Shows the least popular menu item
- **Last Month's Sales** - Monthly sales report (PDF)
- **Last Week's Sales** - Weekly sales report (PDF)
- **Today's Sales** - Today's sales report (PDF)

### Custom Questions
You can ask any natural language question like:
- "What's the most popular item?"
- "Show me today's revenue"
- "Which items sold the most this month?"
- "What's the average order value?"
- "How many orders were placed today?"
- "What's the top selling add-on today?"

### AI Capabilities
- **Dynamic SQL Generation** - No hardcoded queries
- **Schema Understanding** - Knows your database structure
- **Natural Language Processing** - Understands complex questions
- **Real-time Data** - Always queries your live MySQL database
- **Error Handling** - Graceful handling of database and AI errors

## 📊 PDF Reports

### Daily Report
- Today's sales summary
- Top selling items and add-ons
- Order types breakdown
- Recent transactions

### Weekly Report
- Last week's performance
- Daily sales breakdown
- Top customers
- Item popularity trends

### Monthly Report
- Monthly sales summary
- Weekly breakdown
- Customer analytics
- Add-ons performance

## 🗄️ Database Schema

### Tables
- **users** - Customer information (id, name, phone)
- **transactions** - Order details (id, user_id, seat_number, order_type, total, payment_method, payment_time)
- **order_items** - Menu items in orders (id, transaction_id, item_id, name, quantity, price)
- **add_ons** - Additional items (id, transaction_id, add_on_id, name, quantity, price)

### Relationships
- `transactions.user_id` → `users.id`
- `order_items.transaction_id` → `transactions.id`
- `add_ons.transaction_id` → `transactions.id`

## 🔧 API Endpoints

### Order Processing
- `POST /transaction` - Save order data to database

### AI Queries
- `POST /ai-query` - Process natural language questions

### PDF Reports
- `POST /generate-daily-report` - Generate daily PDF report
- `POST /generate-weekly-report` - Generate weekly PDF report
- `POST /generate-monthly-report` - Generate monthly PDF report

## 🐛 Troubleshooting

### General Issues
- **Port conflicts**: Kill processes using port 5001: `lsof -ti:5001 | xargs kill -9`
- **MySQL connection**: Verify MySQL is running and credentials are correct
- **Missing dependencies**: Run `pip install -r requirements.txt` in backend directory

### AI Chatbot Issues
- **"Could not connect to Ollama"**: Make sure Ollama is running (`ollama serve`)
- **"Database error"**: Check MySQL connection and ensure database exists
- **"No data found"**: Query ran successfully but no data matches criteria
- **"Model not found"**: Run `ollama pull mistral` to download the model

### PDF Generation Issues
- **"Connection error"**: Ensure backend is running on port 5001
- **"Download failed"**: Check browser download settings
- **"Empty report"**: Verify database has data for the requested period

### Backend Issues
- **Import errors**: Ensure virtual environment is activated
- **Database errors**: Check MySQL server status and credentials
- **CORS errors**: Verify Flask-CORS is installed and configured

## 📁 Project Structure

```
kiosk-app/
├── backend/
│   ├── app.py                 # Main Flask application (orchestrator)
│   ├── database.py           # Database operations and utilities
│   ├── ai_service.py         # AI/LLM processing and query handling
│   ├── transaction_service.py # Transaction processing and business logic
│   ├── pdf_reports.py        # PDF generation functions
│   ├── schema_prompt.txt     # Database schema for AI
│   ├── requirements.txt      # Python dependencies
│   └── venv/                 # Virtual environment
├── src/
│   ├── components/
│   │   ├── NovaAIChatbot.tsx # AI chatbot component
│   │   ├── Payment.tsx       # Payment processing
│   │   ├── Confirmation.tsx  # Order confirmation
│   │   └── ...               # Other components
│   ├── App.tsx               # Main React application
│   └── main.tsx              # React entry point
├── kiosk_schema.sql          # Database schema
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## 🏗️ Backend Modular Architecture

The backend has been refactored into a clean, modular architecture with clear separation of concerns. Each module handles a specific aspect of the application, making the code more maintainable, testable, and easier to understand.

### 📦 Module Descriptions

#### 1. **`app.py` - Main Application (Orchestrator)**
**What it does**: This is the boss of the backend - it coordinates everything and handles all the web requests.

**In simple terms**: Think of it as a restaurant manager who takes orders from customers (frontend) and delegates them to the right departments (other modules).

**What it handles**:
- Receives requests from the frontend
- Routes them to the right service
- Returns responses back to the frontend
- Handles errors gracefully

**Example**: When someone asks "What's the best selling item?", `app.py` receives this question and sends it to the AI service to get an answer.

#### 2. **`database.py` - Database Manager**
**What it does**: Handles all database operations like connecting to MySQL, running queries, and formatting results.

**In simple terms**: Think of it as a librarian who knows exactly where to find information in a huge library (database) and can retrieve it quickly.

**What it handles**:
- Connecting to the MySQL database
- Running SQL queries safely
- Cleaning up messy SQL from the AI
- Formatting database results nicely

**Example**: When the AI generates a SQL query like "SELECT * FROM orders", `database.py` makes sure it's safe to run, executes it, and returns the results in a clean format.

#### 3. **`ai_service.py` - AI Brain**
**What it does**: Handles all AI-related tasks like understanding natural language questions and converting them to database queries.

**In simple terms**: Think of it as a smart translator who can understand human questions like "What's the best selling item?" and turn them into computer language (SQL) that the database can understand.

**What it handles**:
- Detecting if someone is just saying "hello" vs asking a business question
- Creating smart prompts for the AI
- Talking to the Mistral AI model
- Converting database results into human-readable answers

**Example**: When you ask "How much did we earn today?", `ai_service.py`:
1. Recognizes this is a business question (not just "hello")
2. Creates a prompt for the AI: "Generate SQL to find today's revenue"
3. Sends it to Mistral AI
4. Gets back SQL like "SELECT SUM(total) FROM transactions WHERE DATE(payment_time) = CURDATE()"
5. Sends this to the database
6. Formats the result as "Today's revenue is $1,250.00"

#### 4. **`transaction_service.py` - Order Processor**
**What it does**: Handles all the business logic for processing orders, validating data, and storing transactions.

**In simple terms**: Think of it as a cashier who checks if orders are valid, processes payments, and makes sure everything is recorded correctly.

**What it handles**:
- Validating customer information (name, phone, etc.)
- Checking if orders are complete and valid
- Storing customer data in the database
- Recording transactions and order items
- Enforcing business rules (like requiring seat numbers for dine-in orders)

**Example**: When someone places an order:
1. `transaction_service.py` checks if they provided a name and phone number
2. Verifies the order has items and a valid total
3. If it's a "Dine In" order, makes sure they provided a seat number
4. Saves the customer info to the database
5. Records the transaction and all the items they ordered
6. Returns a success message

#### 5. **`pdf_reports.py` - Report Generator**
**What it does**: Creates beautiful PDF reports with sales data, analytics, and business insights.

**In simple terms**: Think of it as an accountant who takes all the sales data and creates professional reports that business owners can use to make decisions.

**What it handles**:
- Generating daily sales reports
- Creating weekly performance summaries
- Building monthly analytics reports
- Formatting data into professional PDF documents

**Example**: When you click "Generate Daily Report", `pdf_reports.py`:
1. Queries the database for today's sales data
2. Calculates totals, averages, and trends
3. Creates a professional PDF with charts and tables
4. Saves it as a downloadable file

### 🔄 How They Work Together

Here's how the modules work together when someone asks "What's the best selling item?":

1. **`app.py`** receives the question from the frontend
2. **`app.py`** sends it to **`ai_service.py`**
3. **`ai_service.py`** creates a prompt and sends it to Mistral AI
4. **`ai_service.py`** gets back SQL and sends it to **`database.py`**
5. **`database.py`** runs the SQL query and returns the results
6. **`ai_service.py`** formats the results into a nice answer
7. **`app.py`** sends the answer back to the frontend

### ✅ Benefits of This Structure

- **Easy to fix bugs**: If there's an issue with AI responses, you only need to look in `ai_service.py`
- **Easy to add features**: Want to add email notifications? Just create a new `email_service.py` module
- **Easy to test**: Each module can be tested independently
- **Easy to understand**: Each file has one clear job
- **Easy to maintain**: Changes in one module don't break others

## 📋 Detailed Function Documentation

### **Backend Module Functions**

#### **`app.py` - Main Application Orchestrator**
- **`@app.route('/ai-query', methods=['POST'])`** → Handles AI chatbot requests, delegates to `ai_service.py`
- **`@app.route('/transaction', methods=['POST'])`** → Processes order transactions, delegates to `transaction_service.py`
- **`@app.route('/generate-daily-report', methods=['POST'])`** → Generates daily PDF reports
- **`@app.route('/generate-weekly-report', methods=['POST'])`** → Generates weekly PDF reports
- **`@app.route('/generate-monthly-report', methods=['POST'])`** → Generates monthly PDF reports
- **`@app.route('/test-db', methods=['GET'])`** → Tests database connectivity

#### **`database.py` - Database Operations**
- **`get_db()`** → Creates and returns MySQL database connection
- **`load_schema()`** → Reads database schema from `schema_prompt.txt` file
- **`extract_sql(raw_output)`** → Extracts clean SQL from Mistral's response, removes malformed queries
- **`check_aliases(sql)`** → Validates SQL for undeclared table aliases
- **`execute_query(sql)`** → Executes SQL query and returns results or error
- **`format_query_results(result)`** → Converts database results to readable string format

#### **`ai_service.py` - AI and Natural Language Processing**
- **`is_conversational_query(question)`** → Determines if question is casual chat or business query
- **`get_conversational_response(question)`** → Generates friendly responses for greetings and casual chat
- **`create_ai_prompt(question)`** → Builds comprehensive prompt for Mistral with schema and guidelines
- **`query_ollama(prompt)`** → Sends prompt to Mistral via Ollama API, handles timeouts
- **`format_natural_response(question, result, formatted_result)`** → Converts raw database results to natural English
- **`process_ai_query(question)`** → Main orchestrator for AI query processing pipeline

#### **`transaction_service.py` - Order Processing and Business Logic**
- **`validate_user_data(user_data)`** → Validates customer name and phone number
- **`validate_order_data(order_data)`** → Validates order items and add-ons structure
- **`insert_user(name, phone)`** → Inserts new customer into users table
- **`insert_transaction(user_id, order_data)`** → Creates transaction record with business rules
- **`insert_order_items(transaction_id, items)`** → Stores individual menu items for the order
- **`insert_add_ons(transaction_id, add_ons)`** → Stores add-on items for the order
- **`process_transaction(data)`** → Main function that orchestrates entire order processing

#### **`pdf_reports.py` - PDF Report Generation**
- **`generate_daily_report()`** → Creates PDF with today's sales data and analytics
- **`generate_weekly_report()`** → Creates PDF with last week's performance summary
- **`generate_monthly_report()`** → Creates PDF with comprehensive monthly analytics
- **`create_pdf_header(pdf, title)`** → Adds professional header to PDF reports
- **`add_sales_summary(pdf, data)`** → Adds sales summary section to PDF
- **`add_top_items(pdf, data)`** → Adds best-selling items section to PDF

### **Frontend Component Functions**

#### **`NovaAIChatbot.tsx` - AI Chatbot Interface**
- **`handleSend()`** → Processes user input, sends to backend, displays response
- **`handleQuickOption(option)`** → Handles predefined quick action buttons
- **`downloadPDF(reportType)`** → Downloads generated PDF reports
- **`scrollToBottom()`** → Auto-scrolls chat to latest message

#### **`Payment.tsx` - Payment Processing**
- **`handlePayment()`** → Collects user data, sends order to backend, handles response
- **`validateForm()`** → Validates payment form before submission

#### **`Menu.tsx` - Menu Display**
- **`addToCart(item)`** → Adds menu item to shopping cart
- **`removeFromCart(itemId)`** → Removes item from cart
- **`updateQuantity(itemId, quantity)`** → Updates item quantity in cart

### **Key Data Flow Examples**

#### **AI Query Flow**
1. User types: "What is the best selling item?"
2. `NovaAIChatbot.handleSend()` → Sends to `/ai-query`
3. `app.py` → Calls `ai_service.process_ai_query()`
4. `ai_service.is_conversational_query()` → Returns `false` (business query)
5. `ai_service.create_ai_prompt()` → Builds prompt with schema
6. `ai_service.query_ollama()` → Gets SQL from Mistral
7. `database.extract_sql()` → Cleans SQL query
8. `database.execute_query()` → Runs query against MySQL
9. `ai_service.format_natural_response()` → Converts to: "The best selling item is Udon with 17 orders"
10. Response sent back to frontend

#### **Order Processing Flow**
1. User clicks "Pay" button
2. `Payment.handlePayment()` → Collects user and order data
3. Sends to `/transaction` endpoint
4. `app.py` → Calls `transaction_service.process_transaction()`
5. `transaction_service.validate_user_data()` → Validates customer info
6. `transaction_service.insert_user()` → Creates customer record
7. `transaction_service.insert_transaction()` → Creates order with business rules
8. `transaction_service.insert_order_items()` → Stores menu items
9. `transaction_service.insert_add_ons()` → Stores add-ons
10. Success response sent back to frontend

## 🔄 Development Workflow

### Making Changes
1. **Frontend changes**: Edit React components in `src/`
2. **Backend changes**: Edit Flask app in `backend/app.py`
3. **Database changes**: Update `kiosk_schema.sql` and run in MySQL
4. **AI improvements**: Modify `backend/schema_prompt.txt`

### Testing
- **Frontend**: Changes auto-reload in development
- **Backend**: Flask debug mode auto-reloads
- **Database**: Test queries in MySQL Workbench
- **AI**: Test questions in chatbot interface

## 🚀 Deployment

### Production Setup
1. **Build frontend**: `npm run build`
2. **Set up production server** with Node.js and Python
3. **Configure MySQL** with proper credentials
4. **Set up Ollama** on production server
5. **Configure environment variables** for database and AI settings

### Environment Variables
```bash
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=kiosk

# AI Service
OLLAMA_URL=http://localhost:11434
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔧 Troubleshooting

### Common Issues and Solutions

#### **Backend Issues**
- **"Port 5001 is in use"** → Kill existing process: `lsof -ti:5001 | xargs kill -9`
- **"ModuleNotFoundError: No module named 'mysql'"** → Install requirements: `pip install -r requirements.txt`
- **"MySQL connection failed"** → Check MySQL is running: `sudo /usr/local/mysql/support-files/mysql.server restart`

#### **Frontend Issues**
- **"Error connecting to backend"** → Ensure backend is running on port 5001
- **"CORS errors"** → Backend CORS is configured, restart backend if needed
- **"Build errors"** → Clear node_modules: `rm -rf node_modules && npm install`

#### **AI Chatbot Issues**
- **"Ollama timeout"** → Restart Ollama: `ollama serve` in new terminal
- **"No response from AI"** → Check Mistral is downloaded: `ollama list`
- **"SQL errors"** → Check database connection and schema

#### **Database Issues**
- **"Table doesn't exist"** → Run schema: `mysql -u root -p kiosk < kiosk_schema.sql`
- **"Connection refused"** → Start MySQL: `sudo /usr/local/mysql/support-files/mysql.server start`
- **"Access denied"** → Check credentials in `database.py`

### Debug Commands

#### **Test Backend**
```bash
# Test database connection
curl http://localhost:5001/test-db

# Test AI query
curl -X POST http://localhost:5001/ai-query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the best selling item?"}'
```

#### **Test Frontend**
```bash
# Check if frontend is running
curl http://localhost:5173

# Check for build errors
npm run build
```

#### **Test Ollama**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test Mistral model
ollama run mistral "Hello, how are you?"
```

### Performance Tips

#### **Faster AI Responses**
- **Use SSD storage** for Ollama model files
- **Increase system RAM** for better model performance
- **Close other applications** to free up resources

#### **Database Optimization**
- **Add indexes** on frequently queried columns
- **Use connection pooling** for production
- **Regular database maintenance** and cleanup

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure all services are running
4. Check console logs for error messages
5. Contact support with specific error details

---

**Happy coding! 🎉**
