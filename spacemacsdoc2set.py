#!/usr/bin/env python3

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag


DOC_ROOT = 'Spacemacs.docset/Contents/Resources/Documents/'
DOC_DIR = 'doc'
DOCS = [
    ('quick_start.html', 'Guide'),
    ('beginners_tutorial.html', 'Guide'),
    ('vimusers.html', 'Guide'),
    ('documentation.html', 'Framework'),
    ('layers.html', 'Library')
]


insert_to_db = lambda cursor, doc_name, doc_type, doc_path: \
    cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (doc_name, doc_type, doc_path))

get_doc_path = lambda doc: os.path.join(DOC_DIR, doc)

get_full_doc_path = lambda doc: os.path.join(DOC_ROOT,DOC_DIR, doc)

load_page = lambda doc: BeautifulSoup(open(get_full_doc_path(doc)).read(), 'html.parser')


def build_doc(cursor, doc_type, doc):
    org_tag = re.compile('#.')
    num_text = re.compile('^\d+\.\d+.')
    text_regex = re.compile('\.\s([A-z\s\-]+)')
    soup = load_page(doc)

    if doc_type == 'Guide':
        name = soup.find('title').text.strip()
        insert_to_db(cursor, name, doc_type, get_doc_path(doc))

    elif doc_type in ('Framework', 'Library'):
        for tag in soup.find_all('a', {'href':org_tag}, text=num_text):
            name = text_regex.findall(tag.text.strip())[-1]
            path = get_doc_path(doc) + tag.attrs['href'].strip()
            insert_to_db(cursor, name, doc_type, path)
            print ('name: {}, type: {} path: {}'.format(name, doc_type, path))


if __name__ == '__main__':

    conn = sqlite3.connect('Spacemacs.docset/Contents/Resources/docSet.dsidx')
    cursor = conn.cursor()

    try:
        cursor.execute('DROP TABLE searchIndex;')
    except e:
        pass

    cursor.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cursor.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    for doc, doc_type in DOCS:
        build_doc(cursor, doc_type, doc)

    conn.commit()
    conn.close()
