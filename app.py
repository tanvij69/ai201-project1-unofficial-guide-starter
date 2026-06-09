import gradio as gr
from retriever import embed_and_store, retrieve
from generator import query_rag

print("Loading embeddings...")
collection, model = embed_and_store()

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    answer, sources = query_rag(question, collection, model)
    sources_text = "\n".join(f"• {s}" for s in sources)
    return answer, sources_text

with gr.Blocks() as demo:
    gr.Markdown("# 🦃 VT Dining Unofficial Guide")
    gr.Markdown("Ask anything about Virginia Tech campus dining based on real student reviews.")
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()