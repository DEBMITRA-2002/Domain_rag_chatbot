from document_loader import extract_text_from_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# PDF path
pdf_path = "documents/sample_rag_document.pdf"


# Step 1: Extract PDF text
documents = extract_text_from_pdf(pdf_path)


# Step 2: Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)


# Step 3: Create chunks
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


# Step 4: Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# Step 5: Create embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(texts)


# Step 6: Display results
print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])