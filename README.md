# Alberta Perspectives – RAG Chatbot MVP

This project is a Retrieval-Augmented Generation (RAG) prototype designed for AlbertaPerspectives.ca. It allows users to ask natural language questions about economic reports and receive AI-generated answers based on context retrieved from stored documents.

The project was built using a modular, phase-based approach with AI-assisted development, and is deployed fully online via Render (backend) and Vercel (frontend).

---

## Features

- PDF-to-vector pipeline for economic documents
- Supabase database with vector search (`vector(1536)`)
- FastAPI backend for semantic search + LLM integration
- Chat interface built with Next.js, TailwindCSS, and Shadcn/UI
- Fully deployed frontend/backend
- User can query and receive responses with context from reports

---

## 📁 Tech Stack

| Layer          | Tech                         |
|----------------|------------------------------|
| Frontend       | Next.js, TailwindCSS, Shadcn |
| Backend        | FastAPI, OpenAI              |
| Database       | Supabase (PostgreSQL + vectors) |
| Embeddings     | `text-embedding-ada-002`     |
| Deployment     | Vercel (frontend), Render (backend) |

---

## 🏗️ System Architecture

```
User → Vercel (Frontend) → Render (FastAPI) → Supabase (DB) + OpenAI → Answer
```

- PDF files are processed and split into chunks
- Each chunk is embedded and stored in Supabase
- User queries are embedded and matched against stored chunks
- Relevant context is passed to OpenAI for answer generation
- Response is returned to the user via chat UI

---

## Setup Instructions (Local Development)

### 1. Clone the Backend

```bash
git clone https://github.com/your-username/Olu-tech-interview-genai-engineer.git
cd Olu-tech-interview-genai-engineer
```
I renamed the original repo which was tech-interview-genai-engineer.git

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up `.env` file

Create a `.env` file based on `.env.template`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_public_key
SUPABASE_SECRET=your_service_role_key
OPENAI_API_KEY=your_openai_key
```

### 4. Process documents

```bash
python process_documents.py
```

### 5. Start backend API

```bash
uvicorn rag_api:app --reload
```

---

### 6. Clone the Frontend

```bash
git clone https://github.com/your-username/chat-ui.git
cd chat-ui
```

### 7. Install dependencies

```bash
npm install
```

### 8. Run the frontend

```bash
npm run dev
```

Edit `pages/index.tsx` to point to your Render backend URL:

```ts
fetch("https://your-backend.onrender.com/ask", { ... })
```

---

## ✅ Deployment URLs

- **Frontend (Vercel)**: [Chat Frontend](https://chat-ui-gules-gamma.vercel.app/)
- **Backend (Render)**: [Backend](https://alberta11.onrender.com)
- **API Docs (Swagger)**: [https://alberta11.onrender.com/docs](https://alberta11.onrender.com/docs)

---

## 📦 Project Structure

```
Olu-tech-interview-genai-engineer/
├── rag_api.py            # FastAPI backend
├── process_documents.py  # PDF chunking + embedding
├── requirements.txt
├── .env.template
└── README.md

chat-ui/
├── pages/
│   └── index.tsx         # Chat interface
├── components/
├── public/
└── tailwind.config.js
```

---

##Credits

Oluwasegun Oyeniyi built this project as part of a GenAI Engineer technical challenge. Development was supported by AI tools for code generation, planning, and deployment guidance. Every implementation step was reviewed, adapted, and validated manually.

---

## Notes

- Supabase RLS was disabled to allow unrestricted insert access during MVP development
- Platform-specific packages (`pywin32`, `WMI`) were removed for deployment compatibility
- This is an MVP focused on core functionality, not all optional features (like image extraction or memory) were implemented
