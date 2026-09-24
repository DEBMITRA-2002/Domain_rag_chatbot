from document_loader import extract_text_from_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_store import VectorStore


# PDF path
pdf_path = "documents/sample_rag_document.pdf"


# Extract PDF text
documents = extract_text_from_pdf(pdf_path)


# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)


# Create chunks
chunks = []

for document in documents:
    split_texts = text_splitter.split_text(document["text"])

    for text in split_texts:
        chunks.append(
            {
                "text": text,
                "source": document["source"],
                "page": document["page"],
            }
        )


# Create vector store
vector_store = VectorStore()


# Build FAISS index
vector_store.build_index(chunks)


# Test search
query = "What is Machine Learning?"

results = vector_store.search(query, top_k=2)


print("\nSearch Results:")

for result in results:
    print("\n-------------------------")
    print("Source:", result["source"])
    print("Page:", result["page"])
    print("Text:")
    print(result["text"])