import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

    def create_embeddings(self, chunks):
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(texts)

        embeddings = np.array(embeddings).astype("float32")

        return embeddings

    def build_index(self, chunks):
        embeddings = self.create_embeddings(chunks)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        self.documents = chunks

        print("FAISS index created successfully!")
        print("Number of vectors:", self.index.ntotal)

    def search(self, query, top_k=3):
        query_embedding = self.model.encode([query])

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for index in indices[0]:
            if index < len(self.documents):
                results.append(self.documents[index])

        return results