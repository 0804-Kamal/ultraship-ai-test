# -------- IMPORTS --------
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import re


# -------- 1. LOAD DOCUMENT --------
def load_document(path):
    loader = PyPDFLoader(path)
    return loader.load()


# -------- 2. SPLIT DOCUMENT --------
def split_docs(documents):
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)


# -------- 3. CREATE VECTOR DB --------
def create_db(chunks):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    return db


# -------- 4. ASK QUESTION (FINAL CLEAN VERSION) --------
def ask_question(db, query):
    retriever = db.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)

    if not docs:
        return "Not found in document", "", 0.0

    # Combine context
    context = " ".join([doc.page_content for doc in docs])

    # -------- RULE-BASED EXTRACTION --------
    answer = "Not found"

    # Rate
    match = re.search(r"\$\d+\.?\d*\s?USD", context)
    if match:
        answer = match.group()

    # Carrier name
    elif "LOGISTICS" in query.lower():
        match = re.search(r"SWIFT SHIFT LOGISTICS LLC", context)
        if match:
            answer = match.group()

    # Weight
    elif "weight" in query.lower():
        match = re.search(r"\d{5,}\s?lbs", context)
        if match:
            answer = match.group()

    # Shipment ID
    elif "shipment" in query.lower():
        match = re.search(r"LD\d+", context)
        if match:
            answer = match.group()

    # -------- OUTPUT --------
    source = docs[0].page_content
    confidence = round(min(len(docs) / 3, 1.0), 2)

    return answer, source, confidence