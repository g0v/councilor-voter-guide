#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#import json
import time
import unittest
#import requests.exceptions
from requests import get

from requests.exceptions import ConnectionError

ESBASE = 'http://localhost:9200'

class TestHttpSrv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        for i in range(5):
            try:
                r = get(ESBASE)
                if r.status_code == 200:
                    time.sleep(2)
                    break
            except ConnectionError:
                time.sleep(i+1)


    def test_kibana_http_conn(self):
        r = get('http://localhost:8080/')
        self.assertEquals(200, r.status_code)

    def test_elasticsearch_http_conn(self):
        r = get('http://localhost:9200/')
        self.assertEquals(200, r.status_code)

if __name__ == "__main__":
    unittest.main()
