from fastapi import FastAPI, UploadFile, File
import shutil

from rag import load_document, split_docs, create_db, ask_question
from extract import extract_data

app = FastAPI()

db = None
docs = None


# Upload API
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global db, docs

    with open("temp.pdf", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_document("temp.pdf")
    chunks = split_docs(docs)
    db = create_db(chunks)

    return {"message": "File uploaded and processed successfully"}


# Ask API
@app.post("/ask")
async def ask(query: str):
    global db

    if db is None:
        return {"error": "Upload document first"}

    answer, source, confidence = ask_question(db, query)

    return {
        "answer": answer,
        "confidence": confidence
    }


# Extract API
@app.get("/extract")
async def extract():
    global docs

    if docs is None:
        return {"error": "Upload document first"}

    full_text = " ".join([doc.page_content for doc in docs])
    data = extract_data(full_text)

    return data
