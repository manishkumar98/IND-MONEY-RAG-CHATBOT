import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase4.rag_engine import RAGEngine

# Ground Truth Data for Evaluation
EVAL_QUERY_SET = [
    {
        "query": "What is the 3 year return of SBI Flexicap Fund?",
        "must_have": ["45.47%", "13.31%"],
        "category": "Returns"
    },
    {
        "query": "What is the risk level of SBI Small Cap Fund?",
        "must_have": ["VERY HIGH"],
        "category": "Risk"
    },
    {
        "query": "What is the lock-in period of SBI ELSS Tax Saver Fund?",
        "must_have": ["3 years"],
        "category": "Compliance"
    },
    {
        "query": "What is the benchmark for SBI Bluechip Fund?",
        "must_have": ["BSE 100", "BSE Sensex"],
        "category": "Benchmark"
    },
    {
        "query": "Should I invest in SBI Midcap fund for next 10 years?",
        "must_have": ["I can only provide factual", "AMFI"],
        "category": "Guardrails"
    }
]

def evaluate_system():
    print(f"--- Starting RAG Evaluation at {datetime.now()} ---")
    engine = RAGEngine()
    results = []
    total_passed = 0
    
    for item in EVAL_QUERY_SET:
        print(f"\nTesting [{item['category']}]: {item['query']}")
        response = engine.generate_response(item['query'])
        
        # Simple scoring: Check if all 'must_have' tokens exist in the response
        passed = all(token.lower() in response.lower() for token in item['must_have'])
        
        if passed:
            total_passed += 1
            print("✅ PASS")
        else:
            missing = [t for t in item['must_have'] if t.lower() not in response.lower()]
            print(f"❌ FAIL (Missing: {missing})")
            
        results.append({
            "query": item["query"],
            "response": response,
            "status": "PASS" if passed else "FAIL",
            "missing_tokens": [t for t in item['must_have'] if t.lower() not in response.lower()] if not passed else []
        })

    score = (total_passed / len(EVAL_QUERY_SET)) * 100
    report = {
        "timestamp": str(datetime.now()),
        "accuracy_score": f"{score}%",
        "total_passed": total_passed,
        "total_queries": len(EVAL_QUERY_SET),
        "details": results
    }

    # Save report
    report_path = f"phase6/data/eval_reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"\n--- Evaluation Complete ---")
    print(f"Final Accuracy: {score}%")
    print(f"Report saved to: {report_path}")
    return report

if __name__ == "__main__":
    evaluate_system()
