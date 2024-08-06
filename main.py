import faiss
import argparse

from embeddings import HFEmbeddings
from index import FaissIdx
from splitter import Splitter
from soffice_handler import SofficeHandler
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_community.embeddings import HuggingFaceEmbeddings


TRHESH = 0.8

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True, help='path to document')
    args = parser.parse_args()

    office_handler = SofficeHandler(args.file)
    chunks = office_handler.get_paragraphs()
    embeddings = HFEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    heads_index = FaissIdx(embeddings, 384)
    body_index = FaissIdx(embeddings, 384)

    for head, body in chunks.items():
        heads_index.add_doc(head)
        for paragraph in body:
            body_index.add_doc(paragraph)

    while True:
        query = input('Input query: ')
        # response = retriever.invoke(query)
        response = heads_index.search_doc(query, 1)
        print(response)

        if response['score'] < TRHESH:
            response = body_index.search_doc(query, 1)
            print(response)
            s = [response['text']]
        # office_handler.search(response[0].page_content)
        # for item in response:

        else:
            s = [response['text']]

            if chunks[response['text']]:
                s.append(chunks[response['text']][-1])

        office_handler.search(s)
