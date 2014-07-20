# -*- coding: utf-8 -*-
import requests
import codecs


payload = {
   'queryCol': u'period',
   'queryStr': u'66_01',
   'perPage': u'300'
}
r = requests.post('http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/baseList.jsp&ctNode=', data=payload)
#r.encoding = 'Big5'
print r.text
