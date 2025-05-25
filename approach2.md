## Approach & Implementation

To build this RAG system prototype, I took an iterative, phase-based approach. While I authored and validated all decisions, I used AI tools extensively — particularly for code generation, error handling, Supabase schema guidance, and clarifying framework usage. These tools helped me accelerate development within the time constraints, and I made sure to thoroughly understand and validate every component before integrating it into the system.

---

## 1. Phase-Based Planning with AI Assistance

From the beginning, I worked with AI to break the problem into structured phases. This included:

1. File Processing & Text Extraction  
2. Embedding Generation  
3. Supabase Schema Setup & Integration  
4. Backend (FastAPI) Development  
5. Frontend (Next.js) Development  
6. Deployment to Render & Vercel  

Each phase was treated as a separate milestone. I completed one phase with AI-assisted code generation and debugging, tested it thoroughly, and only then proceeded to the next.

---

## 2. Document Processing

Although the challenge instructions referred to PowerPoint files, I discovered that the provided files were PDFs. AI tools helped me refactor the original `.pptx` parsing logic into a robust PDF extraction pipeline using `PyMuPDF`. The result was clean page-by-page text chunks ready for embedding.

---

## 3. Embedding & Supabase Integration

Using OpenAI’s `text-embedding-ada-002`, I generated embeddings for each chunk of text using python genrated by openAI. I then worked with Supabase to store the data efficiently. With AI assistance, I created two tables:

- `document`: to store metadata about each file  
- `chunks`: to store individual text chunks and their vector embeddings  

I encountered challenges with permissions during insertion, which were resolved by disabling Row-Level Security (RLS) on the `document` and `chunks` tables. Additionally, the embedding field was explicitly set as `vector(1536)` to align with the OpenAI model's output.

The `.env.template` file was updated and renamed to `.env`, where I manually added my Supabase credentials and OpenAI API key.

---

## 4. Backend Development (FastAPI)

AI tools helped scaffold the FastAPI backend, which performs:

- Embedding of the user query  
- Similarity search in Supabase  
- Context selection and prompt construction  
- Answer generation via OpenAI’s chat model  

While the AI proposed much of the structure, I customized error handling, Supabase queries, and improved prompt formatting. I tested this backend locally until it was stable and functional.

---

## 5. Deployment to Render

After validating the backend locally, I deployed it to Render. During this process, I faced platform-specific compatibility issues, primarily due to `pywin32` and `WMI`, which are Windows-only. I removed these dependencies with AI guidance, and the backend deployed successfully to:

`https://alberta11.onrender.com`

---

## 6. Frontend Development & Vercel Deployment

For the UI, I used Next.js with TailwindCSS and Shadcn/UI. I kept the interface minimal and focused on usability, supporting:

- Freeform user input  
- Suggested question buttons  
- Context-aware AI responses  

After building locally, I updated the frontend to use the Render backend URL and deployed it on Vercel. This made the project fully cloud-based, requiring no local setup to use or test.

---

## Key Trade-Offs & Design Decisions

| Decision | Justification |
|----------|----------------|
| Switched to PDF parsing | Matched the actual file format; simplified processing |
| Disabled Supabase RLS | Enabled backend inserts without complex auth |
| Manual schema edits | Ensured compatibility with OpenAI embeddings |
| AI-assisted development | Accelerated progress while maintaining code ownership |
| Phase-based development | Allowed for targeted debugging and iteration |

---

## Summary

While I used AI for assistance throughout the development process — from code generation to Supabase modeling and deployment troubleshooting — every decision and implementation was verified, customized, and tested manually. This project was built in clear phases, each validated before progressing to the next, to ensure overall system stability.

The final system delivers a functional MVP that demonstrates:

- PDF document processing  
- Vector storage and retrieval via Supabase  
- A complete RAG pipeline powered by OpenAI  
- A working frontend chat interface  
- Cloud deployment across Render (backend) and Vercel (frontend)  
