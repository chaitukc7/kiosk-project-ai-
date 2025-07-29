"""
Transaction Service Module
=========================

This module handles all transaction-related operations including:
- Order processing and validation
- User data management
- Business rules enforcement
- Transaction data insertion

Date: 2025
"""

import mysql.connector
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from database import get_db

def validate_user_data(user_data: Dict) -> Tuple[bool, str]:
    """
    Validate user data before processing transaction.
    
    Args:
        user_data (Dict): User information dictionary
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        - is_valid: True if data is valid, False otherwise
        - error_message: Error description if invalid, empty string if valid
    """
    required_fields = ['name', 'phone']
    
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            return False, f"Missing required field: {field}"
    
    # Validate phone number format (basic validation)
    phone = user_data['phone']
    if not phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
        return False, "Invalid phone number format"
    
    return True, ""

def validate_order_data(order_data: Dict) -> Tuple[bool, str]:
    """
    Validate order data before processing transaction.
    
    Args:
        order_data (Dict): Order information dictionary
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        - is_valid: True if data is valid, False otherwise
        - error_message: Error description if invalid, empty string if valid
    """
    required_fields = ['items', 'total', 'orderType']
    
    for field in required_fields:
        if field not in order_data:
            return False, f"Missing required field: {field}"
    
    # Validate items
    if not order_data['items'] or len(order_data['items']) == 0:
        return False, "Order must contain at least one item"
    
    # Validate total
    try:
        total = float(order_data['total'])
        if total <= 0:
            return False, "Order total must be greater than 0"
    except (ValueError, TypeError):
        return False, "Invalid order total"
    
    # Validate order type
    valid_order_types = ['Dine In', 'Pick Up']
    if order_data['orderType'] not in valid_order_types:
        return False, f"Invalid order type. Must be one of: {', '.join(valid_order_types)}"
    
    # Validate seat number for Dine In orders
    if order_data['orderType'] == 'Dine In':
        if 'seatNumber' not in order_data or not order_data['seatNumber']:
            return False, "Seat number is required for Dine In orders"
    
    return True, ""

def insert_user(user_data: Dict) -> Tuple[Optional[int], str]:
    """
    Insert or update user data in the database.
    
    Args:
        user_data (Dict): User information dictionary
        
    Returns:
        Tuple[Optional[int], str]: (user_id, error_message)
        - user_id: User ID if successful, None if failed
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if user already exists (by phone number)
        cursor.execute(
            "SELECT id FROM users WHERE phone = %s",
            (user_data['phone'],)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Update existing user
            cursor.execute(
                "UPDATE users SET name = %s, email = %s WHERE phone = %s",
                (user_data['name'], user_data.get('email', ''), user_data['phone'])
            )
            user_id = existing_user[0]
        else:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (name, phone, email) VALUES (%s, %s, %s)",
                (user_data['name'], user_data['phone'], user_data.get('email', ''))
            )
            user_id = cursor.lastrowid
        
        db.commit()
        cursor.close()
        db.close()
        
        return user_id, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def insert_transaction(user_id: int, order_data: Dict, payment_time: str) -> Tuple[Optional[int], str]:
    """
    Insert transaction data into the database.
    
    Args:
        user_id (int): User ID from users table
        order_data (Dict): Order information dictionary
        payment_time (str): Payment timestamp
        
    Returns:
        Tuple[Optional[int], str]: (transaction_id, error_message)
        - transaction_id: Transaction ID if successful, None if failed
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Parse payment time
        try:
            payment_datetime = datetime.fromisoformat(payment_time.replace('Z', '+00:00'))
            formatted_time = payment_datetime.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None, "Invalid payment time format"
        
        # Insert transaction
        cursor.execute(
            """INSERT INTO transactions 
               (user_id, total, payment_time, order_type, seat_number) 
               VALUES (%s, %s, %s, %s, %s)""",
            (
                user_id,
                order_data['total'],
                formatted_time,
                order_data['orderType'],
                order_data.get('seatNumber', None)
            )
        )
        
        transaction_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        
        return transaction_id, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def insert_order_items(transaction_id: int, items: List[Dict]) -> str:
    """
    Insert order items into the database.
    
    Args:
        transaction_id (int): Transaction ID from transactions table
        items (List[Dict]): List of order items
        
    Returns:
        str: Error message if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        for item in items:
            cursor.execute(
                "INSERT INTO order_items (transaction_id, name, quantity, price) VALUES (%s, %s, %s, %s)",
                (transaction_id, item['name'], item['quantity'], item['price'])
            )
        
        db.commit()
        cursor.close()
        db.close()
        
        return ""
        
    except mysql.connector.Error as err:
        return f"Database error: {err}"

def insert_add_ons(transaction_id: int, add_ons: List[Dict]) -> str:
    """
    Insert add-ons into the database.
    
    Args:
        transaction_id (int): Transaction ID from transactions table
        add_ons (List[Dict]): List of add-ons
        
    Returns:
        str: Error message if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        for add_on in add_ons:
            cursor.execute(
                "INSERT INTO add_ons (transaction_id, name, quantity, price) VALUES (%s, %s, %s, %s)",
                (transaction_id, add_on['name'], add_on['quantity'], add_on['price'])
            )
        
        db.commit()
        cursor.close()
        db.close()
        
        return ""
        
    except mysql.connector.Error as err:
        return f"Database error: {err}"

def process_transaction(transaction_data: Dict) -> Dict:
    """
    Main function to process a complete transaction.
    
    This function orchestrates the entire transaction processing pipeline:
    1. Validate user and order data
    2. Insert/update user data
    3. Insert transaction data
    4. Insert order items
    5. Insert add-ons
    
    Args:
        transaction_data (Dict): Complete transaction data from frontend
        
    Returns:
        Dict: Response dictionary with success status and message
    """
    try:
        # Extract data from request
        user_data = transaction_data.get('user', {})
        order_data = transaction_data.get('order', {})
        payment_time = transaction_data.get('paymentTime', '')
        
        # Validate user data
        is_valid, error_msg = validate_user_data(user_data)
        if not is_valid:
            return {"success": False, "error": error_msg}
        
        # Validate order data
        is_valid, error_msg = validate_order_data(order_data)
        if not is_valid:
            return {"success": False, "error": error_msg}
        
        # Insert/update user
        user_id, error_msg = insert_user(user_data)
        if user_id is None:
            return {"success": False, "error": error_msg}
        
        # Insert transaction
        transaction_id, error_msg = insert_transaction(user_id, order_data, payment_time)
        if transaction_id is None:
            return {"success": False, "error": error_msg}
        
        # Insert order items
        error_msg = insert_order_items(transaction_id, order_data['items'])
        if error_msg:
            return {"success": False, "error": error_msg}
        
        # Insert add-ons (if any)
        if 'addOns' in order_data and order_data['addOns']:
            error_msg = insert_add_ons(transaction_id, order_data['addOns'])
            if error_msg:
                return {"success": False, "error": error_msg}
        
        return {
            "success": True,
            "message": "Transaction processed successfully",
            "transaction_id": transaction_id,
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"} 