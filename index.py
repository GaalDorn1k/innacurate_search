import faiss
import numpy as np
from embeddings import HFEmbeddings


class FaissIdx:
    def __init__(self, model: HFEmbeddings, dim=384) -> None:
        self.index = faiss.IndexFlatIP(dim)
        self.doc_map = dict()
        self.model = model
        self.ctr = 0

    def add_doc(self, document_text: str) -> None:
        self.index.add(np.array(self.model.get_embeddings(document_text.lower())))
        self.doc_map[self.ctr] = document_text
        self.ctr += 1

    def search_doc(self, query: str, k=1) -> dict:
        score, text = self.index.search(np.array(self.model.get_embeddings(query)), k)
        return {'text': self.doc_map[text[0][0]] if text[0][0] != -1 else '',
                'score': score[0][0]}
