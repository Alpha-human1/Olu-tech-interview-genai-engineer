import os
import fitz  # PyMuPDF
from supabase import create_client, Client
import openai
from dotenv import load_dotenv
import uuid
import tiktoken

# Load environment variables
load_dotenv()

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

# Tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

def num_tokens(text):
    return len(encoding.encode(text))

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def chunk_text(text, max_tokens=500):
    words = text.split()
    chunks, chunk = [], []

    for word in words:
        chunk.append(word)
        if num_tokens(" ".join(chunk)) > max_tokens:
            chunks.append(" ".join(chunk))
            chunk = []

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

# ✅ FIXED: Embedding function for OpenAI v1.x
def generate_embedding(text):
    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def save_document_and_chunks(title, chunks):
    result = supabase.table("document").insert({
        "title": title
    }).execute()

    if not result.data:
        print("❌ Failed to insert document.")
        return

    doc_id = result.data[0]['id']

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        supabase.table("chunks").insert({
            "document_id": doc_id,
            "chunk_text": chunk,
            "embedding": embedding
        }).execute()

    print(f"✅ Uploaded '{title}' with {len(chunks)} chunks.")

if __name__ == "__main__":
    folder = "samples"

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            print(f"\n📄 Processing: {file}")
            text = extract_text_from_pdf(path)
            chunks = chunk_text(text)
            save_document_and_chunks(file, chunks)
