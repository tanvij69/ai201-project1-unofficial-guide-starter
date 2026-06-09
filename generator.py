import os
from groq import Groq
from dotenv import load_dotenv
from retriever import embed_and_store, retrieve

load_dotenv()

def query_rag(question, collection, model):
    # Retrieve relevant chunks
    chunks = retrieve(question, collection, model)
    
    # Build context string with sources
    context = ""
    sources = []
    for chunk in chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])
    
    # Build prompt
    prompt = f"""You are a helpful guide for Virginia Tech students answering questions about campus dining.
Use ONLY the context below to answer the question. Do not use outside knowledge.
If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer (cite your sources by filename at the end):"""

    # Call Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    return answer, sources

if __name__ == "__main__":
    print("Loading embeddings...")
    collection, model = embed_and_store()
    
    questions = [
        "What do students say about wait times at D2 during lunch?",
        "Which dining plan do students recommend for first years?",
        "What vegetarian options are available at Owens?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        answer, sources = query_rag(question, collection, model)
        print(answer)
        print(f"\nSources: {', '.join(sources)}")
        print("=" * 50)