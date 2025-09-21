import os
from tqdm import tqdm

DATA_DIR = "data"
CHUNK_DIR = "chunks"
os.makedirs(CHUNK_DIR, exist_ok=True)
CHUNK_SIZE = 500  # tokens

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def preprocess():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                text = f.read()
            chunks = chunk_text(text)
            for idx, chunk in enumerate(chunks):
                chunk_file = f"{filename.replace('.txt','')}_chunk_{idx}.txt"
                with open(os.path.join(CHUNK_DIR, chunk_file), "w", encoding="utf-8") as f:
                    f.write(chunk)
    print("Preprocessing complete!")

if __name__ == "__main__":
    preprocess()
