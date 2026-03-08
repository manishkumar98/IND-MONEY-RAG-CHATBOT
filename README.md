# SBI Mutual Fund RAG Assistant

A facts-only retrieval-augmented generation (RAG) assistant for SBI Mutual Fund schemes, designed to simulate a knowledge tool for the **INDmoney** platform.

> [!IMPORTANT]
> This project is for demo purposes only and does not constitute financial advice.

---

## 🏗️ Architecture & Scope
The system uses a **multi-phase RAG pipeline** to provide accurate, source-backed answers to retail investor queries.

- **AMC Focus:** SBI Mutual Fund
- **Key Schemes Covered:**
  - SBI Large Cap Fund (formerly SBI Bluechip)
  - SBI Flexicap Fund
  - SBI ELSS Tax Saver Fund (formerly SBI Long Term Equity)
  - SBI Small Cap Fund
  - SBI Midcap Fund (formerly SBI Magnum Midcap)
- **Features:** 
  - Expense Ratio & Exit Load retrieval
  - Riskometer level & Benchmark details
  - Minimum SIP & Lumpsum investment thresholds
  - Automatic source attribution with "Last updated" timestamps
  - PII (Personal Identifiable Information) protection

---

## 🛠️ Setup & Local Deployment

### 1. Prerequisites
- Python 3.12+ 
- [Groq API Key](https://console.groq.com/) (for LLM generation)
- [HuggingFace Token](https://huggingface.co/settings/tokens) (for free embeddings)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/manishkumar98/IND-MONEY-RAG-CHATBOT.git
cd IND-MONEY-RAG-CHATBOT

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```text
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_TOKEN=your_hf_token_here
```

### 4. Running the Assistant
#### Option A: FastAPI Backend
```bash
python src/api/api.py
```
#### Option B: Streamlit Host (Mock Frontend)
```bash
streamlit run backend_host.py
```

---

## 🚀 Deployment (Vercel Core)
The project is optimized for **zero-cost deployment** on Vercel:
1. **Frontend:** Static HTML/JS in `/frontend` folder.
2. **Backend:** FastAPI serverless functions in `/src/api`.
3. **Embeddings:** Uses **HuggingFace Inference API** to keep serverless storage under the 500MB limit.

---

## ⚠️ Known Limits & Guardrails
- **Scope:** Only answers questions specific to SBI Mutual Funds based on the scraped dataset.
- **Accuracy:** Performance depends on the presence of data in the `phase3/data/chroma_db` folder. 
- **Advisory Refusal:** Explicitly refuses queries asking for "Best fund," "Should I invest," or predicted returns.
- **Privacy:** Automatically flags and refuses to process PAN numbers, Aadhaar, or Bank ID details.

---

## 📂 Documentation
- [Source List](docs/sources.md) - Representative list of 15-25 URLs used.
- [Sample Q&A](docs/sample_qa.md) - Example queries and their source-backed answers.
- [Disclaimer](docs/disclaimer.md) - Full text of the advisory refusal snippet.
