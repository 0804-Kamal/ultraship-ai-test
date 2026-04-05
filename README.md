# 🚚 AI Document Assistant (RAG)

## 🔹 Overview
- AI-based system to analyze logistics documents (PDF)
- Uses RAG (Retrieval-Augmented Generation)
- Supports Q&A and structured data extraction

## 🔹 Features
- Upload PDF (Shipper / Carrier / BOL)
- Ask questions from document
- Extract key fields (shipment_id, rate, shipper, etc.)
- FastAPI backend + Streamlit UI

## 🔹 Tech Stack
- Python
- Streamlit
- FastAPI
- LangChain
- FAISS
- HuggingFace Transformers
- PyPDF

## 🔹 Project Files
- app.py → Streamlit UI
- main.py → FastAPI APIs
- rag.py → RAG logic
- extract.py → Data extraction
- requirements.txt → Dependencies

## 🔹 How to Run
- Install: `pip install -r requirements.txt`
- Run UI: `streamlit run app.py`
- Run API: `uvicorn main:app --reload`

## 🔹 Example Questions
- What is the shipment ID?
- Who is the shipper?

## 🔹 Output
- Returns answer + confidence
- Extracts structured JSON data

## 🔹 Future Improvements
- Better extraction accuracy
- Multi-document support
- Cloud deployment

## 👨‍💻 Author
Kamalesh K
