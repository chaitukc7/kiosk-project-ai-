# =============================================================================
# PDF REPORT GENERATOR FOR KIOSK APP
# =============================================================================
# This module generates comprehensive PDF reports for:
# - Daily reports (Today's data)
# - Weekly reports (Last week's data) 
# - Monthly reports (This month's data)
# =============================================================================

import mysql.connector
from fpdf import FPDF
from datetime import datetime, timedelta
import os

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# MySQL connection settings - same as in app.py
# Update the password below with your MySQL root password
MYSQL_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'admin123',  # CHANGE THIS TO YOUR MYSQL PASSWORD
    'database': 'kiosk'
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def run_query(query, params=None):
    """
    Execute a SQL query and return results.
    This function handles database connections and query execution.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Parameters for the query
        
    Returns:
        list: Query results as list of tuples
        
    Raises:
        mysql.connector.Error: If database connection or query fails
    """
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        
        # Execute query with optional parameters
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Close connection
        cursor.close()
        connection.close()
        
        return results
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise

def init_pdf(title):
    """
    Initialize a new PDF document with proper formatting.
    Sets up fonts, margins, and title for the report.
    
    Args:
        title (str): Title for the PDF report
        
    Returns:
        FPDF: Configured PDF object
    """
    # Create PDF object with A4 page size
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    
    return pdf

def add_table(pdf, headers, data, title=""):
    """
    Add a formatted table to the PDF document.
    Creates a table with headers and data rows.
    
    Args:
        pdf (FPDF): PDF object to add table to
        headers (list): Column headers
        data (list): Table data as list of tuples
        title (str, optional): Table title
    """
    # Add table title if provided
    if title:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, title, ln=True)
        pdf.ln(2)
    
    # Set font for table
    pdf.set_font('Arial', 'B', 10)
    
    # Calculate column widths (equal distribution)
    col_width = 190 / len(headers)
    
    # Add headers
    for header in headers:
        pdf.cell(col_width, 8, str(header), border=1, align='C')
    pdf.ln()
    
    # Add data rows
    pdf.set_font('Arial', '', 9)
    if data:
        for row in data:
            for item in row:
                # Truncate long text to fit in cell
                text = str(item)[:20] + "..." if len(str(item)) > 20 else str(item)
                pdf.cell(col_width, 6, text, border=1, align='C')
            pdf.ln()
    else:
        # Show "No data available" if no results
        pdf.cell(190, 6, "No data available", border=1, align='C')
        pdf.ln()
    
    pdf.ln(5)

# =============================================================================
# REPORT GENERATION FUNCTIONS
# =============================================================================

