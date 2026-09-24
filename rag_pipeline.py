import os

from dotenv import load_dotenv
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document_loader import extract_text_from_pdf
from vector_store import VectorStore
from prompt import SYSTEM_PROMPT


# Load environment variables
load_dotenv()


class RAGPipeline:

    def __init__(self):

        # -----------------------------
        # Load Groq API Key
        # -----------------------------

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file"
            )

        # -----------------------------
        # Initialize Groq Client
        # -----------------------------

        self.client = Groq(
            api_key=api_key
        )

        # -----------------------------
        # Groq Model
        # -----------------------------

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

        # -----------------------------
        # Text Splitter
        # -----------------------------

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120
        )

        # -----------------------------
        # Initialize FAISS Vector Store
        # -----------------------------

        self.vector_store = VectorStore()

        # -----------------------------
        # Store Chunks
        # -----------------------------

        self.chunks = []


    # =========================================================
    # SINGLE PDF
    # =========================================================

    def load_pdf(self, pdf_file):

        """
        Process a single PDF file.

        Steps:
        PDF
        ↓
        Text Extraction
        ↓
        Chunking
        ↓
        Embeddings
        ↓
        FAISS Index
        """

        # Extract text from PDF
        documents = extract_text_from_pdf(
            pdf_file
        )

        chunks = []

        # Split every page into chunks
        for document in documents:

            split_texts = self.text_splitter.split_text(
                document["text"]
            )

            for text in split_texts:

                chunks.append(
                    {
                        "text": text,
                        "source": document["source"],
                        "page": document["page"],
                    }
                )

        # Store chunks
        self.chunks = chunks

        # Build FAISS index
        self.vector_store.build_index(
            chunks
        )

        return chunks


    # =========================================================
    # MULTIPLE PDFs
    # =========================================================

    def load_pdfs(self, pdf_files):

        """
        Process multiple PDF files.

        All PDFs are combined into one FAISS vector index.
        """

        all_chunks = []

        # Process every uploaded PDF
        for pdf_file in pdf_files:

            # Extract text
            documents = extract_text_from_pdf(
                pdf_file
            )

            # Process every page
            for document in documents:

                # Split page text into chunks
                split_texts = self.text_splitter.split_text(
                    document["text"]
                )

                # Store each chunk
                for text in split_texts:

                    all_chunks.append(
                        {
                            "text": text,
                            "source": document["source"],
                            "page": document["page"],
                        }
                    )

        # Store all chunks
        self.chunks = all_chunks

        # Build one FAISS index
        # containing chunks from all PDFs
        self.vector_store.build_index(
            all_chunks
        )

        return all_chunks


    # =========================================================
    # QUESTION ANSWERING
    # =========================================================

    def ask_question(
        self,
        question,
        top_k=3
    ):

        """
        Ask a question using retrieved document context.
        """

        # -----------------------------
        # Retrieve relevant chunks
        # -----------------------------

        results = self.vector_store.search(
            question,
            top_k=top_k
        )

        # -----------------------------
        # No results
        # -----------------------------

        if not results:

            return (
                "I could not find this information "
                "in the uploaded documents.",
                []
            )

        # -----------------------------
        # Build Context
        # -----------------------------

        context_parts = []

        for result in results:

            context_parts.append(
                f"Source: {result['source']}\n"
                f"Page: {result['page']}\n"
                f"Content: {result['text']}"
            )

        context = "\n\n".join(
            context_parts
        )

        # -----------------------------
        # Create User Prompt
        # -----------------------------

        user_prompt = f"""
Context from uploaded documents:

{context}

User Question:
{question}

Answer the question using ONLY the context above.

If the answer is not present in the context, say:

"I could not find this information in the uploaded documents."

Mention the relevant source document and page number.
"""

        # -----------------------------
        # Send Request to Groq
        # -----------------------------

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            # Low temperature helps
            # keep answers grounded
            temperature=0
        )

        # -----------------------------
        # Get Answer
        # -----------------------------

        answer = response.choices[0].message.content

        # -----------------------------
        # Return Answer + Sources
        # -----------------------------

        return answer, results