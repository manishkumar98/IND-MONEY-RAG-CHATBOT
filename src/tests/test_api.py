import requests
import json
import unittest
import time
import subprocess
import os

class TestPhase5API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the FastAPI server in the background
        cls.server_process = subprocess.Popen(
            ["python3", "src/api/api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        )
        # Wait for server to start
        time.sleep(10)

    def test_health_endpoint(self):
        """Test the /health endpoint."""
        response = requests.get("http://localhost:8000/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["engine_ready"])

    def test_ask_endpoint(self):
        """Test the /ask endpoint with a factual query."""
        payload = {"query": "What is the exit load of SBI Small Cap Fund?"}
        response = requests.post("http://localhost:8000/ask", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertIn("1%", data["answer"])

    def test_pii_refusal_via_api(self):
        """Test if the API handles PII refusal correctly through the RAG engine."""
        payload = {"query": "My phone number is 9999999999, tell me details."}
        response = requests.post("http://localhost:8000/ask", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cannot process", data["answer"].lower())

    @classmethod
    def tearDownClass(cls):
        # Terminate the server process
        cls.server_process.terminate()

if __name__ == "__main__":
    unittest.main()
