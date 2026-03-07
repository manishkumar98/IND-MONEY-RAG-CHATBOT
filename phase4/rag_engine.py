import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Add project root to sys.path to import from other phases/src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3.indexer import MFIndexer
from src.rag.prompts import SYSTEM_PROMPT

class RAGEngine:
    def __init__(self):
        load_dotenv()
        # Fallback to Streamlit secrets if not in environment
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GROQ_API_KEY")
            except ImportError:
                pass
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in .env or Streamlit Secrets.")
        self.client = Groq(api_key=api_key)
        self.indexer = MFIndexer()

    def generate_response(self, query):
        """Processes query in a single LLM call for maximum speed."""
        
        # 1. Query Expansion for Retrieval
        search_query = query
        if "bluechip" in query.lower():
            search_query += " SBI Large Cap Fund"
        if "long term equity" in query.lower():
            search_query += " SBI ELSS Tax Saver Fund"
            
        # 2. Retrieval (Perform this BEFORE the LLM call)
        retrieval_results = self.indexer.query(search_query, n_results=5)
        context = ""
        source_details = []
        for i, doc in enumerate(retrieval_results['documents'][0]):
            metadata = retrieval_results['metadatas'][0][i]
            source_url = metadata.get('source_url', '[Unknown Source]')
            scraped_date = metadata.get('scraped_at', 'Mar 2026')
            
            context += f"--- Snippet from {source_url} ---\n{doc}\n\n"
            source_details.append({'url': source_url, 'date': scraped_date})
        
        # 3. All-in-one Contextual Generation + Safety Check
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context from supported documentation:\n{context}\n\nClient Query: {query}"}
                ],
                model="llama-3.1-8b-instant",
                temperature=0,
            )
            
            raw_answer = chat_completion.choices[0].message.content.strip()
            
            # 4. Post-process (Safety Refusals usually don't need sources, but we'll check)
            is_refusal = any(refusal in raw_answer for refusal in ["I can only provide factual", "I cannot process personal"])
            return self.post_process_response(raw_answer, [] if is_refusal else source_details)
            
        except Exception as e:
            return f"I encountered an error processing your request: {e}"

    def post_process_response(self, answer, source_details):
        """Cleans response and appends HTML links for custom bubbles with date."""
        placeholders = ["[Source Link]", "Last updated from sources:", "Source:"]
        for p in placeholders:
            if p in answer:
                answer = answer.split(p)[0].strip()
        
        unique_sources = {}
        for s in source_details:
            url = s.get('url')
            date = s.get('date', 'Unknown')
            if url and url != "[Unknown Source]" and url not in unique_sources:
                unique_sources[url] = date
        
        if unique_sources:
            links_html = "".join([f"<li><a href='{url}' target='_blank' style='color: #00d09c;'>{url}</a> ({date})</li>" for url, date in unique_sources.items()])
            answer += f"<br><br><b>Last updated from sources:</b><ul>{links_html}</ul>"
        
        return answer

if __name__ == "__main__":
    engine = RAGEngine()
    print("-" * 30)
    print("TEST 1: Factual Retrieval (Single Call)")
    print(engine.generate_response("What is the exit load of SBI Flexicap Fund?"))
    print("-" * 30)
    print("\nTEST 2: Advisory Refusal (Single Call)")
    print(engine.generate_response("Should I invest in SBI Small Cap Fund for next 2 years?"))
    print("-" * 30)
    print("\nTEST 3: PII Refusal (Single Call)")
    print(engine.generate_response("My PAN number is ABCDE1234F, tell me about my holdings."))
    print("-" * 30)
