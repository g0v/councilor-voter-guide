import json
import unittest
from binhash import makelist

class TestRedis(unittest.TestCase):

    def setUp(self):
        pass

    def test_makelist(self):
        # $ sha256sum test/data/bin.txt
        # 317b8e1765bbb4be1a4cbff522264f5292aea029b03be2bcbda12e0da1dc55ed  test/data/bin.txt
        r0 = {'name':'bin.txt',
              'dir':'test/data',
              'sha256':'317b8e1765bbb4be1a4cbff522264f5292aea029b03be2bcbda12e0da1dc55ed',
              'size':13}
        r = makelist('test/data','http://localhost/waa')
        self.assertTrue('created_time' in r)
        self.assertTrue('host_path' in r)
        self.assertEquals('http://localhost/waa', r['host_path'])
        self.assertEquals(len(r['list']), 1)
        t0 = r['list'][0]
        self.assertEquals(t0, r0)

if __name__ == "__main__":
    unittest.main()
