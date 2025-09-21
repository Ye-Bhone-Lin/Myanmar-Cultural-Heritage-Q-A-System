import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
import pickle


model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Returns an embedding vector for the given text.
    Drop-in replacement for OpenAI Embedding API.
    """
    embedding = model.encode(text).tolist()
    return embedding

CHUNK_DIR = "/Users/yebhonelin/Documents/github/Myanmar-Cultural-Heritage-Q-A-System/ingestion/chunks"
INDEX_FILE = "vector.index"
DOCS_FILE = "documents.pkl"
VECTOR_DIM = 1536  

index = None
documents = []

def build_index():
    global documents, index

    documents = []
    first_embedding = None

    for filename in os.listdir(CHUNK_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(CHUNK_DIR, filename), "r", encoding="utf-8") as f:
                text = f.read()
            embedding = np.array(get_embedding(text), dtype=np.float32)

            if first_embedding is None:
                dim = embedding.shape[0]
                index = faiss.IndexFlatL2(dim)
                first_embedding = True

            index.add(np.array([embedding]))
            documents.append(text)

    faiss.write_index(index, INDEX_FILE)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(documents, f)

    print(f"Vector index built with {len(documents)} documents!")


def load_index():
    global index, documents
    if os.path.exists(INDEX_FILE) and os.path.exists(DOCS_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(DOCS_FILE, "rb") as f:
            documents = pickle.load(f)
    else:
        raise RuntimeError("Index not built yet. Run build_index() first.")

def query_index(query, k=5):
    global index, documents
    if index is None or not documents:
        load_index()

    embedding = np.array(get_embedding(query), dtype=np.float32)
    D, I = index.search(np.array([embedding]), k)

    # Avoid IndexError by checking bounds
    results = [documents[i] for i in I[0] if i < len(documents)]
    return results

if __name__ == "__main__":
    build_index()