def generate_daily_report():
    """
    Generate daily report for today's data.
    Creates a comprehensive PDF report showing today's sales, orders, and analytics.
    
    Returns:
        str: Path to generated PDF file
    """
    # Initialize PDF with title
    pdf = init_pdf("Today's Restaurant Report")
    
    try:
        # Get today's date for filtering
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Today's Sales Summary
        sales_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total) as total_revenue,
            AVG(total) as average_order_value
        FROM transactions 
        WHERE DATE(payment_time) = %s
        """
        sales_data = run_query(sales_query, (today,))
        
        if sales_data and sales_data[0][0]:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, "Today's Sales Summary", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, f"Total Orders: {sales_data[0][0]}", ln=True)
            pdf.cell(0, 6, f"Total Revenue: ${sales_data[0][1]:.2f}", ln=True)
            pdf.cell(0, 6, f"Average Order Value: ${sales_data[0][2]:.2f}", ln=True)
        else:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, "Today's Sales Summary", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, "No sales recorded today", ln=True)
        
        pdf.ln(10)
        
        # 2. Top Selling Items Today
        top_items_query = """
        SELECT 
            oi.name,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.price) as total_revenue
        FROM order_items oi
        JOIN transactions t ON oi.transaction_id = t.id
        WHERE DATE(t.payment_time) = %s
        GROUP BY oi.name
        ORDER BY total_quantity DESC
        LIMIT 5
        """
        top_items = run_query(top_items_query, (today,))
        add_table(pdf, ["Item", "Quantity Sold", "Revenue"], top_items, "Top Selling Items Today")
        
        # 3. Top Selling Add-ons Today
        top_addons_query = """
        SELECT 
            a.name,
            SUM(a.quantity) as total_quantity,
            SUM(a.quantity * a.price) as total_revenue
        FROM add_ons a
        JOIN transactions t ON a.transaction_id = t.id
        WHERE DATE(t.payment_time) = %s
        GROUP BY a.name
        ORDER BY total_quantity DESC
        LIMIT 5
        """
        top_addons = run_query(top_addons_query, (today,))
        add_table(pdf, ["Add-on", "Quantity Sold", "Revenue"], top_addons, "Top Selling Add-ons Today")
        
        # 4. Order Types Today
        order_types_query = """
        SELECT 
            order_type,
            COUNT(*) as count,
            SUM(total) as total_revenue
        FROM transactions
        WHERE DATE(payment_time) = %s
        GROUP BY order_type
        """
        order_types = run_query(order_types_query, (today,))
        add_table(pdf, ["Order Type", "Count", "Revenue"], order_types, "Orders by Type Today")
        
        # 5. Recent Transactions
        recent_transactions_query = """
        SELECT 
            t.id,
            u.name as customer_name,
            t.order_type,
            t.total,
            t.payment_method,
            t.payment_time
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        WHERE DATE(t.payment_time) = %s
        ORDER BY t.payment_time DESC
        LIMIT 10
        """
        recent_transactions = run_query(recent_transactions_query, (today,))
        add_table(pdf, ["ID", "Customer", "Type", "Total", "Payment", "Time"], recent_transactions, "Recent Transactions Today")
        
    except Exception as e:
        # Handle errors gracefully
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Error generating report", ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"Error: {str(e)}", ln=True)
    
    # Save PDF file
    filename = f"daily_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)
    pdf.output(filepath)
    
    return filepath

def generate_weekly_report():
    """
    Generate weekly report for last week's data.
    Creates a comprehensive PDF report showing last week's sales, orders, and analytics.
    
    Returns:
        str: Path to generated PDF file
    """
    # Initialize PDF with title
    pdf = init_pdf("Weekly Restaurant Report")
    
    try:
        # Calculate last week's date range
        today = datetime.now()
        last_week_start = today - timedelta(days=today.weekday() + 7)
        last_week_end = last_week_start + timedelta(days=6)
        
        # 1. Weekly Sales Summary
        sales_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total) as total_revenue,
            AVG(total) as average_order_value
        FROM transactions 
        WHERE DATE(payment_time) BETWEEN %s AND %s
        """
        sales_data = run_query(sales_query, (last_week_start.strftime('%Y-%m-%d'), last_week_end.strftime('%Y-%m-%d')))
        
        if sales_data and sales_data[0][0]:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, f"Weekly Sales Summary ({last_week_start.strftime('%Y-%m-%d')} to {last_week_end.strftime('%Y-%m-%d')})", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, f"Total Orders: {sales_data[0][0]}", ln=True)
            pdf.cell(0, 6, f"Total Revenue: ${sales_data[0][1]:.2f}", ln=True)
            pdf.cell(0, 6, f"Average Order Value: ${sales_data[0][2]:.2f}", ln=True)
        else:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, "Weekly Sales Summary", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, "No sales recorded this week", ln=True)
        
        pdf.ln(10)
        
        # 2. Top Selling Items This Week
        top_items_query = """
        SELECT 
            oi.name,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.price) as total_revenue
        FROM order_items oi
        JOIN transactions t ON oi.transaction_id = t.id
        WHERE DATE(t.payment_time) BETWEEN %s AND %s
        GROUP BY oi.name
        ORDER BY total_quantity DESC
        LIMIT 10
        """
        top_items = run_query(top_items_query, (last_week_start.strftime('%Y-%m-%d'), last_week_end.strftime('%Y-%m-%d')))
        add_table(pdf, ["Item", "Quantity Sold", "Revenue"], top_items, "Top Selling Items This Week")
        
        # 3. Daily Sales Breakdown
        daily_sales_query = """
        SELECT 
            DATE(payment_time) as date,
            COUNT(*) as orders,
            SUM(total) as revenue
        FROM transactions
        WHERE DATE(payment_time) BETWEEN %s AND %s
        GROUP BY DATE(payment_time)
        ORDER BY date
        """
        daily_sales = run_query(daily_sales_query, (last_week_start.strftime('%Y-%m-%d'), last_week_end.strftime('%Y-%m-%d')))
        add_table(pdf, ["Date", "Orders", "Revenue"], daily_sales, "Daily Sales Breakdown")
        
        # 4. Order Types This Week
        order_types_query = """
        SELECT 
            order_type,
            COUNT(*) as count,
            SUM(total) as total_revenue
        FROM transactions
        WHERE DATE(payment_time) BETWEEN %s AND %s
        GROUP BY order_type
        """
        order_types = run_query(order_types_query, (last_week_start.strftime('%Y-%m-%d'), last_week_end.strftime('%Y-%m-%d')))
        add_table(pdf, ["Order Type", "Count", "Revenue"], order_types, "Orders by Type This Week")
        
        # 5. Top Customers This Week
        top_customers_query = """
        SELECT 
            u.name,
            COUNT(*) as order_count,
            SUM(t.total) as total_spent
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        WHERE DATE(t.payment_time) BETWEEN %s AND %s
        GROUP BY u.id, u.name
        ORDER BY total_spent DESC
        LIMIT 10
        """
        top_customers = run_query(top_customers_query, (last_week_start.strftime('%Y-%m-%d'), last_week_end.strftime('%Y-%m-%d')))
        add_table(pdf, ["Customer", "Orders", "Total Spent"], top_customers, "Top Customers This Week")
        
    except Exception as e:
        # Handle errors gracefully
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Error generating report", ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"Error: {str(e)}", ln=True)
    
    # Save PDF file
    filename = f"weekly_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)
    pdf.output(filepath)
    
    return filepath

