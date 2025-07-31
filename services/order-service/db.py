"""
Database Management Module
==========================

This module handles all database-related operations including:
- Database connection management
- Schema loading and validation
- SQL utility functions
- Database configuration

Date: 2025
"""

import mysql.connector
import re
import os
from typing import Optional, List, Tuple, Any

# Database configuration
DB_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "localhost"),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD", "admin123"),
    'database': os.getenv("MYSQL_DATABASE", "kiosk"),
    'autocommit': True
}

def get_db():
    """
    Create and return a database connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
        
    Raises:
        mysql.connector.Error: If connection fails
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

def load_schema() -> str:
    """
    Load database schema from schema_prompt.txt file.
    
    This function reads the database schema definition that is used
    by the LLM to understand the database structure and generate
    appropriate SQL queries.
    
    Returns:
        str: Database schema as a formatted string
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    try:
        with open('schema_prompt.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Warning: schema_prompt.txt not found. Using default schema.")
        return """
        Database Schema:
        - users (id, name, phone, email)
        - transactions (id, user_id, total, payment_time, order_type, seat_number)
        - order_items (id, transaction_id, name, quantity, price)
        - add_ons (id, transaction_id, name, quantity, price)
        """

def extract_sql(raw_output: str) -> str:
    """
    Extract SQL query from Mistral's response.
    
    This function handles both markdown format (```sql ... ```) and plain text,
    and cleans up malformed SQL by removing semicolons, WITH clauses, and
    multiple statements.
    
    Args:
        raw_output (str): Raw response from Mistral LLM
        
    Returns:
        str: Clean, extracted SQL query
    """
    # Try to find SQL in markdown code blocks
    match = re.search(r"```sql(.*?)```", raw_output, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        # If no markdown, extract SQL lines manually
        lines = raw_output.strip().splitlines()
        sql_lines = []
        found = False
        for line in lines:
            if line.strip().lower().startswith(("select", "with")):
                found = True
            if found:
                if line.strip() == "":
                    break
                sql_lines.append(line)
        sql = "\n".join(sql_lines).strip()
    
    # Clean up malformed SQL
    if sql:
        # Remove multiple semicolons and split on first semicolon
        if ";" in sql:
            sql = sql.split(";")[0].strip()
        
        # Remove WITH clauses and CTEs
        if "WITH" in sql.upper():
            # Find the main SELECT after WITH
            select_match = re.search(r"SELECT.*", sql, re.DOTALL | re.IGNORECASE)
            if select_match:
                sql = select_match.group(0).strip()
        
        # Remove any trailing semicolons
        sql = sql.rstrip(";")
        
        # Ensure it starts with SELECT
        if not sql.upper().startswith("SELECT"):
            return ""
    
    return sql

def check_aliases(sql: str) -> set:
    """
    Check for undeclared table aliases in SQL.
    
    This function analyzes SQL queries to identify aliases that are used
    but not properly declared in FROM/JOIN clauses, which can cause
    ambiguous column errors.
    
    Args:
        sql (str): SQL query to check
        
    Returns:
        set: Set of undeclared aliases
    """
    declared_aliases = set()
    used_aliases = set()
    
    # Find declared aliases in FROM/JOIN clauses
    from_join_lines = re.findall(r"(FROM|JOIN)\s+(\w+)\s+(?:AS\s+)?(\w+)", sql, re.IGNORECASE)
    for _, _, alias in from_join_lines:
        declared_aliases.add(alias.lower())
    
    # Find used aliases in the query
    alias_usage = re.findall(r"(\w+)\.\w+", sql)
    for alias in alias_usage:
        used_aliases.add(alias.lower())
    
    # Return undeclared aliases
    undeclared = used_aliases - declared_aliases
    return undeclared

def execute_query(sql: str) -> Tuple[List[Tuple], Optional[str]]:
    """
    Execute a SQL query and return results.
    
    Args:
        sql (str): SQL query to execute
        
    Returns:
        Tuple[List[Tuple], Optional[str]]: (results, error_message)
        - results: List of tuples containing query results
        - error_message: Error message if query fails, None if successful
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result, None
    except mysql.connector.Error as err:
        return [], str(err)

def format_query_results(result: List[Tuple]) -> str:
    """
    Format database query results into a readable string.
    
    Args:
        result (List[Tuple]): Raw query results
        
    Returns:
        str: Formatted result string
    """
    if not result:
        return "No data found."
    
    if len(result[0]) == 1:
        # Single column results
        return str(result[0][0])
    elif len(result[0]) == 2:
        # Two column results (name + value)
        formatted_items = [f"{row[0]} ({row[1]})" for row in result]
        return ", ".join(formatted_items)
    else:
        # Complex results
        formatted_items = [str(row) for row in result]
        return ", ".join(formatted_items) 