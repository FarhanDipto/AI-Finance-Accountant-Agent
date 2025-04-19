import re

def parse_intent(text):
    text = text.lower().strip()
    
    if any(phrase in text for phrase in ["balance", "how much do i have", "net worth", "profit and loss", "bottom line"]):
        return {"intent": "query_financial_docs", "query": "what is my financial balance"}

    elif any(word in text for word in ["expense", "spent", "cost", "payment", "bill", "invoice"]):
        if any(word in text for word in ["highest", "largest", "biggest", "most expensive"]):
            return {"intent": "query_financial_docs", "query": "what is the highest expense"}

        elif any(word in text for word in ["latest", "recent", "newest", "last"]):
            return {"intent": "query_financial_docs", "query": "what is the most recent expense"}

        months = ["january", "february", "march", "april", "may", "june", 
                 "july", "august", "september", "october", "november", "december"]
                 
        for month in months:
            if month in text:
                return {"intent": "query_financial_docs", "query": f"expenses in {month}"}

        return {"intent": "query_financial_docs", "query": "total expenses"}

    elif any(word in text for word in ["income", "earn", "revenue", "payment received", "earnings", "money in"]):
        if any(word in text for word in ["highest", "largest", "biggest", "most"]):
            return {"intent": "query_financial_docs", "query": "what is the highest income"}
            
        elif any(word in text for word in ["latest", "recent", "newest", "last"]):
            return {"intent": "query_financial_docs", "query": "what is the most recent income"}
            
        months = ["january", "february", "march", "april", "may", "june", 
                 "july", "august", "september", "october", "november", "december"]
                 
        for month in months:
            if month in text:
                return {"intent": "query_financial_docs", "query": f"income in {month}"}
                
        return {"intent": "query_financial_docs", "query": "total income"}
    
    elif any(word in text for word in ["profit", "loss", "net", "bottom line"]):
        months = ["january", "february", "march", "april", "may", "june", 
                 "july", "august", "september", "october", "november", "december"]
                 
        for month in months:
            if month in text:
                return {"intent": "query_financial_docs", "query": f"net profit for {month}"}
                
        return {"intent": "query_financial_docs", "query": "what is the net profit"}
    
    elif re.search(r'invoice.*(#|number)\s*(\d{3}|\d{1,3})', text) or re.search(r'voice.*(#|number)\s*(\d{3}|\d{1,3})', text):
        invoice_match = re.search(r'(\d{3}|\d{1,3})', text)
        if invoice_match:
            invoice_number = invoice_match.group(1).zfill(3)  
            return {"intent": "query_financial_docs", "query": f"invoice #{invoice_number}"}
    
    elif re.search(r'income.*(#|number)\s*(\d{3}|\d{1,3})', text):
        income_match = re.search(r'(\d{3}|\d{1,3})', text)
        if income_match:
            income_number = income_match.group(1).zfill(3)
            return {"intent": "query_financial_docs", "query": f"income #{income_number}"}
    
    elif any(month in text for month in ["january", "february", "march", "april", "may", "june", 
                                        "july", "august", "september", "october", "november", "december"]):
        for month in ["january", "february", "march", "april", "may", "june", 
                    "july", "august", "september", "october", "november", "december"]:
            if month in text:
                return {"intent": "query_financial_docs", "query": f"financial summary for {month}"}

    elif any(word in text for word in ["how much", "total", "what did", "give me", "show me", "summary"]):
        return {"intent": "query_financial_docs", "query": text}
    
    elif any(word in text for word in ["stop", "exit", "quit", "goodbye"]):
        return {"intent": "exit"}

    else:
        return {"intent": "query_financial_docs", "query": text}