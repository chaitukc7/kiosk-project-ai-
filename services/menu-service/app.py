"""
Menu Service Module
==================

This module handles all menu-related operations including:
- Menu item retrieval
- Category management
- Menu data operations

Date: 2025
"""

import mysql.connector
from typing import Dict, List, Any, Optional, Tuple
from db import get_db

def get_all_categories() -> Tuple[List[Dict], str]:
    """
    Get all menu categories.
    
    Returns:
        Tuple[List[Dict], str]: (categories, error_message)
        - categories: List of category dictionaries
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return categories, ""
        
    except mysql.connector.Error as err:
        return [], f"Database error: {err}"

def get_menu_items_by_category(category_id: Optional[int] = None) -> Tuple[List[Dict], str]:
    """
    Get menu items, optionally filtered by category.
    
    Args:
        category_id (Optional[int]): Category ID to filter by
        
    Returns:
        Tuple[List[Dict], str]: (menu_items, error_message)
        - menu_items: List of menu item dictionaries
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        if category_id:
            cursor.execute(
                "SELECT * FROM menu_items WHERE category_id = %s ORDER BY name",
                (category_id,)
            )
        else:
            cursor.execute("SELECT * FROM menu_items ORDER BY name")
        
        menu_items = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return menu_items, ""
        
    except mysql.connector.Error as err:
        return [], f"Database error: {err}"

def get_menu_item_by_id(item_id: int) -> Tuple[Optional[Dict], str]:
    """
    Get a specific menu item by ID.
    
    Args:
        item_id (int): Menu item ID
        
    Returns:
        Tuple[Optional[Dict], str]: (menu_item, error_message)
        - menu_item: Menu item dictionary if found, None otherwise
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
        menu_item = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return menu_item, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def get_full_menu() -> Tuple[Dict, str]:
    """
    Get the complete menu with categories and items.
    
    Returns:
        Tuple[Dict, str]: (menu_data, error_message)
        - menu_data: Dictionary with categories and their items
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get all categories
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        # Get all menu items
        cursor.execute("SELECT * FROM menu_items ORDER BY category_id, name")
        menu_items = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        # Organize items by category
        menu_data = {
            "categories": categories,
            "items": menu_items,
            "menu_by_category": {}
        }
        
        for category in categories:
            category_id = category['id']
            menu_data["menu_by_category"][category_id] = {
                "category": category,
                "items": [item for item in menu_items if item['category_id'] == category_id]
            }
        
        return menu_data, ""
        
    except mysql.connector.Error as err:
        return {}, f"Database error: {err}"

# Flask App Setup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all menu categories."""
    try:
        categories, error = get_all_categories()
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "categories": categories
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get categories: {str(e)}"
        }), 500

@app.route('/menu-items', methods=['GET'])
def get_menu_items():
    """Get menu items, optionally filtered by category."""
    try:
        category_id = request.args.get('category_id', type=int)
        menu_items, error = get_menu_items_by_category(category_id)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "menu_items": menu_items
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get menu items: {str(e)}"
        }), 500

@app.route('/menu-items/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get a specific menu item by ID."""
    try:
        menu_item, error = get_menu_item_by_id(item_id)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        if not menu_item:
            return jsonify({
                "success": False,
                "error": "Menu item not found"
            }), 404
        
        return jsonify({
            "success": True,
            "menu_item": menu_item
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get menu item: {str(e)}"
        }), 500

@app.route('/menu', methods=['GET'])
def get_full_menu_endpoint():
    """Get the complete menu with categories and items."""
    try:
        menu_data, error = get_full_menu()
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "menu": menu_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get menu: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "menu-service",
        "port": 5003
    })

if __name__ == '__main__':
    print("Starting Menu Service...")
    print("Service URL: http://localhost:5003")
    print("Categories: http://localhost:5003/categories")
    print("Menu Items: http://localhost:5003/menu-items")
    print("Full Menu: http://localhost:5003/menu")
    print("Health Check: http://localhost:5003/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5003, debug=True) 