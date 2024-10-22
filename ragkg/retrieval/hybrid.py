"""Hybrid retrieval: vector search + graph traversal."""
import logging

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, vector_store, graph_client, vector_weight=0.6):
        self.vectors = vector_store
        self.graph = graph_client
        self.vector_weight = vector_weight

    def retrieve(self, query, entities=None, n_results=5, max_hops=2):
        """Retrieve relevant context using both vector search and graph."""
        # vector search
        vector_results = self.vectors.search(query, n_results=n_results)
        vector_docs = vector_results['documents'][0] if vector_results['documents'] else []
        
        # graph traversal
        graph_context = []
        if entities:
            for entity in entities:
                triples = self.graph.get_triples(entity, max_hops=max_hops)
                for t in triples:
                    graph_context.append(f"{t['subject']} -> {t['predicate']} -> {t['object']}")
                neighbors = self.graph.get_neighbors(entity, max_hops=max_hops)
                logger.info(f"Found {len(neighbors)} neighbors for {entity}")

        return {
            'text_chunks': vector_docs,
            'graph_triples': graph_context,
            'combined': vector_docs + [f"[Graph] {t}" for t in graph_context],
        }
