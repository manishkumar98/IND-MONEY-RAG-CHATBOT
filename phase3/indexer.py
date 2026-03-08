import os
import json
import chromadb
from chromadb.utils import embedding_functions

class MFIndexer:
    def __init__(self, processed_dir="phase2/data/processed", db_path="phase3/data/chroma_db"):
        self.processed_dir = processed_dir
        self.db_path = db_path
        # Using a local, high-quality embedding function
        # Use HuggingFace Free Inference API (Zero disk space for Vercel, Zero cost)
        hf_token = os.environ.get("HUGGINGFACE_TOKEN") # Optional but recommended for higher limits
        self.embed_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name="sbi_mf_collection",
            embedding_function=self.embed_fn
        )

    def load_chunks(self):
        documents = []
        metadatas = []
        ids = []
        
        if not os.path.exists(self.processed_dir):
            print(f"Error: {self.processed_dir} not found.")
            return [], [], []

        for filename in os.listdir(self.processed_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.processed_dir, filename), "r") as f:
                    data = json.load(f)
                    documents.append(data["content"])
                    metadatas.append({
                        "fund_name": data["fund_name"],
                        "source_url": data["source_url"],
                        "scraped_at": data.get("scraped_at", "Unknown"),
                        "chunk_index": data["metadata"]["index"]
                    })
                    ids.append(data["chunk_id"])
        
        return documents, metadatas, ids

    def index_data(self):
        print("Loading chunks from processed data...")
        docs, metas, ids = self.load_chunks()
        
        if not docs:
            print("No data found to index.")
            return

        print(f"Indexing {len(docs)} chunks into ChromaDB at {self.db_path}...")
        
        # Batching to avoid potential overhead
        batch_size = 50
        for i in range(0, len(docs), batch_size):
            self.collection.add(
                documents=docs[i:i+batch_size],
                metadatas=metas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        
        print(f"Successfully indexed {len(docs)} chunks.")

    def query(self, text, n_results=3):
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    indexer = MFIndexer()
    indexer.index_data()
    
    # Quick test
    print("\nTest Query: 'What is the expense ratio of SBI Large Cap Fund?'")
    res = indexer.query("What is the expense ratio of SBI Large Cap Fund?")
    for doc, meta in zip(res['documents'][0], res['metadatas'][0]):
        print(f"\nSource: {meta['source_url']}\nContent Preview: {doc[:200]}...")
