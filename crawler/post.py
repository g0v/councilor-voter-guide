# -*- coding: utf-8 -*-
import requests


payload = {
   'FTSearch': u'ON',
   'pagesize': u'20',
   'omastext': u'',
   'rdoDE': u'0',
   'OmasDetr': u'11',
   'OmasDetp': u'',
   'OmasDetm': u'',
   'sDateY': u'',
   'sDateM': u'',
   'sDateD': u'',
   'eDateY': u'',
   'eDateM': u'',
   'eDateD': u'',
   'spek': u''
}
r = requests.post('http://tccmis.tcc.gov.tw/OM/OM_SearchList.asp', data=payload)
r.encoding = 'Big5'
print r.text
