from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
import numpy as np
import torch.nn.functional as F
import torch


class HFEmbeddings:
    def __init__(self,
                 model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

    def get_embeddings(self, text: str) -> np.ndarray:
        emb = self.embeddings.embed_query(text)
        emb = torch.Tensor([emb])
        emb = F.normalize(emb, p=2, dim=1)
        return emb.detach().numpy()
