"""Query interface."""
import argparse
import logging
from .vectors.store import VectorStore
from .graph.client import GraphClient
from .graph.extractor import EntityExtractor
from .retrieval.hybrid import HybridRetriever
from .llm.client import LLMClient

logger = logging.getLogger(__name__)

def query(question, use_graph=True):
    vector_store = VectorStore()
    graph = GraphClient()
    retriever = HybridRetriever(vector_store, graph)
    llm = LLMClient()
    
    # extract entities from query
    entities = []
    if use_graph:
        extractor = EntityExtractor()
        extracted = extractor.extract(question)
        entities = [e['name'] for e in extracted.get('entities', [])]
        logger.info(f"Query entities: {entities}")
    
    # retrieve
    context = retriever.retrieve(question, entities=entities)
    logger.info(f"Retrieved {len(context['text_chunks'])} chunks, {len(context['graph_triples'])} triples")
    
    # generate
    answer = llm.generate(question, context['combined'])
    return answer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('question')
    parser.add_argument('--no-graph', action='store_true')
    args = parser.parse_args()
    print(query(args.question, use_graph=not args.no_graph))
