from document_loader import extract_text_from_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter


# PDF path
pdf_path = "documents/sample_rag_document.pdf"

# Extract text
documents = extract_text_from_pdf(pdf_path)

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

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


print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print("\n==============================")
    print("Chunk:", i)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:")
    print(chunk["text"])