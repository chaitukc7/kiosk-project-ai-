from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Update these with your actual MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin123',
    'database': 'kiosk'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.json
    print("Received payload:", data)
    db = get_db()
    cursor = db.cursor()

    # Defensive: ensure user object has name and phone
    user_data = data.get('user', {})
    name = user_data.get('name', 'Guest')
    phone = user_data.get('phone', '')

    # Insert user (or get existing)
    cursor.execute("SELECT id FROM users WHERE phone=%s", (phone,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
    else:
        cursor.execute(
            "INSERT INTO users (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        user_id = cursor.lastrowid

    # Convert ISO8601 to MySQL DATETIME string
    payment_time = data['payment']['timestamp']
    try:
        # Remove Z if present
        if payment_time.endswith('Z'):
            payment_time = payment_time[:-1]
        # Parse and format
        dt = datetime.fromisoformat(payment_time)
        payment_time_mysql = dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print("Datetime conversion error:", e)
        payment_time_mysql = None

    # Insert transaction
    cursor.execute("""
        INSERT INTO transactions (user_id, seat_number, order_type, total, payment_method, payment_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data.get('seatNumber'),
        data.get('orderType'),
        data['order']['total'],
        data['payment']['method'],
        payment_time_mysql
    ))
    transaction_id = cursor.lastrowid

    # Insert order items
    for item in data['order'].get('items', []):
        cursor.execute("""
            INSERT INTO order_items (transaction_id, item_id, name, quantity, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (transaction_id, item['id'], item['name'], item['quantity'], item['price']))

    # Insert add-ons
    for add_on in data['order'].get('addOns', []):
        cursor.execute("""
            INSERT INTO add_ons (transaction_id, add_on_id, name, quantity, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (transaction_id, add_on['id'], add_on['name'], add_on['quantity'], add_on['price']))

    db.commit()
    cursor.close()
    db.close()
    return jsonify({"status": "success", "transaction_id": transaction_id})

if __name__ == '__main__':
    app.run(port=5001, debug=True) 