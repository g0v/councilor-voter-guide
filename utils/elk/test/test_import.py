#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#import json
#import time
import unittest
from elasticsearch import Elasticsearch

class TestEsImport(unittest.TestCase):

    es = None

    def setUp(self):
        if self.es is None:
            self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def test_es_fooindex_conn(self):
        res = self.es.search(index="g0v-voter-guide", doc_type='councilors', _source=False, q="platform:治安")
        self.assertTrue(res['hits']['total'] > 0)
        print "hits.total = %d" % res['hits']['total']

if __name__ == "__main__":
    unittest.main()
