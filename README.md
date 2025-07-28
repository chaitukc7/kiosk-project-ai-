# Kiosk App

A full-stack kiosk ordering system with a modern React frontend, a Python Flask backend, and a MySQL database.

---

## Features
- Users can select menu items, enter details, and place orders via a React frontend.
- Orders, user details, and payment info are sent to a Flask backend and stored in MySQL.
- Dine In orders require a seat number; Pick Up orders do not.
- Discounts and tax are shown in both checkout and receipt.
- Robust error handling and business logic.

---

## Technologies Used
- **Frontend:** Vite, TypeScript, React, shadcn-ui, Tailwind CSS
- **Backend:** Python, Flask, flask-cors, mysql-connector-python
- **Database:** MySQL

---

## Getting Started

### 1. Clone the Repository
```sh
git clone <YOUR_GIT_URL>
cd <YOUR_PROJECT_NAME>
```

### 2. Set Up the Database
- Open MySQL Workbench or your preferred client.
- Create the database and tables:
  ```sql
  CREATE DATABASE kiosk;
  USE kiosk;
  SOURCE backend/../kiosk_schema.sql;
  ```
  *(Or copy-paste the contents of `kiosk_schema.sql` and run in Workbench)*

### 3. Set Up the Backend
```sh
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
backend/venv/bin/python backend/app.py
```
- The backend runs on: `http://127.0.0.1:5001`

### 4. Set Up the Frontend
```sh
npm install
npm run dev
```
- The frontend runs on: `http://localhost:8080`

---

## Project Flow
1. **User places an order** in the React frontend.
2. **Frontend sends order data** to the Flask backend via POST.
3. **Backend processes and stores** the data in MySQL.
4. **Receipt and confirmation** are shown in the frontend.

---

## Editing and Collaboration
- Edit files directly in GitHub (pencil icon) and commit changes.
- Or use GitHub Codespaces for a cloud dev environment.

---

## Business Logic
- **Dine In:** Requires seat number.
- **Pick Up:** No seat number required.
- **Discounts and tax** are shown in both checkout and receipt.

---

## Troubleshooting
- If you see MySQL lock errors, restart your MySQL server.
- Ensure backend is running on port 5001 and frontend on 8080.
- Check the backend terminal for error messages if something fails.

---

## License
MIT
