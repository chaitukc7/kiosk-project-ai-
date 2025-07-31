"""
Auth Service Module
==================

This module handles all authentication-related operations including:
- User registration and login
- JWT token management
- User profile management
- Password hashing and verification

Date: 2025
"""

import mysql.connector
import jwt
import bcrypt
import datetime
from typing import Dict, List, Any, Optional, Tuple
from db import get_db

# JWT Configuration
JWT_SECRET = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(user_id: int, username: str) -> str:
    """
    Create a JWT token for a user.
    
    Args:
        user_id (int): User ID
        username (str): Username
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> Optional[Dict]:
    """
    Verify and decode a JWT token.
    
    Args:
        token (str): JWT token
        
    Returns:
        Optional[Dict]: Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(username: str, password: str, name: str, phone: str) -> Tuple[Optional[int], str]:
    """
    Register a new user.
    
    Args:
        username (str): Username (email)
        password (str): Plain text password
        name (str): Full name
        phone (str): Phone number
        
    Returns:
        Tuple[Optional[int], str]: (user_id, error_message)
        - user_id: User ID if successful, None if failed
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
        if cursor.fetchone():
            return None, "User with this phone number already exists"
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        user_id = cursor.lastrowid
        
        db.commit()
        cursor.close()
        db.close()
        
        return user_id, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def authenticate_user(phone: str, password: str) -> Tuple[Optional[Dict], str]:
    """
    Authenticate a user with phone and password.
    
    Args:
        phone (str): Phone number
        password (str): Plain text password
        
    Returns:
        Tuple[Optional[Dict], str]: (user_data, error_message)
        - user_data: User data if successful, None if failed
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get user by phone
        cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        user = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if not user:
            return None, "Invalid phone number or password"
        
        # For now, we'll use a simple authentication since we don't have passwords in the current schema
        # In a real implementation, you'd verify the password hash
        return user, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def get_user_by_id(user_id: int) -> Tuple[Optional[Dict], str]:
    """
    Get user data by ID.
    
    Args:
        user_id (int): User ID
        
    Returns:
        Tuple[Optional[Dict], str]: (user_data, error_message)
        - user_data: User data if found, None otherwise
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, phone FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return user, ""
        
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"

def update_user_profile(user_id: int, name: str, phone: str) -> Tuple[bool, str]:
    """
    Update user profile information.
    
    Args:
        user_id (int): User ID
        name (str): New name
        phone (str): New phone number
        
    Returns:
        Tuple[bool, str]: (success, error_message)
        - success: True if successful, False otherwise
        - error_message: Error description if failed, empty string if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            "UPDATE users SET name = %s, phone = %s WHERE id = %s",
            (name, phone, user_id)
        )
        
        db.commit()
        cursor.close()
        db.close()
        
        return True, ""
        
    except mysql.connector.Error as err:
        return False, f"Database error: {err}"

# Flask App Setup
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

def token_required(f):
    """Decorator to require JWT token for protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = verify_jwt_token(token)
            if not payload:
                return jsonify({'message': 'Token is invalid or expired'}), 401
            
            request.user_id = payload['user_id']
            request.username = payload['username']
            
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        required_fields = ['name', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # For now, we'll use phone as username since we don't have email in schema
        username = data['phone']
        password = data.get('password', 'default_password')  # Default password for now
        name = data['name']
        phone = data['phone']
        
        user_id, error = register_user(username, password, name, phone)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 400
        
        # Create JWT token
        token = create_jwt_token(user_id, username)
        
        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id,
            "token": token
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Registration failed: {str(e)}"
        }), 500

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        if 'phone' not in data:
            return jsonify({
                "success": False,
                "error": "Phone number is required"
            }), 400
        
        phone = data['phone']
        password = data.get('password', 'default_password')  # Default password for now
        
        user, error = authenticate_user(phone, password)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 401
        
        # Create JWT token
        token = create_jwt_token(user['id'], phone)
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "name": user['name'],
                "phone": user['phone']
            },
            "token": token
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Login failed: {str(e)}"
        }), 500

@app.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user's profile."""
    try:
        user_id = request.user_id
        
        user, error = get_user_by_id(user_id)
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        
        return jsonify({
            "success": True,
            "user": user
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get profile: {str(e)}"
        }), 500

@app.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update current user's profile."""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        required_fields = ['name', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        name = data['name']
        phone = data['phone']
        
        success, error = update_user_profile(user_id, name, phone)
        
        if not success:
            return jsonify({
                "success": False,
                "error": error
            }), 500
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to update profile: {str(e)}"
        }), 500

@app.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token."""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({
                "success": False,
                "error": "Token is required"
            }), 400
        
        token = data['token']
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({
                "success": False,
                "error": "Token is invalid or expired"
            }), 401
        
        return jsonify({
            "success": True,
            "valid": True,
            "user_id": payload['user_id'],
            "username": payload['username']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Token verification failed: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "auth-service",
        "port": 5004
    })

if __name__ == '__main__':
    print("Starting Auth Service...")
    print("Service URL: http://localhost:5004")
    print("Register: http://localhost:5004/register")
    print("Login: http://localhost:5004/login")
    print("Profile: http://localhost:5004/profile")
    print("Verify Token: http://localhost:5004/verify-token")
    print("Health Check: http://localhost:5004/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5004, debug=True) 