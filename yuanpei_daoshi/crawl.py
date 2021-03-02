import concurrent.futures
import contextlib
import html
import http.client
import ssl

from html.parser import HTMLParser
from urllib.parse import urlparse


_DAOSHI_INDEX = 'https://yuanpei.pku.edu.cn/ypds/dsfc/index.htm'


class _PagesHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('class') == 'next':
            self._next_pg = attrs['href']
        elif tag == 'a' and attrs.get('class') == 'end':
            self._end_pg = attrs['href']

    @property
    def next_pg(self):
        if self._next_pg > self._end_pg:
            return None
        else:
            return self._next_pg

    def reset(self):
        self._next_pg = None
        self._end_pg = None
        super().reset() 


class _DaoshiLinksHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'ul' and any(k == 'class' and v == 'yp-list12' for k, v in attrs):
            self._in_daoshi_ul = True
        elif tag == 'ul' and self._in_daoshi_ul:
            self._levels += 1
        elif tag == 'li' and self._in_daoshi_ul:
            self._in_daoshi_li = True
        elif tag == 'a' and self._in_daoshi_li:
            assert len(attrs) > 0 and attrs[0][0] == 'href'
            self.links.append(attrs[0][1])

    def handle_endtag(self, tag):
        if tag == 'ul' and self._levels == 0:
            self._in_daoshi_ul = False
        elif tag == 'ul' and self._levels > 0:
            self._levels -= 1
        elif tag == 'li' and self._in_daoshi_li:
            self._in_daoshi_li = False

    def reset(self):
        self._in_daoshi_ul = False
        self._in_daoshi_li = False
        self._levels = 0
        self.links = []
        super().reset()
 

class _DaoshiHTMLParser(HTMLParser):
    def __init__(self):
        self.data = {}
        self._is_key = False
        self._this_keys = []
        self._this_values = []
        self._curr_values = []

        self._in_tr = False
        self._in_td = False
        self._in_p = False
        self._in_span = False

        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self._in_tr = True

        elif tag == 'td':
            self._in_td = True
            self._is_key = not self._is_key

        elif self._in_td and tag in ('p', 'h1'):
            self._in_p = True

        elif self._in_p and tag == 'span':
            self._in_span = True

    def _write_entry(self):
        k = '\n'.join(k for k in self._this_keys if not k.isspace()).strip('\n').replace('\n', ' ')
        v = [v.strip('\n ') for v in self._this_values]
        v = [vv for vv in v if len(vv) > 0 and not vv.isspace()]
        if len(v) == 1:
            v = v[0]
        elif len(v) == 0:
            v = ''

        self.data[k] = v
        self._this_keys = []
        self._this_values = []

    def handle_endtag(self, tag):
        if tag == 'tr' and self._in_tr:
            self._in_tr = False
            self._is_key = False
            if len(self._this_keys) > 0 or len(self._this_values) > 0:
                self._write_entry()

        elif tag == 'td' and self._in_td:
            self._in_td == False

            if not self._is_key:
                self._write_entry()

        elif tag in ('p', 'h1') and self._in_p:
            self._in_p = False
            if not self._is_key:
                self._this_values.append(''.join(self._curr_values))
                self._curr_values = []

        elif tag == 'span' and self._in_span:
            self._in_span = False

    def handle_data(self, data):
        if self._in_span:
            if self._is_key:
                self._this_keys.append(html.unescape(data))
            else:
                self._curr_values.append(html.unescape(data))


@contextlib.contextmanager
def _conn_to(base):
    conn = http.client.HTTPSConnection(base, context=ssl._create_unverified_context()) 
    try:
        yield conn
    finally:
        conn.close()


def _get_raw_html(base, path):
    with _conn_to(base) as conn:
        conn.request("GET", path)
        resp = conn.getresponse()
        assert resp.status == 200, f"req to {base}{path} failed <{resp.status}>"
        return resp.read().decode('utf-8')  # assume always utf-8


def _change_last_to(path, new_last):
    assert '/' in path
    return path[:path.rfind('/')+1] + new_last


def _get_raw_html_and_pg(base, path, pages_html_parser):
    raw_html = _get_raw_html(base, path)
    pages_html_parser.feed(raw_html)
    next_pg = pages_html_parser.next_pg
    pages_html_parser.reset()

    return raw_html, next_pg


def _crawl_one(base, path):
    parser = _DaoshiHTMLParser()
    raw_html = _get_raw_html(base, path)
    parser.feed(raw_html)

    return parser.data


def crawl_all(index_page=_DAOSHI_INDEX):
    pages_html_parser = _PagesHTMLParser()
    ds_links_html_parser = _DaoshiLinksHTMLParser()

    parsed_url = urlparse(index_page)
    base, path = parsed_url.netloc, parsed_url.path
    raw_html, next_pg = _get_raw_html_and_pg(base, path, pages_html_parser)

    links = []
    while next_pg is not None:
        ds_links_html_parser.feed(raw_html)
        links.extend(ds_links_html_parser.links)
        ds_links_html_parser.reset()

        path = _change_last_to(path, next_pg)
        raw_html, next_pg = _get_raw_html_and_pg(base, path, pages_html_parser)

    ds_links_html_parser.feed(raw_html)
    links.extend(ds_links_html_parser.links)

    for i in range(len(links)):
        links[i] = _change_last_to(path, links[i])

    daoshi = []
    n_err = n_completed = 0
    total = len(links)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        fs = {}
        for link in links:
            fs[executor.submit(_crawl_one, base, link)] = f"{base}{link}"

        for f in concurrent.futures.as_completed(fs):
            try:
                daoshi.append(f.result())
                n_completed += 1
            except Exception as e:
                print("\r" + " " * 100, end='')  # clear line
                print(f"\rlink: {fs[f]} has error: {e}")
                n_err += 1

            print(f"\rcompleted: {n_completed} / {total}, errors: {n_err}", end='')
        print()

    return daoshi

