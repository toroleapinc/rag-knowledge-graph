"""Neo4j graph client."""
import os
from neo4j import GraphDatabase

class GraphClient:
    def __init__(self, uri=None, password=None):
        self.uri = uri or os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
        self.password = password or os.environ.get('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(self.uri, auth=('neo4j', self.password))

    def add_entity(self, name, entity_type, properties=None):
        with self.driver.session() as session:
            props = properties or {}
            session.run(
                f"MERGE (e:{entity_type} {{name: $name}}) SET e += $props",
                name=name, props=props
            )

    def add_relationship(self, source, target, rel_type, properties=None):
        with self.driver.session() as session:
            session.run(
                "MATCH (a {name: $src}), (b {name: $tgt}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += $props",
                src=source, tgt=target, props=properties or {}
            )

    def get_neighbors(self, entity_name, max_hops=2):
        """Get entities within max_hops of the given entity."""
        with self.driver.session() as session:
            result = session.run(
                f"MATCH path = (start {{name: $name}})-[*1..{max_hops}]-(end) "
                "RETURN DISTINCT end.name AS name, labels(end) AS types, length(path) AS distance",
                name=entity_name
            )
            return [dict(r) for r in result]

    def get_triples(self, entity_name, max_hops=1):
        """Get (subject, predicate, object) triples around an entity."""
        with self.driver.session() as session:
            result = session.run(
                f"MATCH (a {{name: $name}})-[r]-(b) RETURN a.name AS subject, type(r) AS predicate, b.name AS object",
                name=entity_name
            )
            return [dict(r) for r in result]

    def close(self):
        self.driver.close()
