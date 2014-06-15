# -*- coding: utf-8 -*-

from flask import current_app

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParserBase
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search  import BooleanClause
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version



def query(q):
    """
    :param q:
    :return:search result, type list, eg. [{'name', 'path'}...]
    """
    lucene.initVM()
    index_store_dir = current_app.config['INDEX_STORE_DIR']
    directory = SimpleFSDirectory(File(index_store_dir))
    print 'directory', directory
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    parse = MultiFieldQueryParser(Version.LUCENE_CURRENT, ['name', 'title', 'content'], analyzer)
    query = MultiFieldQueryParser.parse(parse, q)
    scoreDocs = searcher.search(query, 50).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    result = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        item = dict(date=doc.get('date'), name=doc.get('name'), title=doc.get('title'), summary=doc.get('summary'))
        result.append(item)
    return result