"""
AI Service Module
================

This module handles all AI/LLM-related operations including:
- Natural language to SQL conversion
- Response formatting and natural language generation
- Conversational query handling
- AI prompt management

Date: 2025
"""

import requests
import json
from typing import Dict, List, Tuple, Optional
from database import load_schema, extract_sql, check_aliases, execute_query, format_query_results

# Conversational phrases that should be handled directly without LLM
CONVERSATIONAL_PHRASES = [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
    "how are you", "how's it going", "what's up",
    "thank you", "thanks", "appreciate it",
    "bye", "goodbye", "see you", "talk to you later",
    "help", "what can you do", "capabilities"
]

# Business-related terms that should trigger AI processing
BUSINESS_QUESTIONS = [
    "revenue", "earnings", "sales", "orders", "customers", "items", "best", "least", "top", "average",
    "total", "count", "how much", "how many", "which day", "dine-in", "takeout", "pick up", "earn", "spend",
    "spent", "spending", "customer", "number", "amount", "popular", "selling", "yesterday", "today", "week", "month"
]

def is_conversational_query(question: str) -> bool:
    """
    Check if a question is conversational and should be handled directly.
    
    Args:
        question (str): The user's question
        
    Returns:
        bool: True if conversational, False if business-related
    """
    question_lower = question.lower()
    
    # Check for business terms first
    is_business = any(term in question_lower for term in BUSINESS_QUESTIONS)
    is_conversational = any(phrase in question_lower for phrase in CONVERSATIONAL_PHRASES)
    
    # If it contains business terms, it's not conversational
    if is_business:
        return False
    
    return is_conversational

