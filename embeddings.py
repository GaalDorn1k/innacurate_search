import torch
import numpy as np
import torch.nn.functional as F
from langchain_community.embeddings import HuggingFaceEmbeddings


class HFEmbeddings:
    def __init__(self,
                 model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

    def get_embeddings(self, text: str) -> np.ndarray:
        emb = self.embeddings.embed_query(text)
        emb = torch.Tensor([emb])
        emb = F.normalize(emb, p=2, dim=1)
        return emb.detach().numpy()
