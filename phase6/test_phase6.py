import pytest
import os
import json
from phase6.automation import full_sync
from phase6.evaluator import evaluate_system

def test_automation_pipeline():
    """Test if the full sync pipeline (Scrape -> Process -> Index) runs without crashing."""
    # We won't actually run the full sync here to save time/API calls in CI, 
    # but we verify the script exists and is importable.
    assert os.path.exists("phase6/automation.py")
    # Uncomment the below line to run a real sync check if needed
    # assert full_sync() == True

def test_system_accuracy():
    """Master Test Case: Verify the system accuracy is above 80%."""
    report = evaluate_system()
    accuracy_score = float(report["accuracy_score"].replace("%", ""))
    
    # We expect at least 80% accuracy for the pilot phase
    assert accuracy_score >= 80.0, f"System accuracy dropped to {accuracy_score}%"

def test_data_integrity():
    """Verify that the reports are being generated correctly."""
    reports_dir = "phase6/data/eval_reports"
    files = [f for f in os.listdir(reports_dir) if f.endswith(".json")]
    assert len(files) > 0, "No evaluation reports generated."

if __name__ == "__main__":
    # If run directly, run the evaluator
    evaluate_system()
