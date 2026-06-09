import os

def load_documents(docs_folder="docs"):
    documents = []
    for filename in os.listdir(docs_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({"source": filename, "text": text})
    return documents

def clean_text(text):
    import re
    text = re.sub(r'<[^>]+>', '', text)        # remove HTML tags
    text = re.sub(r'&amp;|&nbsp;|&lt;|&gt;', '', text)  # remove HTML entities
    text = re.sub(r'\n{3,}', '\n\n', text)     # collapse extra blank lines
    text = text.strip()
    return text

def chunk_text(text, source, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_id": f"{source}_{chunk_id}"
            })
            chunk_id += 1
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["source"])
        all_chunks.extend(chunks)
    
    print(f"Total chunks: {len(all_chunks)}")
    print("\n--- 5 Sample Chunks ---")
    for chunk in all_chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"ID: {chunk['chunk_id']}")
        print(f"Text: {chunk['text']}")
        print("-" * 40)