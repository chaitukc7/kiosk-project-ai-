"""
Kiosk Backend Server - Main Application
======================================

This is the main Flask application that orchestrates all the services:
- Database operations (database.py)
- AI/LLM processing (ai_service.py) 
- Transaction processing (transaction_service.py)
- PDF report generation (pdf_reports.py)

The application provides RESTful API endpoints for:
- Transaction processing (/transaction)
- AI-powered queries (/ai-query)
- PDF report generation (/generate-*-report)
- Database testing (/test-db)

Date: 2025
"""

import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdf_reports
from datetime import datetime

# Import our service modules
from database import get_db
from ai_service import process_ai_query
from transaction_service import process_transaction

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================

app = Flask(__name__)

# Configure CORS to allow frontend communication
# This allows the React frontend (port 8080) to communicate with this backend (port 5001)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_server_info():
    """
    Print server startup information.
    This helps verify that all services are properly configured.
    """
    print(" Starting Kiosk Backend Server...")
    print(" Backend URL: http://localhost:5001")
    print(" AI Query Endpoint: http://localhost:5001/ai-query")
    print(" Transaction Endpoint: http://localhost:5001/transaction")
    print(" Database: MySQL (kiosk)")
    print(" AI Model: Mistral via Ollama")
    print("=" * 60)

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/test-db', methods=['GET'])
def test_db():
    """
    Test database connection and basic query functionality.
    
    This endpoint is useful for debugging database connectivity issues.
    It performs a simple query to verify the database is working correctly.
    
    Returns:
        JSON response with test results
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Test a simple query
        cursor.execute("SELECT name, SUM(quantity) as total FROM order_items GROUP BY name ORDER BY total ASC LIMIT 1")
        result = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({
            "success": True,
            "message": "Database connection successful",
            "test_query_result": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database test failed: {str(e)}"
        }), 500

@app.route('/transaction', methods=['POST'])
def transaction():
    """
    Process a new transaction from the kiosk frontend.
    
    This endpoint handles the complete transaction flow:
    1. Receives order data from frontend
    2. Validates user and order information
    3. Stores data in MySQL database
    4. Returns success/error response
    
    Expected JSON payload:
    {
        "user": {
            "name": "John Doe",
            "phone": "123-456-7890",
            "email": "john@example.com"
        },
        "order": {
            "items": [...],
            "addOns": [...],
            "total": 25.50,
            "orderType": "Dine In",
            "seatNumber": "A1"
        },
        "paymentTime": "2025-07-29T10:30:00Z"
    }
    
    Returns:
        JSON response with transaction status
    """
    try:
        # Get transaction data from request
        transaction_data = request.get_json()
        
        if not transaction_data:
            return jsonify({
                "success": False,
                "error": "No transaction data provided"
            }), 400
        
        # Process the transaction using our service
        result = process_transaction(transaction_data)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Transaction processing failed: {str(e)}"
        }), 500

@app.route('/ai-query', methods=['POST'])
def ai_query():
    """
    Process AI-powered natural language queries.
    
    This endpoint handles user questions about sales data, inventory, and business metrics.
    It uses the Mistral LLM to convert natural language to SQL queries and returns
    human-readable responses.
    
    Expected JSON payload:
    {
        "question": "What is the best selling item?"
    }
    
    Returns:
        JSON response with AI-generated answer
    """
    try:
        # Get question from request
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "No question provided"
            }), 400
        
        question = data['question']
        
        # Process the AI query using our service
        result = process_ai_query(question)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"AI query processing failed: {str(e)}"
        }), 500

@app.route('/generate-daily-report', methods=['POST'])
def generate_daily_pdf():
    """
    Generate and download a daily sales report in PDF format.
    
    This endpoint creates a comprehensive daily report including:
    - Total revenue for the day
    - Number of orders
    - Best selling items
    - Customer insights
    
    Returns:
        PDF file download
    """
    try:
        # Generate the daily report
        pdf_path = pdf_reports.generate_daily_report()
        
        # Return the PDF file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"daily_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Daily report generation failed: {str(e)}"
        }), 500

@app.route('/generate-weekly-report', methods=['POST'])
def generate_weekly_pdf():
    """
    Generate and download a weekly sales report in PDF format.
    
    This endpoint creates a comprehensive weekly report including:
    - Weekly revenue summary
    - Daily breakdowns
    - Weekly trends
    - Performance metrics
    
    Returns:
        PDF file download
    """
    try:
        # Generate the weekly report
        pdf_path = pdf_reports.generate_weekly_report()
        
        # Return the PDF file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"weekly_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Weekly report generation failed: {str(e)}"
        }), 500

@app.route('/generate-monthly-report', methods=['POST'])
def generate_monthly_pdf():
    """
    Generate and download a monthly sales report in PDF format.
    
    This endpoint creates a comprehensive monthly report including:
    - Monthly revenue summary
    - Weekly breakdowns
    - Monthly trends
    - Business insights
    
    Returns:
        PDF file download
    """
    try:
        # Generate the monthly report
        pdf_path = pdf_reports.generate_monthly_report()
        
        # Return the PDF file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"monthly_report_{datetime.now().strftime('%Y%m')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Monthly report generation failed: {str(e)}"
        }), 500

# =============================================================================
# MAIN APPLICATION ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    # Print server information on startup
    print_server_info()
    
    # Start the Flask development server
    # Note: In production, use a proper WSGI server like Gunicorn
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True  # Set to False in production
    ) 