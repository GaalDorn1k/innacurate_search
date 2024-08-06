import sys

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/lib/libreoffice/program')

import uno
import os
import json

from tqdm import tqdm
from pprint import pprint
from index import FaissIdx
from ooodev.loader import Lo
from embeddings import HFEmbeddings
from soffice_handler import SofficeHandler


EMBEDDER = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
SEARCH_TRHESH = 0.8


class InnacurateSearcher:
    def __init__(self) -> None:
        self.open_doc_name = ''
        self.embeddings = HFEmbeddings(model_name=EMBEDDER)
        self.doc_loader = Lo.load_office(Lo.ConnectSocket())

    def search(self, query: str) -> dict:
        response = self.heads_index.search_doc(query, 1)

        if response['score'] < SEARCH_TRHESH:
            response = self.body_index.search_doc(query, 1)
            s = [response['text']]

        else:
            s = [response['text']]

            if self.chunks[response['text']]:
                s.append(self.chunks[response['text']][-1])

        # pprint(response)
        page = self.office_handler.search(s)

        return {'exists': True if response else False,
                'pages': page,
                'text': response}

    def open_doc(self, path: str) -> None:
        self.office_handler = SofficeHandler(path, self.doc_loader)
        self.chunks = self.office_handler.get_paragraphs()
        self.heads_index = FaissIdx(self.embeddings, 384)
        self.body_index = FaissIdx(self.embeddings, 384)

        for head, body in self.chunks.items():
            self.heads_index.add_doc(head)
            for paragraph in body:
                self.body_index.add_doc(paragraph)

    def close_doc(self) -> None:
        # if self.open_doc_name:
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


if __name__ == '__main__':
    service = InnacurateSearcher()
    service.run()

    # METRICS

    # dataset_path = '/home/user0/projects/0000/dataset.json'
    # docs_path = '/home/user0/projects/0000/documents'

    # with open(dataset_path, 'r', encoding='utf-8') as jf:
    #     etalons = json.load(jf)['documents']

    # search_rows = {
    #     0: "арбитражная оговорка",
    #     1: "антикоррупционная оговорка",
    #     2: "форс-мажор",
    #     3: "неустойка"
    # }

    # def search_frame_in_etalons(doc_name: str) -> list:
    #     for item in etalons:
    #         if item['document_name'][:item['document_name'].rfind('.')] == doc_name[:doc_name.rfind('.')]:
    #             return item['sections']

    # positives = 0

    # for name in tqdm(os.listdir(docs_path)):
    #     if not (name.lower().endswith('doc') or name.lower().endswith('docx')):
    #         continue

    #     service.open_doc(os.path.join(docs_path, name))
    #     sections = search_frame_in_etalons(name)

    #     if sections is None:
    #         service.close_doc()
    #         continue

    #     for i in range(4):
    #         response = service.search(search_rows[i])

    #         # try:
    #         #     target = sections[i]
    #         # except Exception:
    #         #     continue

    #         target = sections[i]

    #         if response['exists'] == target['exists']:
    #             if target['exists']:
    #                 if response['pages'] in target['pages']:
    #                     positives += 1

    #     service.close_doc()

    # print(positives / (len(etalons) * 4))
    # print(positives)
    # print(len(etalons) * 4)
