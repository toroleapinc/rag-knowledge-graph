# RAG with Knowledge Graphs

Retrieval-Augmented Generation pipeline that combines vector search with knowledge graph traversal for more accurate and contextual answers.

## How It Works

1. **Ingest**: Documents are chunked, embedded, and stored in a vector database. Entities and relationships are extracted and stored in a Neo4j knowledge graph.
2. **Retrieve**: For each query, we do both vector similarity search AND graph traversal from query entities, then merge results.
3. **Generate**: Retrieved context (text chunks + graph triples) is fed to an LLM to produce the answer.

The hybrid retrieval consistently outperforms pure vector search, especially for multi-hop questions where related entities aren't in the same document chunk.

## Setup

```bash
pip install -r requirements.txt
```

You'll need:
- Neo4j running locally or in Docker
- OpenAI API key (for embeddings and generation)
- ChromaDB or Qdrant for vector storage

```bash
docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5
export OPENAI_API_KEY=sk-...
export NEO4J_URI=bolt://localhost:7687
export NEO4J_PASSWORD=password
```

## Usage

```bash
# Ingest documents
python -m ragkg.ingest --source docs/ --chunk-size 512

# Query
python -m ragkg.query "What is the relationship between X and Y?"

# Or use the API
python -m ragkg.api --port 8000
```

## Project Layout

```
ragkg/          # Main package
├── ingest.py   # Document ingestion pipeline
├── graph/      # Neo4j graph operations
├── vectors/    # Vector store interface
├── retrieval/  # Hybrid retrieval
├── llm/        # LLM client
└── api.py      # FastAPI endpoint
tools/          # Go health checker
tests/
```
