import unittest
import os
import json
from processor import DataProcessor

class TestPhase2(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor(raw_dir="phase1/data/raw", processed_dir="phase2/data/test_processed")
        self.test_text = """
        Join Us Header Login
        Some useful data about SBI Fund.
        Benchmark: Nifty 50.
        Exit Load: 1%.
        About us Footer
        """

    def test_cleaning_logic(self):
        """Verify that navigation and footer noise are removed."""
        cleaned = self.processor.clean_text(self.test_text)
        self.assertNotIn("Join Us", cleaned)
        self.assertNotIn("About us", cleaned)
        self.assertIn("SBI Fund", cleaned)
        self.assertIn("Benchmark", cleaned)

    def test_chunking_logic(self):
        """Ensure chunking generates multiple parts if text is long."""
        long_text = "Detailed mutual fund information. " * 100
        chunks = self.processor.chunk_text(long_text, chunk_size=500, overlap=50)
        self.assertGreater(len(chunks), 1)
        # Check overlap (roughly)
        self.assertTrue(any(chunks[0][-20:] in chunks[1] for chunk in chunks))

    def test_output_structure(self):
        """Check if processed JSON contains required keys."""
        # Run process on one dummy file if needed, or just test the logic
        dummy_content = "Source URL: https://test.com\n" + "-"*50 + "\nFund Data Info here."
        os.makedirs("phase1/data/test_raw", exist_ok=True)
        with open("phase1/data/test_raw/test_fund.txt", "w") as f:
            f.write(dummy_content)
        
        test_processor = DataProcessor(raw_dir="phase1/data/test_raw", processed_dir="phase2/data/test_processed")
        test_processor.process_files()
        
        output_files = os.listdir("phase2/data/test_processed")
        self.assertGreater(len(output_files), 0)
        
        with open(os.path.join("phase2/data/test_processed", output_files[0]), "r") as f:
            data = json.load(f)
            self.assertIn("fund_name", data)
            self.assertIn("content", data)
            self.assertIn("source_url", data)
            self.assertEqual(data["source_url"], "https://test.com")

if __name__ == "__main__":
    unittest.main()