def generate_monthly_report():
    """
    Generate monthly report for this month's data.
    Creates a comprehensive PDF report showing this month's sales, orders, and analytics.
    
    Returns:
        str: Path to generated PDF file
    """
    # Initialize PDF with title
    pdf = init_pdf("Monthly Restaurant Report")
    
    try:
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # 1. Monthly Sales Summary
        sales_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total) as total_revenue,
            AVG(total) as average_order_value
        FROM transactions 
        WHERE MONTH(payment_time) = %s AND YEAR(payment_time) = %s
        """
        sales_data = run_query(sales_query, (current_month, current_year))
        
        if sales_data and sales_data[0][0]:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, f"Monthly Sales Summary ({datetime.now().strftime('%B %Y')})", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, f"Total Orders: {sales_data[0][0]}", ln=True)
            pdf.cell(0, 6, f"Total Revenue: ${sales_data[0][1]:.2f}", ln=True)
            pdf.cell(0, 6, f"Average Order Value: ${sales_data[0][2]:.2f}", ln=True)
        else:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, "Monthly Sales Summary", ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, "No sales recorded this month", ln=True)
        
        pdf.ln(10)
        
        # 2. Top Selling Items This Month
        top_items_query = """
        SELECT 
            oi.name,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.price) as total_revenue
        FROM order_items oi
        JOIN transactions t ON oi.transaction_id = t.id
        WHERE MONTH(t.payment_time) = %s AND YEAR(t.payment_time) = %s
        GROUP BY oi.name
        ORDER BY total_quantity DESC
        LIMIT 15
        """
        top_items = run_query(top_items_query, (current_month, current_year))
        add_table(pdf, ["Item", "Quantity Sold", "Revenue"], top_items, "Top Selling Items This Month")
        
        # 3. Weekly Sales Breakdown
        weekly_sales_query = """
        SELECT 
            WEEK(payment_time) as week_number,
            COUNT(*) as orders,
            SUM(total) as revenue
        FROM transactions
        WHERE MONTH(payment_time) = %s AND YEAR(payment_time) = %s
        GROUP BY WEEK(payment_time)
        ORDER BY week_number
        """
        weekly_sales = run_query(weekly_sales_query, (current_month, current_year))
        add_table(pdf, ["Week", "Orders", "Revenue"], weekly_sales, "Weekly Sales Breakdown")
        
        # 4. Order Types This Month
        order_types_query = """
        SELECT 
            order_type,
            COUNT(*) as count,
            SUM(total) as total_revenue
        FROM transactions
        WHERE MONTH(payment_time) = %s AND YEAR(payment_time) = %s
        GROUP BY order_type
        """
        order_types = run_query(order_types_query, (current_month, current_year))
        add_table(pdf, ["Order Type", "Count", "Revenue"], order_types, "Orders by Type This Month")
        
        # 5. Top Customers This Month
        top_customers_query = """
        SELECT 
            u.name,
            COUNT(*) as order_count,
            SUM(t.total) as total_spent
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        WHERE MONTH(t.payment_time) = %s AND YEAR(t.payment_time) = %s
        GROUP BY u.id, u.name
        ORDER BY total_spent DESC
        LIMIT 15
        """
        top_customers = run_query(top_customers_query, (current_month, current_year))
        add_table(pdf, ["Customer", "Orders", "Total Spent"], top_customers, "Top Customers This Month")
        
        # 6. Add-ons Performance This Month
        addons_query = """
        SELECT 
            a.name,
            SUM(a.quantity) as total_quantity,
            SUM(a.quantity * a.price) as total_revenue
        FROM add_ons a
        JOIN transactions t ON a.transaction_id = t.id
        WHERE MONTH(t.payment_time) = %s AND YEAR(t.payment_time) = %s
        GROUP BY a.name
        ORDER BY total_quantity DESC
        LIMIT 10
        """
        addons = run_query(addons_query, (current_month, current_year))
        add_table(pdf, ["Add-on", "Quantity Sold", "Revenue"], addons, "Add-ons Performance This Month")
        
    except Exception as e:
        # Handle errors gracefully
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Error generating report", ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"Error: {str(e)}", ln=True)
    
    # Save PDF file
    filename = f"monthly_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)
    pdf.output(filepath)
    
    return filepath

# =============================================================================
# MAIN EXECUTION (FOR TESTING)
# =============================================================================
# This section runs when the file is executed directly for testing

if __name__ == "__main__":
    print("Generating PDF reports...")
    try:
        # Generate all three types of reports
        daily_file = generate_daily_report()
        print(f" Daily report saved: {daily_file}")
        
        weekly_file = generate_weekly_report()
        print(f" Weekly report saved: {weekly_file}")
        
        monthly_file = generate_monthly_report()
        print(f" Monthly report saved: {monthly_file}")
        
        print("\n All reports generated successfully!")
        print(" Check the 'reports' folder for the generated PDF files.")
        
    except Exception as e:
        print(f" Error generating reports: {e}")
        print(" Make sure:")
        print("   - MySQL is running")
        print("   - Database 'kiosk' exists")
        print("   - Tables are created")
        print("   - FPDF is installed: pip install fpdf") 