import os
import openai
import tiktoken
from fastapi import FastAPI, Request
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Set up OpenAI and Supabase clients
openai.api_key = os.getenv("OPENAI_API_KEY")
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Initialize FastAPI app
app = FastAPI()

# Allow frontend (like Webflow or localhost) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tokenizer setup
encoding = tiktoken.get_encoding("cl100k_base")

# Pydantic model for request
class QueryRequest(BaseModel):
    question: str

# Utility: embed a text string
def embed(text: str):
    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Utility: format chunks into context string
def build_context(chunks):
    context = ""
    for chunk in chunks:
        context += chunk["chunk_text"].strip() + "\n---\n"
    return context.strip()

# Main RAG endpoint
@app.post("/ask")
async def ask_question(request: QueryRequest):
    question = request.question
    question_embedding = embed(question)

    # Perform similarity search
    response = supabase.rpc("match_chunks", {
        "query_embedding": question_embedding,
        "match_threshold": 0.75,
        "match_count": 5
    }).execute()

    if not response.data:
        return {"answer": "Sorry, I couldn't find any relevant information."}

    # Build GPT prompt from context
    context = build_context(response.data)

    prompt = f"""You are an economic insights assistant. Use the context below to answer the question.
If the context does not contain the answer, reply 'I don't know'.

Context:
{context}

Question: {question}
Answer:"""

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = completion.choices[0].message.content.strip()
    return {"answer": answer}
