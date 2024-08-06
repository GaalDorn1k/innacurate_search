import sys

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/lib/libreoffice/program')

import uno
from ooodev.write import WriteDoc
from ooodev.loader import Lo
from com.sun.star.frame import XComponentLoader
from ooodev.format.writer.direct.para.alignment import Alignment
from typing import cast, List


class SofficeHandler:
    def __init__(self, doc: str, loader: XComponentLoader) -> None:
        # loader = Lo.load_office(Lo.ConnectSocket())
        fnm = cast(str, doc)
        self._doc = WriteDoc.open_doc(fnm=fnm, loader=loader, visible=True)
        self._tvc = self._doc.get_view_cursor()

    def search(self, texts: List[str]) -> int:
        search = self._doc.create_search_descriptor()
        search.search_str = texts[0]
        res = search.find_first()

        if res:
            self._tvc.goto_range(res.component)

        search.search_str = texts[-1]
        res = search.find_next(self._tvc.get_end())

        if res:
            self._tvc.goto_range(res.component, True)

        return self._tvc.get_page()

    def get_text_layout(self) -> str:
        res = self._doc.get_text()
        return res.get_string()

    def close_doc(self) -> None:
        self._doc.close_doc()

    def get_paragraphs(self) -> dict:
        cursor = self._doc.get_cursor()
        cursor.goto_start(False)  # go to start test; no selection
        paragraphs = {}
        head = ''

        while True:
            cursor.goto_end_of_paragraph(True)  # select all of paragraph
            curr_para = cursor.get_string()

            if len(curr_para) > 0:
                self._tvc.goto_range(cursor.component.getStart())
                self._tvc.goto_range(cursor.component.getEnd(), True)
                cursor.go_left(1)

                if cursor.char_weight > 100 or cursor.para_adjust == 3:
                    head = curr_para
                    paragraphs[head] = []

                else:
                    if head:
                        paragraphs[head].append(curr_para)

                cursor.go_right(1)            

            if cursor.goto_next_paragraph() is False:
                break

        return paragraphs
