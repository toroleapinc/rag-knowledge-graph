"""Document ingestion: chunk, embed, extract entities, build graph."""
import argparse
import os
import glob
import logging
from tqdm import tqdm
from .vectors.store import VectorStore
from .graph.client import GraphClient
from .graph.extractor import EntityExtractor

logger = logging.getLogger(__name__)

def chunk_text(text, chunk_size=512, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks

def ingest_documents(source_dir, chunk_size=512):
    """Ingest documents from a directory."""
    vector_store = VectorStore()
    graph = GraphClient()
    extractor = EntityExtractor()

    files = glob.glob(os.path.join(source_dir, '**/*.txt'), recursive=True) + \
            glob.glob(os.path.join(source_dir, '**/*.md'), recursive=True)
    
    logger.info(f"Found {len(files)} documents")
    doc_id = 0

    for fpath in tqdm(files, desc="Ingesting"):
        with open(fpath) as f:
            text = f.read()

        chunks = chunk_text(text, chunk_size)
        ids = [f"doc_{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": fpath, "chunk_idx": i} for i in range(len(chunks))]
        
        vector_store.add(chunks, ids=ids, metadatas=metadatas)
        
        # extract entities from first few chunks (expensive)
        for chunk in chunks[:3]:
            extracted = extractor.extract(chunk)
            for entity in extracted.get('entities', []):
                graph.add_entity(entity['name'], entity.get('type', 'Entity'))
            for rel in extracted.get('relationships', []):
                graph.add_relationship(rel['source'], rel['target'], rel.get('type', 'RELATED_TO'))
        
        doc_id += 1

    logger.info(f"Ingested {doc_id} documents, {vector_store.count()} chunks")
    graph.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--chunk-size', type=int, default=512)
    args = parser.parse_args()
    ingest_documents(args.source, args.chunk_size)
