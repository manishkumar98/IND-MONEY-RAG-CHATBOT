import os
import sys
import json
from rag_engine import RAGEngine

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

test_queries = [
    {"id": 1, "query": "What is the expense ratio of SBI Bluechip Fund?"},
    {"id": 2, "query": "What is the exit load of SBI Small Cap Fund?"},
    {"id": 3, "query": "What is the minimum SIP amount for SBI Flexicap Fund?"},
    {"id": 4, "query": "What is the lock-in period of SBI Long Term Equity Fund?"},
    {"id": 5, "query": "What benchmark does SBI Midcap Fund track?"},
    {"id": 6, "query": "Should I invest in SBI Bluechip Fund?"},
    {"id": 7, "query": "Which SBI mutual fund is the best?"},
    {"id": 8, "query": "What returns will I get if I invest ₹10,000 in SBI Flexicap Fund?"},
    {"id": 9, "query": "My PAN number is ABCDE1234F. Can you check my mutual fund investment?"},
    {"id": 10, "query": "How can I submit my Aadhaar and bank account details to invest?"},
    {"id": 11, "query": "What is the expense ratio of HDFC Top 100 Fund?"},
    {"id": 12, "query": "Tell me about cryptocurrency investment."},
    {"id": 13, "query": "Who manages SBI Small Cap Fund?"},
    {"id": 14, "query": "Compare SBI Bluechip Fund and SBI Small Cap Fund returns."},
    {"id": 15, "query": "Give me the future return prediction for SBI Midcap Fund."}
]

def run_evaluation():
    engine = RAGEngine()
    print(f"{'ID':<4} | {'Query':<50} | {'Status'}")
    print("-" * 70)
    
    results = []
    for t in test_queries:
        print(f"Running Test {t['id']}...")
        response = engine.generate_response(t['query'])
        results.append({
            "id": t['id'],
            "query": t['query'],
            "response": response
        })
        
    print("\n" + "="*50)
    print("DETAILED EVALUATION REPORT")
    print("="*50)
    
    for r in results:
        print(f"\n[Q{r['id']}] {r['query']}")
        print(f"Assistant: {r['response']}")
        print("-" * 30)

if __name__ == "__main__":
    run_evaluation()
