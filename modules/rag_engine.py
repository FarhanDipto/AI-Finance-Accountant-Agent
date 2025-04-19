import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pickle

class RAGEngine:
    def __init__(self, file_path=None, force_reload=False):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.model_cache_path = os.path.join(base_dir, "data/rag_cache.pkl")
        
        if file_path is None:
            file_path = os.path.join(base_dir, "data/financial_statements.txt")

        if not force_reload and os.path.exists(self.model_cache_path):
            with open(self.model_cache_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            self.invoices = cache_data.get('invoices', [])
            self.incomes = cache_data.get('incomes', [])
            self.chunks = cache_data['chunks']
            self.chunk_embeddings = cache_data['chunk_embeddings']

            self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            return

        self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        self.invoices, self.incomes, self.chunks = self._load_and_chunk_document(file_path)
        self.chunk_embeddings = self.embedding_model.encode(self.chunks)

        os.makedirs(os.path.dirname(self.model_cache_path), exist_ok=True)
        with open(self.model_cache_path, 'wb') as f:
            pickle.dump({
                'invoices': self.invoices,
                'incomes': self.incomes,
                'chunks': self.chunks,
                'chunk_embeddings': self.chunk_embeddings
            }, f)
    
    def _load_and_chunk_document(self, file_path):
        """Load document and split into chunks with more detailed processing"""
        with open(file_path, 'r') as file:
            text = file.read()

        documents = [line.strip() for line in text.split('\n') if line.strip()]

        invoices = []
        incomes = []
        
        for doc in documents:
            invoice_match = re.match(r'Invoice #(\d+) \| (.*?) \| (.*?) \| \$(\d+)', doc)
            income_match = re.match(r'Income #(\d+) \| (.*?) \| (.*?) \| \$(\d+)', doc)
            
            if invoice_match:
                invoice_id, date, description, amount = invoice_match.groups()
                invoices.append({
                    'raw': doc,
                    'id': invoice_id,
                    'date': date,
                    'description': description,
                    'amount': int(amount),
                    'type': 'expense'
                })
            elif income_match:
                income_id, date, description, amount = income_match.groups()
                incomes.append({
                    'raw': doc,
                    'id': income_id,
                    'date': date,
                    'description': description,
                    'amount': int(amount),
                    'type': 'income'
                })

        chunks = []

        for doc in documents:
            chunks.append(doc)

        self._add_expense_chunks(invoices, chunks)
        
        self._add_income_chunks(incomes, chunks)

        self._add_combined_summaries(invoices, incomes, chunks)
        
        return invoices, incomes, chunks
    
    def _add_expense_chunks(self, invoices, chunks):
        """Add invoice-specific chunks"""
        for doc in invoices:
            chunks.append(f"Invoice #{doc['id']} is for {doc['description']} costing ${doc['amount']}")
            chunks.append(f"{doc['description']} expense of ${doc['amount']} on {doc['date']}")

        if invoices:
            highest = max(invoices, key=lambda x: x['amount'])
            chunks.append(f"The highest invoice is #{highest['id']} for {highest['description']} at ${highest['amount']}")

            latest = max(invoices, key=lambda x: x['date'])
            chunks.append(f"The most recent invoice is #{latest['id']} for {latest['description']} on {latest['date']}")

            total = sum(doc['amount'] for doc in invoices)
            chunks.append(f"The total amount across all invoices is ${total}")
            chunks.append(f"Total expenses: ${total}")

            months = {}
            for doc in invoices:
                month = doc['date'].split()[0] 
                if month not in months:
                    months[month] = []
                months[month].append(doc)
            
            for month, docs in months.items():
                month_total = sum(doc['amount'] for doc in docs)
                chunks.append(f"In {month}, there were {len(docs)} invoices totaling ${month_total}")
                chunks.append(f"Expenses for {month}: ${month_total}")
    
    def _add_income_chunks(self, incomes, chunks):
        """Add income-specific chunks"""
        for doc in incomes:
            chunks.append(f"Income #{doc['id']} is from {doc['description']} earning ${doc['amount']}")
            chunks.append(f"{doc['description']} income of ${doc['amount']} on {doc['date']}")
        
        if incomes:
            highest = max(incomes, key=lambda x: x['amount'])
            chunks.append(f"The highest income is #{highest['id']} from {highest['description']} at ${highest['amount']}")
            
            latest = max(incomes, key=lambda x: x['date'])
            chunks.append(f"The most recent income is #{latest['id']} from {latest['description']} on {latest['date']}")
            
            total = sum(doc['amount'] for doc in incomes)
            chunks.append(f"The total amount across all income entries is ${total}")
            chunks.append(f"Total income: ${total}")
            
            months = {}
            for doc in incomes:
                month = doc['date'].split()[0]  
                if month not in months:
                    months[month] = []
                months[month].append(doc)
            
            for month, docs in months.items():
                month_total = sum(doc['amount'] for doc in docs)
                chunks.append(f"In {month}, there were {len(docs)} income entries totaling ${month_total}")
                chunks.append(f"Income for {month}: ${month_total}")
    
    def _add_combined_summaries(self, invoices, incomes, chunks):
        """Add combined financial summaries"""
        if invoices and incomes:
            total_expenses = sum(doc['amount'] for doc in invoices)
            total_income = sum(doc['amount'] for doc in incomes)
            net = total_income - total_expenses
            
            chunks.append(f"Total income: ${total_income}, Total expenses: ${total_expenses}")
            
            if net >= 0:
                chunks.append(f"Net profit: ${net}")
            else:
                chunks.append(f"Net loss: ${abs(net)}")
            
            months = set()
            for doc in invoices + incomes:
                month = doc['date'].split()[0]
                months.add(month)
            
            for month in months:
                month_expenses = sum(doc['amount'] for doc in invoices if doc['date'].split()[0] == month)
                month_income = sum(doc['amount'] for doc in incomes if doc['date'].split()[0] == month)
                month_net = month_income - month_expenses
                
                chunks.append(f"In {month}, income: ${month_income}, expenses: ${month_expenses}")
                
                if month_net >= 0:
                    chunks.append(f"{month} net profit: ${month_net}")
                else:
                    chunks.append(f"{month} net loss: ${abs(month_net)}")
    
    def retrieve(self, query, top_k=3):
        """Retrieve relevant chunks for the query"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        similarities = cosine_similarity([query_embedding], self.chunk_embeddings)[0]

        top_indices = np.argsort(similarities)[-top_k:][::-1]

        top_chunks = [self.chunks[i] for i in top_indices]
        top_scores = [similarities[i] for i in top_indices]
        
        return top_chunks, top_scores
    
    def format_answer(self, query, contexts):
        """Format an answer based on retrieved contexts"""
        query_lower = query.lower()
        
        is_income_query = any(word in query_lower for word in ["income", "revenue", "earnings", "profit", "earned"])
        is_expense_query = any(word in query_lower for word in ["expense", "invoice", "cost", "spent", "purchase"])
        is_net_query = any(word in query_lower for word in ["net", "profit and loss", "balance", "bottom line"])
        
        if is_income_query and not is_expense_query:
            if "highest" in query_lower or "largest" in query_lower:
                for context in contexts:
                    if "highest income" in context.lower():
                        return context

                if self.incomes:
                    highest = max(self.incomes, key=lambda x: x['amount'])
                    return f"The highest income is #{highest['id']} from {highest['description']} at ${highest['amount']}."
            
            elif "latest" in query_lower or "recent" in query_lower:
                for context in contexts:
                    if "most recent income" in context.lower():
                        return context

                if self.incomes:
                    latest = max(self.incomes, key=lambda x: x['date'])
                    return f"The most recent income is #{latest['id']} from {latest['description']} on {latest['date']}."
            
            elif "total" in query_lower:
                for context in contexts:
                    if "total income" in context.lower():
                        return context

                total = sum(doc['amount'] for doc in self.incomes)
                return f"Total income: ${total}."

            for month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]:
                if month in query_lower:
                    month_cap = month.capitalize()
                    month_docs = [doc for doc in self.incomes if month_cap in doc.get('date', '')]
                    if month_docs:
                        total = sum(doc['amount'] for doc in month_docs)
                        return f"In {month_cap}, there were {len(month_docs)} income entries totaling ${total}."

        elif is_expense_query and not is_income_query:
            if "highest" in query_lower or "largest" in query_lower:
                for context in contexts:
                    if "highest invoice" in context.lower():
                        return context
                
                if self.invoices:
                    highest = max(self.invoices, key=lambda x: x['amount'])
                    return f"The highest invoice is #{highest['id']} for {highest['description']} at ${highest['amount']}."
            
            elif "latest" in query_lower or "recent" in query_lower:
                for context in contexts:
                    if "most recent invoice" in context.lower():
                        return context

                if self.invoices:
                    latest = max(self.invoices, key=lambda x: x['date'])
                    return f"The most recent invoice is #{latest['id']} for {latest['description']} on {latest['date']}."
            
            elif "total" in query_lower:
                for context in contexts:
                    if "total expenses" in context.lower() or "total amount across all invoices" in context.lower():
                        return context

                total = sum(doc['amount'] for doc in self.invoices)
                return f"Total expenses: ${total}."

            for month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]:
                if month in query_lower:
                    month_cap = month.capitalize()
                    month_docs = [doc for doc in self.invoices if month_cap in doc.get('date', '')]
                    if month_docs:
                        total = sum(doc['amount'] for doc in month_docs)
                        return f"In {month_cap}, there were {len(month_docs)} invoices totaling ${total}."

        elif is_net_query or ("total" in query_lower and not is_income_query and not is_expense_query):
            for context in contexts:
                if "net profit" in context.lower() or "net loss" in context.lower():
                    return context

            total_income = sum(doc['amount'] for doc in self.incomes)
            total_expenses = sum(doc['amount'] for doc in self.invoices)
            net = total_income - total_expenses
            
            if net >= 0:
                return f"Net profit: ${net} (Income: ${total_income}, Expenses: ${total_expenses})"
            else:
                return f"Net loss: ${abs(net)} (Income: ${total_income}, Expenses: ${total_expenses})"

        if ("invoice" in query_lower or "income" in query_lower) and "#" in query_lower:
            id_match = re.search(r'#(\d+)', query_lower)
            if id_match:
                id_num = id_match.group(1)
                
                if "invoice" in query_lower:
                    for doc in self.invoices:
                        if doc.get('id') == id_num:
                            return f"Invoice #{id_num} is for {doc['description']} for ${doc['amount']} on {doc['date']}."
                
                elif "income" in query_lower:
                    for doc in self.incomes:
                        if doc.get('id') == id_num:
                            return f"Income #{id_num} is from {doc['description']} for ${doc['amount']} on {doc['date']}."

        if contexts and len(contexts) > 0:
            return contexts[0]
        
        return "I couldn't find relevant information about that in your financial records."

    def get_answer(self, query):
        """Main method to get answer for a query"""
        try:
            top_chunks, top_scores = self.retrieve(query, top_k=5)  

            filtered_chunks = [chunk for chunk, score in zip(top_chunks, top_scores) if score > 0.2]
            
            if not filtered_chunks:
                return "I couldn't find relevant financial information for your query."

            answer = self.format_answer(query, filtered_chunks)
            
            return answer
            
        except Exception as e:
            return f"I encountered an issue processing your financial query: {str(e)}. Please try again."


_rag_engine = None

def initialize_rag():
    """Initialize the RAG engine if not already initialized"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine

def get_rag_answer(query: str):
    """Get answer from RAG engine, initializing if necessary"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine.get_answer(query)