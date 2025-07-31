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
DEFAULT_RESPONSES = {
    "hello": "Hello! I'm your AI assistant. How can I help you today?",
    "hi": "Hi there! I'm here to help with your kiosk questions.",
    "help": "I can help you with:\n- Sales analytics and reports\n- Menu and inventory questions\n- Customer insights\n- PDF report generation\n\nJust ask me anything!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome! Let me know if you need anything else."
}

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
                    "response": "I understand your question, but I need the Mistral model to provide detailed analytics. Please ensure Ollama is running with sufficient memory.",
                    "type": "fallback"
                })
        else:
            # Ollama not available, provide helpful response
            return jsonify({
                "success": True,
                "response": "I can help with basic questions! For advanced analytics, please ensure the Mistral model is loaded in Ollama.",
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
    Check if Ollama service is healthy and Mistral model is available.
    Returns True if Ollama is ready, False otherwise.
    """
    try:
        # Check if Ollama is responding
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            # Check if Mistral model is available
            return any('mistral' in model.get('name', '').lower() for model in models)
        return False
    except Exception as e:
        logger.debug(f"Ollama health check failed: {e}")
        return False

def query_ollama(question):
    """
    Send a query to Ollama/Mistral model for AI processing.
    
    Args:
        question (str): The natural language question to process
        
    Returns:
        str: AI-generated response
    """
    try:
        # Prepare the prompt for sales data analysis
        prompt = f"""
        You are an AI assistant for a restaurant kiosk system. 
        Answer the following question about sales data, menu items, or general kiosk operations:
        
        Question: {question}
        
        Provide a helpful, accurate response based on typical kiosk operations.
        If the question is about specific data, mention that you can help with general insights.
        """
        
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        
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