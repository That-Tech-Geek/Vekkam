from app.core.models import Concept

class InMemoryKnowledgeGraph:
    def __init__(self): self.nodes={}; self.edges=[]
    def upsert_concept(self, concept: Concept) -> None: self.nodes[concept.concept_id]=concept
    def add_edge(self, source: str, relation: str, target: str) -> None: self.edges.append((source,relation,target))

class InMemoryVectorStore:
    def __init__(self): self.items=[]
    def upsert(self, document_id: str, text: str, metadata: dict[str,str]) -> None:
        self.items.append({"id":document_id,"text":text,"metadata":metadata})
    def search(self, query: str, limit: int=5) -> list[dict[str,object]]:
        terms=set(query.lower().split())
        ranked=sorted(self.items,key=lambda x:len(terms & set(str(x["text"]).lower().split())),reverse=True)
        return ranked[:limit]
