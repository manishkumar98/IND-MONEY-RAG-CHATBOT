import os
import sys
import time
import subprocess
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_step(step_name, command):
    print(f"\n>>>> Executing {step_name}...")
    start_time = time.time()
    try:
        # Run command and capture output
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        duration = time.time() - start_time
        print(f"✅ {step_name} completed in {duration:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {step_name} FAILED!")
        print(f"Error Output: {e.stderr}")
        return False

def full_sync():
    """Weekly/Automatic sync of data and index."""
    print(f"--- Full RAG System Sync Started at {datetime.now()} ---")
    
    steps = [
        ("Phase 1: Scraping", "python3 phase1/scraper.py"),
        ("Phase 2: Processing", "python3 phase2/processor.py"),
        ("Phase 3: Indexing", "python3 phase3/indexer.py")
    ]
    
    success_count = 0
    for name, cmd in steps:
        if run_step(name, cmd):
            success_count += 1
        else:
            print("🛑 Stopping sync due to error.")
            break
    
    if success_count == len(steps):
        print("\n✨ FULL SYNC SUCCESSFUL!")
        return True
    return False

if __name__ == "__main__":
    full_sync()
