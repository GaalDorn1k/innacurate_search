from langchain_core.documents import Document
from typing import List


class Splitter:
    def __init__(self) -> None:
        pass

    def split(self, text: str) -> List[Document]:
        text = text.split('\n')
        chunks = []

        for n, text in enumerate(text):
            # chunk = Document(page_content=text,
            #                  metadata={'chunk_index': n})
            chunks.append(text)

        return chunks
