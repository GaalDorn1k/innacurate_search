import os

from index import FaissIdx
from embeddings import HFEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from soffice_handler import SofficeHandler


class Client:
    def __init__(self, embedder: HuggingFaceEmbeddings, search_treshold: float) -> None:
        self.open_doc_name = ''
        self.search_treshold = search_treshold
        self.embeddings = HFEmbeddings(model_name=embedder)
        self.office_handler = SofficeHandler()

    def search(self, query: str) -> dict:
        response = self.heads_index.search_doc(query, 1)

        if response['score'] < self.search_treshold:
            response = self.body_index.search_doc(query, 1)
            s = [response['text']]

        else:
            s = [response['text']]

            if self.chunks[response['text']]:
                s.append(self.chunks[response['text']][-1])

        page = self.office_handler.search(s)

        return {'exists': True if response else False,
                'pages': page,
                'text': response}

    def open_doc(self, path: str) -> None:
        self.office_handler.open_doc(path)
        self.chunks = self.office_handler.get_paragraphs()
        self.heads_index = FaissIdx(self.embeddings, 384)
        self.body_index = FaissIdx(self.embeddings, 384)

        for head, body in self.chunks.items():
            self.heads_index.add_doc(head)
            for paragraph in body:
                self.body_index.add_doc(paragraph)

    def close_doc(self) -> None:
        self.office_handler.close_doc()

    def run(self) -> None:
        print('Enter "@open path/to/doc" for open doc')
        print('Enter "search_query" for search')

        while True:
            query = input(':: ')

            if '@open' in query:
                if self.open_doc_name:
                    self.close_doc()

                body = query.split()[1]

                if os.path.exists(body):
                    self.open_doc(body)
                    self.open_doc_name = body
                else:
                    print(f'{body} not found')

            elif '@close' in query:
                self.close_doc()

            elif self.open_doc_name:
                self.search(query)

            else:
                print('Enter "@open path/to/doc" for open doc')
