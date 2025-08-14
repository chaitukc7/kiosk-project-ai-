# =============================================================================
# SMART KIOSK SYSTEM - LLM SERVICE
# =============================================================================
# This service provides AI chatbot functionality and PDF report generation.
# 
# FEATURES:
# - Natural language query processing using Ollama/Mistral
# - PDF report generation (daily, weekly, monthly)
# - Basic conversational responses
# - Integration with MySQL database for data queries
# 
# ENDPOINTS:
# - /health: Service health check
# - /ai-query: Process natural language queries
# - /generate-daily-report: Generate daily sales PDF
# - /generate-weekly-report: Generate weekly sales PDF
# - /generate-monthly-report: Generate monthly sales PDF
# =============================================================================

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
import mysql.connector
from pdf_service import generate_daily_report, generate_weekly_report, generate_monthly_report
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# PDF service functions are imported directly

# =============================================================================
# CONFIGURATION
# =============================================================================
# Service configuration and environment variables
OLLAMA_URL = "http://ollama:11434"
# Model configuration - optimized for cloud deployment on t3.large
# Options: 
# - "phi:2.7b" (2.7B params, ~2GB RAM, perfect for t3.large)
# - "llama2:7b-chat-q4_0" (quantized, ~4GB RAM, good performance)
# - "mistral" (7B params, ~12GB RAM, best performance but expensive)
AI_MODEL = os.getenv('AI_MODEL', 'phi:2.7b')  # Default to Phi-2 for cost efficiency
MYSQL_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'admin123',
    'database': 'kiosk'
}
DEFAULT_RESPONSES = {
    "hello": "Hello! I'm your AI assistant. How can I help you today?",
    "hi": "Hi there! I'm here to help with your kiosk questions.",
    "help": "I can help you with:\n- Sales analytics and reports\n- Menu and inventory questions\n- Customer insights\n- PDF report generation\n\nJust ask me anything!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome! Let me know if you need anything else."
}

# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================
def get_sales_data():
    """
    Get comprehensive sales data from the database for AI analysis.
    Returns a dictionary with various sales metrics and data.
    """
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        
        data = {}
        
        # Get total transactions and revenue
        cursor.execute("""
            SELECT COUNT(*) as total_orders, SUM(total) as total_revenue, AVG(total) as avg_order_value
            FROM transactions
        """)
        result = cursor.fetchone()
        data['total_orders'] = result[0] if result[0] else 0
        data['total_revenue'] = float(result[1]) if result[1] else 0.0
        data['avg_order_value'] = float(result[2]) if result[2] else 0.0
        
        # Get top selling items
        cursor.execute("""
            SELECT oi.name, SUM(oi.quantity) as total_quantity, SUM(oi.quantity * oi.price) as total_revenue
            FROM order_items oi
            JOIN transactions t ON oi.transaction_id = t.id
            GROUP BY oi.name
            ORDER BY total_quantity DESC
            LIMIT 10
        """)
        top_items = cursor.fetchall()
        data['top_items'] = [{'name': item[0], 'quantity': item[1], 'revenue': float(item[2])} for item in top_items]
        
        # Get least selling items
        cursor.execute("""
            SELECT oi.name, SUM(oi.quantity) as total_quantity, SUM(oi.quantity * oi.price) as total_revenue
            FROM order_items oi
            JOIN transactions t ON oi.transaction_id = t.id
            GROUP BY oi.name
            ORDER BY total_quantity ASC
            LIMIT 10
        """)
        least_items = cursor.fetchall()
        data['least_items'] = [{'name': item[0], 'quantity': item[1], 'revenue': float(item[2])} for item in least_items]
        
        # Get order types breakdown
        cursor.execute("""
            SELECT order_type, COUNT(*) as count, SUM(total) as total_revenue
            FROM transactions
            GROUP BY order_type
        """)
        order_types = cursor.fetchall()
        data['order_types'] = [{'type': ot[0], 'count': ot[1], 'revenue': float(ot[2])} for ot in order_types]
        
        # Get recent transactions
        cursor.execute("""
            SELECT t.id, u.name as customer_name, t.order_type, t.total, t.payment_time
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            ORDER BY t.payment_time DESC
            LIMIT 5
        """)
        recent_transactions = cursor.fetchall()
        data['recent_transactions'] = [{'id': rt[0], 'customer': rt[1], 'type': rt[2], 'total': float(rt[3]), 'time': str(rt[4])} for rt in recent_transactions]
        
        cursor.close()
        connection.close()
        
        return data
        
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return None

# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Docker health monitoring.
    Returns service status and basic connectivity information.
    """
    try:
        # Check if Ollama is available
        ollama_status = "healthy" if check_ollama_health() else "unhealthy"
        
        return jsonify({
            "status": "healthy",
            "service": "llm-service",
            "ollama": ollama_status,
            "pdf_service": "available"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# =============================================================================
# AI QUERY PROCESSING ENDPOINT
# =============================================================================
@app.route('/ai-query', methods=['POST'])
def ai_query():
    """
    Process natural language queries about kiosk data.
    
    Expected JSON payload:
    {
        "question": "What's the best selling item today?"
    }
    
    Returns AI-generated response based on the query.
    """
    try:
        data = request.get_json()
        question = data.get('question', '').lower().strip()
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        # Check for basic conversational queries first
        for key, response in DEFAULT_RESPONSES.items():
            if key in question:
                return jsonify({
                    "success": True,
                    "response": response,
                    "type": "conversational"
                })
        
        # Try to use Ollama for advanced queries
        if check_ollama_health():
            try:
                ai_response = query_ollama(question)
                return jsonify({
                    "success": True,
                    "response": ai_response,
                    "type": "ai_generated"
                })
            except Exception as e:
                logger.warning(f"Ollama query failed: {e}")
                # Fall back to basic response
                return jsonify({
                    "success": True,
                    "response": "I understand your question, but I need the analytics model to provide detailed insights. Please ensure Ollama is running with sufficient memory.",
                    "type": "fallback"
                })
        else:
            # Ollama not available, provide helpful response
            return jsonify({
                "success": True,
                "response": "I can help with basic questions! For advanced analytics, please ensure the Phi-2 model is loaded in Ollama.",
                "type": "basic"
            })
            
    except Exception as e:
        logger.error(f"AI query processing failed: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to process query",
            "details": str(e)
        }), 500

# =============================================================================
# PDF REPORT GENERATION ENDPOINTS
# =============================================================================
@app.route('/generate-daily-report', methods=['POST'])
def generate_daily_report_endpoint():
    """
    Generate a PDF report for today's sales data.
    Returns the PDF file for download.
    """
    try:
        pdf_path = generate_daily_report()
        return send_file(pdf_path, as_attachment=True, download_name='daily_report.pdf')
    except Exception as e:
        logger.error(f"Daily report generation failed: {e}")
        return jsonify({"error": "Failed to generate daily report"}), 500

@app.route('/generate-weekly-report', methods=['POST'])
def generate_weekly_report_endpoint():
    """
    Generate a PDF report for last week's sales data.
    Returns the PDF file for download.
    """
    try:
        pdf_path = generate_weekly_report()
        return send_file(pdf_path, as_attachment=True, download_name='weekly_report.pdf')
    except Exception as e:
        logger.error(f"Weekly report generation failed: {e}")
        return jsonify({"error": "Failed to generate weekly report"}), 500

@app.route('/generate-monthly-report', methods=['POST'])
def generate_monthly_report_endpoint():
    """
    Generate a PDF report for this month's sales data.
    Returns the PDF file for download.
    """
    try:
        pdf_path = generate_monthly_report()
        return send_file(pdf_path, as_attachment=True, download_name='monthly_report.pdf')
    except Exception as e:
        logger.error(f"Monthly report generation failed: {e}")
        return jsonify({"error": "Failed to generate monthly report"}), 500

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def check_ollama_health():
    """
    Check if Ollama service is healthy and Phi-2 model is available.
    Returns True if Ollama is ready, False otherwise.
    """
    try:
        # Check if Ollama is responding
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            # Check if the configured model is available
            return any(AI_MODEL.split(':')[0] in model.get('name', '').lower() for model in models)
        return False
    except Exception as e:
        logger.debug(f"Ollama health check failed: {e}")
        return False

def query_ollama(question):
    """
    Send a query to Ollama/Phi-2 model for analytics processing with real sales data.
    
    Args:
        question (str): The natural language question to process
        
    Returns:
        str: AI-generated response based on real data
    """
    try:
        # Get real sales data from database
        sales_data = get_sales_data()
        
        if not sales_data:
            return "I'm sorry, but I'm unable to access the sales data at the moment. Please try again later."
        
        # Format the sales data for the prompt - optimized for Phi-2
        data_summary = f"Sales Data: {sales_data['total_orders']} orders, ${sales_data['total_revenue']:.2f} revenue. "
        
        # Add top items (limit to 5 for efficiency)
        if sales_data['top_items']:
            data_summary += "Top items: "
            for i, item in enumerate(sales_data['top_items'][:5]):
                data_summary += f"{item['name']}({item['quantity']} sold, ${item['revenue']:.2f}), "
        
        # Add least items (limit to 3 for efficiency)
        if sales_data['least_items']:
            data_summary += "Least sold: "
            for i, item in enumerate(sales_data['least_items'][:3]):
                data_summary += f"{item['name']}({item['quantity']} sold), "
        
        # Prepare the prompt with real data - optimized for Phi-2
        prompt = f"""You are a restaurant analytics assistant. Use this data to answer: {data_summary}

Question: {question}

Answer based on the sales data above. Be specific with numbers and item names."""
        
        payload = {
            "model": AI_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'I apologize, but I could not generate a response.')
        else:
            raise Exception(f"Ollama API returned status {response.status_code}")
            
    except Exception as e:
        logger.error(f"Ollama query failed: {e}")
        raise

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================
if __name__ == '__main__':
    # Start the Flask application
    # Note: In production, use a proper WSGI server like gunicorn
    app.run(host='0.0.0.0', port=5005, debug=False) 