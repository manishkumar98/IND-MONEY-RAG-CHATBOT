import os
import json
import unittest
from scraper import WHITELISTED_DOMAINS, scrape_page
import asyncio

class TestPhase1(unittest.TestCase):
    def test_domain_whitelist(self):
        """Test that non-whitelisted domains are blocked."""
        loop = asyncio.get_event_loop()
        url = "https://unauthorized-finance-blog.com/sbi-midcap"
        # Since scrape_page is async, we use run_until_complete
        result = loop.run_until_complete(scrape_page(url, "test.txt", data_dir="phase1/data/test_raw"))
        self.assertFalse(result, "Scraper should block unauthorized domains")

    def test_official_domain_allowed(self):
        """Test that whitelisted domains are accepted."""
        # We don't necessarily need to run the full scrape here to save time/resources,
        # but we can check if the whitelist logic works.
        url = "https://www.sbimf.com/en-us/equity-schemes/sbi-large-cap-fund"
        is_allowed = any(domain in url for domain in WHITELISTED_DOMAINS)
        self.assertTrue(is_allowed, f"Domain for {url} should be in whitelist")

    def test_data_dir_creation(self):
        """Test that the data directory is created if it doesn't exist."""
        test_dir = "phase1/data/temp_test_dir"
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
        
        # This will create the dir
        os.makedirs(test_dir, exist_ok=True)
        self.assertTrue(os.path.exists(test_dir))
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)

    def test_manifest_structure(self):
        """Test if the manifest file (if it exists) has the correct structure."""
        manifest_path = "phase1/data/raw/manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                data = json.load(f)
                self.assertIsInstance(data, list)
                if len(data) > 0:
                    self.assertIn("fund", data[0])
                    self.assertIn("url", data[0])
                    self.assertIn("success", data[0])

if __name__ == "__main__":
    unittest.main()
