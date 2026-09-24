from rag_pipeline import RAGPipeline


pdf_path = "documents/sample_rag_document.pdf"


print("Initializing RAG pipeline...")

rag = RAGPipeline()


print("Loading PDF...")

chunks = rag.load_pdf(pdf_path)

print(f"PDF loaded successfully!")
print(f"Total chunks: {len(chunks)}")


question = "What is Machine Learning?"

print("\nQuestion:")
print(question)


answer, sources = rag.ask_question(question, top_k=2)


print("\n==============================")
print("ANSWER")
print("==============================")

print(answer)


print("\n==============================")
print("SOURCES")
print("==============================")

for source in sources:
    print(
        f"- {source['source']} | Page {source['page']}"
    )