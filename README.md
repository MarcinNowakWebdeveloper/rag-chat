# 🤖📚 RAG Chat + Personality Engine

A local AI system combining:
- LLM chat (Ollama)
- Retrieval-Augmented Generation (RAG) on Docker docs
- Personality-based response styles

---

## 🚀 Features

- 🔍 Automatically detects whether a question matches the knowledge base
- 📚 Answers strictly based on indexed data (files + websites)
- 🚫 Rejects questions outside of the dataset domain
- 💬 General chat fallback
- 🎭 Multiple response styles:
    - Default 
    - Formal (official tone)
    - Fairy tale style
    - Pessimistic tone
    - Optimistic tone

---

## 🧠 Architecture

User → Router → RAG Validation → (Retrieve / Reject) → Personality Layer → Response

                ┌────────────────┐
                │   USER INPUT   │
                └──────┬─────────┘
                       ↓
                ┌────────────────┐
                │     ROUTER     │
                │ Docker? YES/NO │
                └──────┬─────────┘
          ┌────────────┴────────────┐
          ↓                         ↓
    ┌────────────────┐       ┌────────────────┐
    │   CHAT LLM     │       │   RAG SYSTEM   │
    │    (Ollama)    │       │   (Chroma DB)  │
    └──────┬─────────┘       └──────┬─────────┘
           ↓                        ↓
           └──────────┬─────────────┘
                      ↓
             ┌────────────────┐
             │    PERSONA     │
             │ (style prompt) │
             └────────┬───────┘
                      ↓
             ┌────────────────┐
             │    RESPONSE    │
             └────────────────┘



## 🛠️ Tech Stack

- LangChain
- Ollama (local LLM)
- ChromaDB (vector database)
- Streamlit (UI)
- Async ingestion pipeline (files + web sources)

---

## 📦 Modules

💼 [CV](README/CV.md)

## ⚙️ Setup

1. Install requirements

```pip install -r requirements.txt```

```ollama pull llama3:8b``` - or any other model you want to use

```ollama pull phi3:mini``` - or any other model you want to use for classification

2. Build knowledge base (RAG ingestion)

Load data from files and web sources:

```python -m backend.imports.import```

   Reset database before importing:

```python -m backend.imports.import --reset```

Note: ingestion process (files + web crawling) runs asynchronously

3. Run frontend

```streamlit run frontend/app.py```

## 📚 How RAG works

The system:

1. Loads data from:
   * local files
   * web pages (crawler)
2. Splits content into chunks 
3. Generates embeddings 
4. Stores them in ChromaDB 
5. At query time:
   * retrieves top-k relevant chunks 
   * sends them to the LLM 
8. If no relevant match is found → the question is rejected

## 🌐 Web Crawler

* Fully asynchronous ingestion
* Configurable depth and page limits
* Domain filtering support


## 🎭 Personality system

Every response is modified using a style layer:

* Formal → bureaucratic style
* Fairy tale → storytelling mode
* Pessimistic → dark philosophical tone
* Optimistic → positive framing

## ⚙️ Environment Variables (.env)

### 🧠 AI Models
* OLLAMA_MODEL – main LLM model (default: llama3:8b)
* EMBEDDING_MODEL – embedding model (default: nomic-embed-text)

### 🗄️ Vector Database
* VECTOR_DB – vector DB type (e.g. chroma)
* VECTOR_DB_PATH – path to local database storage

### 🔎 RAG Configuration
* RAG_K – number of retrieved chunks (top-k)
* RAG_SIMILARITY_THRESHOLD – minimum similarity score required for retrieval
* RAG_BATCH_SIZE - batch size for embedding and saving in the database

### ✂️ Default Chunking Settings
* CHUNK_SIZE – size of text chunks
* CHUNK_OVERLAP – overlap between chunks

### 🚫 Topic Filtering
* MIN_ALLOWED_TOPIC_SCORE – minimum confidence that a query belongs to the dataset domain

### 📂 Data Sources
* DATA_PATH – directory containing input files for indexing

### 🌍 Web Crawler Configuration
* WEB_CRAWLER_MAX_DEPTH – maximum crawl depth
* WEB_CRAWLER_MAX_PAGES – maximum number of pages to fetch
* WEB_CRAWLER_DOMAIN – optional domain restriction
* WEB_CRAWLER_SOURCE – JSON list of starting URLs e.g. ```["https://docs.docker.com/manuals/"]```
* WEB_CRAWLER_WORKERS_COUNT - number of concurrent worker tasks used during crawling; each worker independently consumes URLs from the queue and processes pages in parallel, controlling the overall crawl concurrency and speed

## 🧪 Tests

### 📊 Database inspection test
Shows dataset size and sample records:

```python -m backend.tests.test_db```

### 🤖 RAG functional test
Direct query test (Docker-related):

```python -m backend.tests.test_rag```

## 📜 License

MIT