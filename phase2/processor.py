import os
import json
import re

class DataProcessor:
    def __init__(self, raw_dir="phase1/data/raw", processed_dir="phase2/data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        os.makedirs(self.processed_dir, exist_ok=True)

    def clean_text(self, text):
        """Remove common navigation and footer noise."""
        # Remove navigation blocks (approximate)
        noise_patterns = [
            r"Join Us.*?Login",
            r"Learn to Invest.*?Quick Invest",
            r"About us.*?Follow us on:",
            r"Terms & Conditions.*?Privacy Policy",
            r"Mutual Fund Investments are subject to market risks.*",
            r"A\+ A- A",
            r"Light\s*Dark",
            r"About us\s*.*", # Force removal of anything starting with About us at the end
            r"Join Us\s*.*"  # Force removal of anything starting with Join Us at the start
        ]
        
        cleaned = text
        for pattern in noise_patterns:
            cleaned = re.sub(pattern, "\n\n", cleaned, flags=re.DOTALL)
            
        # Remove lines that are just navigation links
        lines = cleaned.split("\n")
        filtered_lines = [l.strip() for l in lines if len(l.strip()) > 10 or ":" in l or "₹" in l]
        return "\n".join(filtered_lines)

    def chunk_text(self, text, chunk_size=1500, overlap=200):
        """Simple chunking by character length with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
            if start >= len(text):
                break
        return chunks

    def process_files(self):
        if not os.path.exists(self.raw_dir):
            print(f"Error: {self.raw_dir} does not exist.")
            return

        processed_count = 0
        for filename in os.listdir(self.raw_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.raw_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    raw_content = f.read()

                # Extract metadata from header
                url_match = re.search(r"Source URL: (.*)", raw_content)
                source_url = url_match.group(1) if url_match else "Unknown"
                
                date_match = re.search(r"Scraped Date: (.*)", raw_content)
                scraped_at = date_match.group(1) if date_match else "Unknown"
                
                # Split cleaning and body
                body = raw_content.split("-" * 50)[-1]
                cleaned_body = self.clean_text(body)
                
                # Chunking
                chunks = self.chunk_text(cleaned_body)
                
                fund_name = filename.replace(".txt", "").replace("_", " ").title()
                
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        "chunk_id": f"{fund_name}_{i}",
                        "fund_name": fund_name,
                        "source_url": source_url,
                        "scraped_at": scraped_at,
                        "content": chunk.strip(),
                        "metadata": {
                            "index": i,
                            "length": len(chunk)
                        }
                    }
                    
                    output_name = f"{filename.replace('.txt', '')}_chunk_{i}.json"
                    with open(os.path.join(self.processed_dir, output_name), "w", encoding="utf-8") as out:
                        json.dump(chunk_data, out, indent=4)
                
                processed_count += 1
                print(f"Processed: {filename} -> {len(chunks)} chunks")
        
        print(f"\nPhase 2 Complete: {processed_count} files processed.")

if __name__ == "__main__":
    processor = DataProcessor()
    processor.process_files()
