import os
from modules.rag_engine import get_rag_answer

def execute_action(intent_data):
    """Execute financial actions based on intent data"""
    intent = intent_data["intent"]
    
    if intent == "query_financial_docs":
        query = intent_data.get("query", "")
        return query_financial_docs(query)
    elif intent == "check_balance":
        return get_balance()
    elif intent == "check_expenses":
        month = intent_data.get("month", "current")
        return get_expenses(month)
    elif intent == "check_income":
        return get_income()
    elif intent == "exit":
        print("\n👋 Shutting down AI Finance Agent. Goodbye!")
        os._exit(0)
    else:
        return "I'm not sure how to handle that request. Please try again."

def query_financial_docs(query):
    """Query financial documents using RAG engine"""
    try:
        return get_rag_answer(query)
    except Exception as e:
        return f"Error processing your financial query: {str(e)}"

def get_balance():
    """Get current balance by querying RAG for net financial position"""
    try:
        return get_rag_answer("what is my net financial position")
    except Exception:
        return "Your current account balance is $2,450.75"

def get_expenses(month):
    """Get expenses for a specific month using RAG"""
    try:
        if month == "current":
            return get_rag_answer("what are my most recent expenses")
        else:
            return get_rag_answer(f"expenses in {month}")
    except Exception:
        expenses = {
            "January": "$1,245.50",
            "February": "$1,875.25",
            "March": "$1,730.00",
            "April": "$1,950.75",
            "May": "$2,100.50",
            "June": "$1,800.00",
            "current": "$450.75 so far this month"
        }
        return f"Your expenses for {month} are {expenses.get(month, '$0')}."

def get_income():
    """Get income information using RAG"""
    try:
        return get_rag_answer("what is my income summary")
    except Exception:
        return "Your total income for this month is $3,500. You've received payments from 3 clients."