def get_conversational_response(question: str) -> str:
    """
    Generate appropriate conversational responses for non-business queries.
    
    Args:
        question (str): The user's conversational question
        
    Returns:
        str: Appropriate conversational response
    """
    question_lower = question.lower()
    
    if any(phrase in question_lower for phrase in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! I'm Nova AI, your sales and inventory assistant. How can I help you today?"
    
    elif any(phrase in question_lower for phrase in ["how are you", "how's it going", "what's up"]):
        return "I'm doing great! Ready to help you with your sales data and inventory questions. What would you like to know?"
    
    elif any(phrase in question_lower for phrase in ["thank you", "thanks", "appreciate it"]):
        return "You're welcome! Is there anything else you'd like to know about your sales or inventory?"
    
    elif any(phrase in question_lower for phrase in ["bye", "goodbye", "see you", "talk to you later"]):
        return "Goodbye! Feel free to come back anytime if you need help with your sales data."
    
    elif any(phrase in question_lower for phrase in ["help", "what can you do", "capabilities"]):
        return "I can help you with sales analysis, inventory tracking, customer insights, and financial reports. I can answer questions about best-selling items, revenue, customer spending, order types, and much more. Just ask me anything about your business data!"
    
    else:
        return "Hello! I'm Nova AI, your sales and inventory assistant. How can I help you today?"

def create_ai_prompt(question: str) -> str:
    """
    Create a comprehensive prompt for the AI to generate SQL queries.
    
    Args:
        question (str): The user's question
        
    Returns:
        str: Formatted prompt for the AI
    """
    schema_text = load_schema()
    
    prompt = f"""
    You are a MySQL SQL expert. Generate ONLY the SQL query, no explanations.
    
    Given the following database schema:
    {schema_text}
    
    Question: \"\"\"{question}\"\"\"
    
    IMPORTANT: Use simple, direct queries without subqueries.
    
    For sales analysis: Use SUM(quantity) with GROUP BY name, ORDER BY total DESC for best selling, ASC for least selling
    For revenue analysis: Use SUM(total) from transactions table
    For customer analysis: Use COUNT(DISTINCT user_id) to count unique customers
    For date filtering: Use DATE(payment_time), YEARWEEK(payment_time), MONTH(payment_time), YEAR(payment_time)
    
    CRITICAL DATE RULES:
    - For "last month": Use MONTH(payment_time) = MONTH(DATE_SUB(CURDATE(), INTERVAL 1 MONTH)) AND YEAR(payment_time) = YEAR(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
    - NEVER use DATE(payment_time) >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) for "last month" queries
    - NEVER use BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() for "last month" queries
    - "Last month" means ONLY the previous calendar month, not the last 30 days
    - Example for "last month": WHERE MONTH(payment_time) = 6 AND YEAR(payment_time) = 2025 (if current month is July 2025)
    - For "yesterday": Use DATE(payment_time) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    - For "this week": Use YEARWEEK(payment_time) = YEARWEEK(CURDATE())
    - For "this month": Use MONTH(payment_time) = MONTH(CURDATE()) AND YEAR(payment_time) = YEAR(CURDATE())
    
    For order type analysis: Use GROUP BY order_type with COUNT(*)
    For customer order counts: JOIN users with transactions and use HAVING clause
    For tax calculations: Multiply total by 0.10 (10% tax rate)
    
    IMPORTANT SQL RULES:
    - Always use table aliases when joining (e.g., FROM transactions t JOIN users u)
    - For ambiguous columns, use table prefix (e.g., t.id, u.name)
    - For "this week": Use YEARWEEK(payment_time) = YEARWEEK(CURDATE())
    - For "today": Use DATE(payment_time) = CURDATE()
    - For "yesterday": Use DATE(payment_time) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    - For "this month": Use MONTH(payment_time) = MONTH(CURDATE()) AND YEAR(payment_time) = YEAR(CURDATE())
    - For order counts: Use COUNT(DISTINCT t.id) or COUNT(*)
    - For revenue: Use SUM(t.total)
    - For average order value: Use AVG(t.total)
    - NEVER use semicolons (;) in the middle of queries
    - NEVER use multiple SQL statements
    - NEVER use WITH clauses or CTEs
    - Use simple, direct queries only
    - For order type queries: Use t.order_type, COUNT(*) as count FROM transactions t WHERE...
    
    Only return the SQL query, nothing else.
    """
    
    return prompt

def query_ollama(prompt: str) -> Tuple[str, Optional[str]]:
    """
    Send a prompt to Ollama (Mistral LLM) and get the response.
    
    Args:
        prompt (str): The prompt to send to the AI
        
    Returns:
        Tuple[str, Optional[str]]: (response, error_message)
        - response: AI response if successful
        - error_message: Error message if failed, None if successful
    """
    try:
        print(f"Sending question to Mistral: {prompt.split('Question:')[1].split('IMPORTANT:')[0].strip() if 'Question:' in prompt else 'Unknown'}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt},
            stream=True,
            timeout=30
        )
        
        # Collect full response from LLM
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode("utf-8"))
                full_response += data.get("response", "")
        
        return full_response, None
        
    except requests.exceptions.ConnectionError:
        return "", "Connection error: Could not connect to Ollama service"
    except requests.exceptions.Timeout:
        return "", "Timeout error: Ollama service took too long to respond"
    except Exception as e:
        return "", f"Unexpected error: {str(e)}"

