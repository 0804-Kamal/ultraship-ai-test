from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import re


# -------------------------------
# Load PDF
# -------------------------------
def load_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


# -------------------------------
# Split into chunks
# -------------------------------
def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    return chunks


# -------------------------------
# Create Vector DB
# -------------------------------
def create_db(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_documents(chunks, embeddings)
    return db


# -------------------------------
# Ask Question (FINAL VERSION)
# -------------------------------
def ask_question(db, query):

    docs = db.similarity_search(query, k=5)

    # Combine and clean context
    context = " ".join([doc.page_content for doc in docs])
    context = re.sub(r'\s+', ' ', context)

    query_lower = query.lower()

    # -------------------------------
    # RATE
    # -------------------------------
    if "rate" in query_lower or "amount" in query_lower:
        match = re.search(r"\$\s?\d+\.\d+", context)
        if match:
            return match.group().replace(" ", ""), "context", 0.95

    # -------------------------------
    # SHIPMENT ID
    # -------------------------------
    if "shipment" in query_lower or "id" in query_lower:
        match = re.search(r"LD\d+", context)
        if match:
            return match.group(), "context", 0.95

    # -------------------------------
    # WEIGHT
    # -------------------------------
    if "weight" in query_lower:
        match = re.search(r"\d+\.?\d*\s?lbs", context, re.IGNORECASE)
        if match:
            return match.group(), "context", 0.90

    # -------------------------------
    # DATE
    # -------------------------------
    if "date" in query_lower:
        match = re.search(r"\d{2}-\d{2}-\d{4}", context)
        if match:
            return match.group(), "context", 0.85

    # -------------------------------
    # DELIVERY LOCATION (FIXED)
    # -------------------------------
    if "delivery location" in query_lower or "drop" in query_lower:
        match = re.search(r"Drop.*?([A-Za-z]+,\s?[A-Z]{2}\s?\d{5})", context)
        if match:
            return match.group(1), "context", 0.90

    # -------------------------------
    # PICKUP LOCATION (BONUS)
    # -------------------------------
    if "pickup location" in query_lower:
        match = re.search(r"Pickup.*?([A-Za-z]+,\s?[A-Z]{2})", context)
        if match:
            return match.group(1), "context", 0.90

    # -------------------------------
    # FALLBACK (SAFE SHORT)
    # -------------------------------
    return "Answer not found in document", "context", 0.5
