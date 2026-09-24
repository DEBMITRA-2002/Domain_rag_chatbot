from pypdf import PdfReader
import os


def extract_text_from_pdf(pdf_file):
    """
    Extract text from every page of a PDF file.

    Returns:
        list: A list of dictionaries containing:
              - text
              - source
              - page
    """

    # If a file path is provided
    if isinstance(pdf_file, str):
        source_name = os.path.basename(pdf_file)
        reader = PdfReader(pdf_file)
    else:
        source_name = pdf_file.name
        reader = PdfReader(pdf_file)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        # Skip empty pages
        if not text or not text.strip():
            continue

        documents.append(
            {
                "text": text.strip(),
                "source": source_name,
                "page": page_number,
            }
        )

    return documents