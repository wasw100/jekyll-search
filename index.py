# -*- coding: utf-8 -*-
"""
create pylucene index
"""
import re
from flask import current_app

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

FILENAME_PATERN = re.compile(r'(\d+-\d+-\d+)-(.+)\.md')

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


def build_index():

    lucene.initVM()

    # post_dir = current_app.config['LOCAL_REPO_PATH'] + '/_posts/'
    post_dir = '/Users/w3/data/github/codeif_backup'
    index_store_dir = current_app.config['INDEX_STORE_DIR']
    print post_dir
    print index_store_dir

    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    store = SimpleFSDirectory(File(index_store_dir))
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    indexDocs(post_dir, writer)
    ticker = Ticker()
    print 'commit index',
    threading.Thread(target=ticker.run).start()
    writer.commit()
    writer.close()
    ticker.tick = False
    print 'done'


def indexDocs(root, writer):
        """
        indexed: name title content
        stored: date name tilte sumary
        :param root:
        :param writer:
        :return:
        """
        #index and store
        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        #only index, but not store
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        #only store
        t3 = FieldType()
        t3.setIndexed(False)
        t3.setStored(True)
        t3.setTokenized(False)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        for root, dirnames, filenames in os.walk(root):
            print filenames
            for filename in filenames:
                if not filename.endswith('.md'):
                    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'utf-8')
                    file.close()

                    date, name = get_date_name(filename)
                    title, content = get_post_title_content(contents)
                    summary = content[:200] if content else ''

                    print date, name, title

                    doc = Document()
                    doc.add(Field('date', date, t3))
                    doc.add(Field('name', name, t1))
                    doc.add(Field('title', title, t1))
                    doc.add(Field('content', content, t2))
                    doc.add(Field('summary', summary, t3))


                    # doc.add(Field("name", filename, t1))
                    # doc.add(Field("path", root, t1))
                    # if len(contents) > 0:
                    #     doc.add(Field("contents", contents, t2))
                    # else:
                    #     print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


def get_date_name(filename):
    """
    :param filename: markdown file name
    :return: get date and name by markdown filename
    """
    m = FILENAME_PATERN.match(filename)
    if m:
        return m.groups()
    else:
        return None, None


def get_post_title(header_text):
    for line in header_text.split('\n'):
        line = line.strip()
        key_value = line.split(':', 1)
        if len(key_value) == 2 and key_value[0].strip().lower()=='title':
            return key_value[1].strip()


def get_post_title_content(text):
    """
    :param text:
    :return: get post title and content
    """
    contents = text.split('---', 2)
    if len(contents) == 3:
        header_text = contents[1]
        post_title = get_post_title(header_text)
        post_content = contents[2]
        return post_title, post_content
    return None, None


