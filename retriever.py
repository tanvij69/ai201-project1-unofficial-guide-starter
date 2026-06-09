import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean_text, chunk_text

def embed_and_store():
    # Load and chunk documents
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["source"])
        all_chunks.extend(chunks)

    # Set up embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it exists to avoid duplicates
    try:
        client.delete_collection("dining_guides")
    except:
        pass
    
    collection = client.create_collection("dining_guides")

    # Embed and store chunks
    texts = [chunk["text"] for chunk in all_chunks]
    ids = [chunk["chunk_id"] for chunk in all_chunks]
    metadatas = [{"source": chunk["source"]} for chunk in all_chunks]
    
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"Stored {len(all_chunks)} chunks in ChromaDB.")
    return collection, model

def retrieve(query, collection, model, top_k=5):
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    collection, model = embed_and_store()
    
    test_queries = [
        "What do students say about wait times at D2 during lunch?",
        "Which dining plan do students recommend for first years?",
        "What vegetarian options are available at Owens?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        results = retrieve(query, collection, model)
        for r in results:
            print(f"Source: {r['source']}")
            print(f"Distance: {r['distance']:.4f}")
            print(f"Text: {r['text'][:200]}")
            print()