#!/usr/bin/env python3.6
import html.parser
import io
import json
import re
import sys
from typing import AbstractSet, Dict, List, Optional, Sequence, Tuple
import urllib.request


SOURCE_URL = 'http://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/'  # noqa: E501

Row = Tuple[str, Optional[AbstractSet[str]]]
Table = Sequence[Row]


class BunkachouTableParser(html.parser.HTMLParser):

    font6_re = re.compile(r'\s*[（［](.)[）］]\s*')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.in_table = False
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.row_read = False
        self.font = None
        self.nested_fonts = []
        self.simplified = None
        self.traditional = None
        self.rows: Table = []

    def handle_starttag(
        self,
        tag: str,
        attrs: Sequence[Tuple[str, str]]
    ) -> None:
        if tag == 'table' and dict(attrs).get('id') == 'urlist':
            self.in_table = True
        elif self.in_table and tag == 'tbody':
            self.in_tbody = True
        elif self.in_tbody and tag == 'tr':
            self.in_tr = True
        elif self.in_tr and not self.row_read and tag == 'td':
            self.in_td = True
        elif self.in_td and tag == 'font':
            if self.font == 6:
                self.nested_fonts.append(attrs)
            else:
                size = dict(attrs).get('size', '')
                self.font = int(size) if size.isdigit() else 0

    def handle_data(self, data: str) -> None:
        if self.font == 7:
            if self.simplified is None:
                self.simplified = ''
            self.simplified += data
        elif self.font == 6:
            if self.traditional is None:
                self.traditional = ''
            self.traditional += data

    def handle_endtag(self, tag: str) -> None:
        if self.in_table and tag == 'table':
            self.in_table = False
        elif self.in_tbody and tag == 'tbody':
            self.in_tbody = False
        elif self.in_tr and tag == 'tr':
            self.in_tr = False
            traditionals = None
            if self.traditional:
                traditionals = set(self.font6_re.findall(self.traditional))
                if self.simplified in traditionals:
                    traditionals.remove(self.simplified)
            self.rows.append((self.simplified, traditionals or None))
            self.simplified = None
            self.traditional = None
            self.row_read = False
        elif self.in_td and tag == 'td':
            self.in_td = False
            self.row_read = True
        elif self.font is not None and tag == 'font':
            if self.nested_fonts:
                self.nested_fonts.pop()
            else:
                self.font = None


def shinjitai_table(table: Table) -> Dict[str, Optional[List[str]]]:
    return {
        char: variants and list(variants)
        for char, variants in table
    }


def kyujitai_table(table: Table) -> Dict[str, Optional[str]]:
    return {
        variant: (None if variant == char else char)
        for char, variants in table
        for variant in (variants or [char])
    }


def fetch(parser: BunkachouTableParser, source_url: str) -> None:
    response = urllib.request.urlopen(source_url)
    reader = io.TextIOWrapper(response, encoding='cp932')
    for chunk in reader:
        parser.feed(chunk)
    response.close()


def make_tables():
    parser = BunkachouTableParser(convert_charrefs=True)
    fetch(parser, SOURCE_URL)
    return shinjitai_table(parser.rows), kyujitai_table(parser.rows)


def main() -> None:
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} SHINJITAI_DST KYUJITAI_DST')
        raise SystemExit(1)
    _, spath, kpath = sys.argv
    st, kt = make_tables()
    with open(spath, 'w') as f:
        json.dump(st, f, indent='\t', ensure_ascii=False)
    with open(kpath, 'w') as f:
        json.dump(kt, f, indent='\t', ensure_ascii=False)


if __name__ == '__main__':
    main()
