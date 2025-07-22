-- Kiosk App MySQL Schema

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    seat_number VARCHAR(10),
    order_type VARCHAR(20),
    total DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20),
    payment_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    item_id VARCHAR(20),
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

CREATE TABLE IF NOT EXISTS add_ons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    add_on_id VARCHAR(20),
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
); 