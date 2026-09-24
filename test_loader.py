from document_loader import extract_text_from_pdf


pdf_path = pdf_path = "documents/sample_rag_document.pdf"

documents = extract_text_from_pdf(pdf_path)

print(f"Total pages extracted: {len(documents)}")

for document in documents:
    print("\n-------------------------")
    print("Source:", document["source"])
    print("Page:", document["page"])
    print("Text:")
    print(document["text"][:500])