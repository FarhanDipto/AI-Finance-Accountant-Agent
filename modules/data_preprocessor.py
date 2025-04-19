import os
import re
import json
from datetime import datetime

def preprocess_financial_data(input_file, output_file=None):
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}_processed.json"
    
    invoices = []
    incomes = []

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        invoice_match = re.match(r'Invoice #(\d+) \| (.*?) \| (.*?) \| \$(\d+)', line)
        income_match = re.match(r'Income #(\d+) \| (.*?) \| (.*?) \| \$(\d+)', line)
        
        if invoice_match:
            invoice_id, date_str, description, amount = invoice_match.groups()
            
            try:
                date_obj = datetime.strptime(date_str, '%B %d, %Y')
                
                invoice = {
                    'id': invoice_id,
                    'date': date_obj.strftime('%Y-%m-%d'),
                    'month': date_obj.strftime('%B'),
                    'description': description,
                    'amount': int(amount),
                    'raw_text': line,
                    'type': 'expense'
                }

                invoice['category'] = categorize_expense(description)
                
                invoices.append(invoice)
            except Exception as e:
                print(f"Error parsing invoice: {line}. Error: {e}")
                
        elif income_match:
            income_id, date_str, description, amount = income_match.groups()
            
            try:
                date_obj = datetime.strptime(date_str, '%B %d, %Y')

                income = {
                    'id': income_id,
                    'date': date_obj.strftime('%Y-%m-%d'),
                    'month': date_obj.strftime('%B'),
                    'description': description,
                    'amount': int(amount),
                    'raw_text': line,
                    'type': 'income'
                }

                income['category'] = categorize_income(description)
                
                incomes.append(income)
            except Exception as e:
                print(f"Error parsing income: {line}. Error: {e}")

    financial_data = {
        'invoices': invoices,
        'incomes': incomes,
        'summary': {
            'total_expenses': sum(invoice['amount'] for invoice in invoices),
            'total_income': sum(income['amount'] for income in incomes),
            'net_profit': sum(income['amount'] for income in incomes) - sum(invoice['amount'] for invoice in invoices),
            'invoice_count': len(invoices),
            'income_count': len(incomes)
        }
    }

    monthly_data = {}

    for invoice in invoices:
        month = invoice['month']
        if month not in monthly_data:
            monthly_data[month] = {'expenses': 0, 'income': 0, 'expense_count': 0, 'income_count': 0}
        monthly_data[month]['expenses'] += invoice['amount']
        monthly_data[month]['expense_count'] += 1

    for income in incomes:
        month = income['month']
        if month not in monthly_data:
            monthly_data[month] = {'expenses': 0, 'income': 0, 'expense_count': 0, 'income_count': 0}
        monthly_data[month]['income'] += income['amount']
        monthly_data[month]['income_count'] += 1

    for month, data in monthly_data.items():
        data['net_profit'] = data['income'] - data['expenses']
    
    financial_data['monthly'] = monthly_data

    with open(output_file, 'w') as f:
        json.dump(financial_data, f, indent=2)
    
    print(f"Processed {len(invoices)} invoices and {len(incomes)} income entries. Saved to {output_file}")
    return financial_data

def categorize_expense(description):
    """Categorize expense based on description"""
    description = description.lower()
    
    categories = {
        'utilities': ['electricity', 'internet', 'bill', 'utility'],
        'office': ['office', 'supplies', 'equipment', 'purchase'],
        'travel': ['travel', 'transportation'],
        'food': ['lunch', 'dinner', 'meal', 'restaurant'],
        'software': ['software', 'subscription', 'license'],
    }
    
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
            
    return 'other'

def categorize_income(description):
    """Categorize income based on description"""
    description = description.lower()
    
    categories = {
        'client_work': ['client', 'project', 'consulting'],
        'sales': ['sale', 'product', 'retail'],
        'services': ['service', 'support', 'maintenance'],
        'royalties': ['royalty', 'licensing'],
        'investments': ['dividend', 'interest', 'investment'],
    }
    
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
            
    return 'other'

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(script_dir, "data/financial_statements.txt")
    preprocess_financial_data(input_file)