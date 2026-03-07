import unittest
import os
import shutil
from indexer import MFIndexer

class TestPhase3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We use a temp DB for testing
        cls.test_db_path = "phase3/data/test_chroma_db"
        if os.path.exists(cls.test_db_path):
            shutil.rmtree(cls.test_db_path)
        
        cls.indexer = MFIndexer(processed_dir="phase2/data/processed", db_path=cls.test_db_path)
        cls.indexer.index_data()

    def test_collection_exists(self):
        """Verify that the collection was created and has documents."""
        count = self.indexer.collection.count()
        self.assertGreater(count, 0, "Collection should not be empty")

    def test_semantic_retrieval(self):
        """Test if query for 'lock-in' returns ELSS/Locking related content in top 3."""
        results = self.indexer.query("3-year lock-in period", n_results=3)
        all_content = " ".join(results['documents'][0]).lower()
        self.assertTrue("lock" in all_content or "elss" in all_content or "tax" in all_content, 
                        f"Query for lock-in should return relevant content. Found: {all_content[:200]}")

    def test_metadata_persistence(self):
        """Ensure specific metadata keys are preserved."""
        results = self.indexer.query("SBI Small Cap", n_results=1)
        metadata = results['metadatas'][0][0]
        self.assertIn("fund_name", metadata)
        self.assertIn("source_url", metadata)
        self.assertTrue(metadata["source_url"].startswith("http"))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            shutil.rmtree(cls.test_db_path)

if __name__ == "__main__":
    unittest.main()
