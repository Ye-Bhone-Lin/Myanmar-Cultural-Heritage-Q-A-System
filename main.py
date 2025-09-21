from fastapi import FastAPI, Form
from pydantic import BaseModel
import os 

from knowledge_base.vector_db import query_index
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
groq_api_key = os.getenv("GROQ_API_KEY")


class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(data: Question):
    client = Groq(api_key=groq_api_key)

    top_docs = query_index(data.query)
    context = "\n".join(top_docs)
    prompt = f"Answer the question based on context:\n\nContext:\n{context}\n\nQuestion:\n{data.query}\nAnswer:"
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
        {
            "role": "user",
            "content": prompt
        },
        ]
    )
    answer = response.choices[0].message.content
    
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "Welcome to Myanmar Cultural Heritage Q&A System"}
