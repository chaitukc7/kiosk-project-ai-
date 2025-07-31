"""
Payment Service Module
=====================

This module handles all payment-related operations including:
- Payment processing
- Payment method management
- Payment status tracking

Date: 2025
"""

import mysql.connector
import datetime
from typing import Dict, List, Any, Optional, Tuple
from db import get_db

def process_payment(transaction_id: int, payment_method: str, amount: float) -> Tuple[bool, str]:
    """
    Process a payment for a transaction.
    
    Args:
        transaction_id (int): Transaction ID
        payment_method (str): Payment method (Cash, Card, etc.)
        amount (float): Payment amount
        
    Returns:
        Tuple[bool, str]: (success, error_message)
        - success: True if successful, False otherwise
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Update transaction with payment method
        cursor.execute(
            "UPDATE transactions SET payment_method = %s WHERE id = %s",
            (payment_method, transaction_id)
        )
        
        # Insert payment record
        cursor.execute(
            "INSERT INTO payments (transaction_id, amount, payment_method, payment_time) VALUES (%s, %s, %s, %s)",
            (transaction_id, amount, payment_method, datetime.datetime.now())
        )
        
        db.commit()
        cursor.close()
        db.close()
        
        return True, ""
        
    except mysql.connector.Error as err:
        return False, f"Database error: {err}"

def get_payment_methods() -> List[Dict]:
    """
    Get available payment methods.
    
    Returns:
        List[Dict]: List of payment methods
    """
    return [
        {"id": "cash", "name": "Cash", "icon": "💵"},
        {"id": "card", "name": "Card", "icon": "💳"},
        {"id": "mobile", "name": "Mobile Payment", "icon": "📱"},
        {"id": "split", "name": "Split Bill", "icon": "✂️"}
    ]

def get_payment_status(transaction_id: int) -> Tuple[Optional[Dict], str]:
    """
    Get payment status for a transaction.
    
    Args:
        transaction_id (int): Transaction ID
        
    Returns:
        Tuple[Optional[Dict], str]: (payment_data, error_message)
        - payment_data: Payment information if found, None otherwise
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM payments WHERE transaction_id = %s ORDER BY payment_time DESC LIMIT 1",
            (transaction_id,)
        )
        payment = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return payment, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

# Flask App Setup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process-payment', methods=['POST'])
def process_payment_endpoint():
    """Process a payment."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        required_fields = ['transaction_id', 'payment_method', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        transaction_id = data['transaction_id']
        payment_method = data['payment_method']
        amount = float(data['amount'])
        
        success, error = process_payment(transaction_id, payment_method, amount)
        
        if not success:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "message": "Payment processed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Payment processing failed: {str(e)}"
        }), 500

@app.route('/payment-methods', methods=['GET'])
def get_payment_methods_endpoint():
    """Get available payment methods."""
    try:
        payment_methods = get_payment_methods()
        
        return jsonify({
            "success": True,
            "payment_methods": payment_methods
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get payment methods: {str(e)}"
        }), 500

@app.route('/payment-status/<int:transaction_id>', methods=['GET'])
def get_payment_status_endpoint(transaction_id):
    """Get payment status for a transaction."""
    try:
        payment, error = get_payment_status(transaction_id)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "payment": payment
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get payment status: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "service": "payment-service",
        "port": 5006,
        "status": "healthy"
    })

if __name__ == '__main__':
    print("Starting Payment Service...")
    print("Service URL: http://localhost:5006")
    print("Process Payment: http://localhost:5006/process-payment")
    print("Payment Methods: http://localhost:5006/payment-methods")
    print("Payment Status: http://localhost:5006/payment-status/<transaction_id>")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5006, debug=True) 