def format_natural_response(question: str, result: List[Tuple], formatted_result: str) -> str:
    """
    Convert raw database results into natural English responses.
    
    This function makes the chatbot responses more human-like and readable
    by analyzing the question type and data structure to generate appropriate
    natural language responses.
    
    Args:
        question (str): Original user question
        result (List[Tuple]): Raw database results
        formatted_result (str): Pre-formatted result string
        
    Returns:
        str: Natural language response
    """
    question_lower = question.lower()
    
    if not result:
        return "I couldn't find any data for that question."

    # Intelligent response generation based on question type and data structure
    if len(result[0]) == 1:
        # Single value results
        value = result[0][0]
        if value is None:
            return "No data found for that question."
        
        if "revenue" in question_lower or "sales" in question_lower or "earnings" in question_lower:
            return f"Total revenue is ${value}."
        elif "customers" in question_lower or "visitors" in question_lower:
            return f"{value} unique customers."
        elif "orders" in question_lower or "count" in question_lower:
            return f"{value} orders."
        else:
            return f"The result is {value}."
    
    elif len(result[0]) == 2:
        # Two-column results (name + value)
        if "spending" in question_lower or "customers" in question_lower:
            if len(result) > 1:
                customers = []
                for i, row in enumerate(result[:5], 1):
                    name, total = row
                    customers.append(f"{i}. {name}: ${total}")
                return f"Top spending customers:\n" + "\n".join(customers)
            else:
                name, total = result[0]
                return f"{name} spent ${total}."
        
        elif "selling" in question_lower or "popular" in question_lower:
            if "least" in question_lower or "worst" in question_lower:
                name, quantity = result[0]
                return f"The least selling item is {name} with {quantity} orders."
            else:
                name, quantity = result[0]
                return f"The best selling item is {name} with {quantity} orders."
        
        elif "orders" in question_lower or "types" in question_lower:
            types = []
            for row in result:
                order_type, count = row
                types.append(f"{order_type}: {count} orders")
            return f"Order breakdown: {', '.join(types)}."
        
        elif "customer" in question_lower and "count" in question_lower:
            # Customer count queries
            count = result[0][0]
            return f"{count} unique customers."
        
        elif "customer" in question_lower and ("spent" in question_lower or "spending" in question_lower):
            # Customer spending queries
            if len(result) > 1:
                customers = []
                for i, row in enumerate(result[:5], 1):
                    name, total = row
                    customers.append(f"{i}. {name}: ${total}")
                return f"Top spending customers:\n" + "\n".join(customers)
            else:
                name, total = result[0]
                return f"{name} spent ${total}."
        
        else:
            # Generic two-column response
            items = []
            for row in result[:5]:  # Limit to 5 items
                items.append(f"{row[0]} ({row[1]})")
            return f"Results: {', '.join(items)}"
    
    else:
        # Complex results - try to make them more readable
        if len(result) <= 3:
            # For small result sets, format them nicely
            formatted_items = []
            for row in result:
                if len(row) >= 4:  # Transaction-like data
                    formatted_items.append(f"Order {row[0]}: {row[2]} ({row[3]}) - ${row[4]}")
                else:
                    formatted_items.append(str(row))
            return f"Here's what I found: {', '.join(formatted_items)}"
        else:
            # For larger result sets, just show count
            return f"I found {len(result)} records for your query."

def process_ai_query(question: str) -> Dict:
    """
    Main function to process an AI query from start to finish.
    
    This function orchestrates the entire AI query processing pipeline:
    1. Check if query is conversational
    2. Generate AI prompt
    3. Query Ollama
    4. Extract and execute SQL
    5. Format response
    
    Args:
        question (str): User's question
        
    Returns:
        Dict: Response dictionary with success status, SQL, and result
    """
    # Check if this is a conversational query
    if is_conversational_query(question):
        response_text = get_conversational_response(question)
        return {
            "success": True,
            "question": question,
            "sql": "N/A (Conversational query)",
            "result": response_text
        }
    
    # Create AI prompt
    prompt = create_ai_prompt(question)
    
    # Query Ollama
    ai_response, error = query_ollama(prompt)
    if error:
        return {
            "success": False,
            "error": f"Sorry, I'm having trouble connecting to my AI service right now. Please try again later or contact support. ({error})"
        }
    
    # Extract SQL from AI response
    generated_sql = extract_sql(ai_response)
    print(f"Generated SQL: {generated_sql}")
    
    if not generated_sql:
        return {
            "success": False,
            "error": "Sorry, I couldn't understand that question properly. Please try rephrasing it or ask something simpler."
        }
    
    # Check for undeclared aliases
    undeclared_aliases = check_aliases(generated_sql)
    if undeclared_aliases:
        print(f"Warning: Undeclared alias(es): {undeclared_aliases}")
    
    # Execute SQL query
    result, db_error = execute_query(generated_sql)
    if db_error:
        print(f"MySQL Error: {db_error}")
        print(f"Generated SQL: {generated_sql}")
        return {
            "success": False,
            "error": "Sorry, I couldn't understand that question properly. Please try rephrasing it or ask something simpler."
        }
    
    # Format results
    formatted_result = format_query_results(result)
    natural_response = format_natural_response(question, result, formatted_result)
    
    return {
        "success": True,
        "question": question,
        "sql": generated_sql,
        "result": natural_response
    } 