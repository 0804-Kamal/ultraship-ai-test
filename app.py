import streamlit as st
from rag import load_document, split_docs, create_db, ask_question
from extract import extract_data

# 👇 PASTE FROM HERE
st.title("🚚 AI Document Assistant")

file = st.file_uploader("Upload PDF", type=["pdf"])

if file:
    st.success("✅ File uploaded")

    with open("temp.pdf", "wb") as f:
        f.write(file.read())

    docs = load_document("temp.pdf")
    st.session_state["docs"] = docs

    chunks = split_docs(docs)
    db = create_db(chunks)

    st.success("📄 Document processed")

    query = st.text_input("Ask a question")

    if query:
        if st.button("Ask"):
            answer, source, confidence = ask_question(db, query)

            st.write("### ✅ Answer:")
            st.write(answer)

            st.write("### 📄 Source:")
            st.write(source)

            st.write("### 📊 Confidence:")
            st.write(confidence)

# 👇 EXTRACTION BUTTON
if "docs" in st.session_state:
    if st.button("Extract Structured Data"):
        full_text = " ".join([doc.page_content for doc in st.session_state["docs"]])
        extracted = extract_data(full_text)

        st.write("### 📦 Extracted Data:")
        st.json(extracted)