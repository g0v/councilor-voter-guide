# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import codecs
import requests
import subprocess
from scrapy.selector import Selector

import common


def normalize_constituency(constituency):
    match = re.search(u'第(?P<num>.+)選(?:舉)?區', constituency)
    if not match:
        return 1
    try:
        return int(match.group('num'))
    except:
        pass
    ref = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9}
    if re.search(u'^\s*十\s*$', match.group('num')):
        return 10
    num = re.sub(u'^\s*十', u'一', match.group('num'))
    num = re.sub(u'十', '', num)
    digits = re.findall(u'(一|二|三|四|五|六|七|八|九)', num)
    total, dec = 0, 1
    for i in reversed(range(0, len(digits))):
        total = total + int(ref.get(digits[i], 0)) * dec
        dec = dec * 10
    return total

ref = {
    u"臺北市": "1",
    u"新北市": "2",
    u"桃園市": "3",
    u"臺中市": "4",
    u"臺南市": "5",
    u"高雄市": "6",
    u"基隆市": "7",
    u"新竹市": "8",
    u"嘉義市": "9",
    u"新竹縣": "10",
    u"苗栗縣": "11",
    u"彰化縣": "12",
    u"南投縣": "13",
    u"雲林縣": "14",
    u"嘉義縣": "15",
    u"屏東縣": "16",
    u"宜蘭縣": "17",
    u"花蓮縣": "18",
    u"臺東縣": "19",
    u"澎湖縣": "20",
    u"金門縣": "21",
    u"連江縣": "22"
}
path = u'../../data/avatar/councilors/2018/中國國民黨'
candidates = []
for county, tid in ref.items():
    print county
    r = requests.get('https://kmt2018.com/candidate_json.asp?tid=%s&cid=2' % tid)
    if r.status_code == 500:
        continue
    r.encoding = 'utf-8'
    cs = r.json()
    cs = [x for x in cs if x['name'] != u'陸續更新中']
    for candidate in cs:
        print candidate['name']
        rd = requests.get('https://kmt2018.com/read_candidate.asp?ids=%s' % candidate['uid'])
        rd.encoding = 'utf-8'
        x = Selector(text=rd.text, type='html')
        for desc in x.css('.desc .title'):
            content = '\n'.join([x.strip() for x in desc.xpath('following-sibling::div[1]//text()').extract() if x.strip()])
            if desc.xpath('text()').extract_first() == u'競選口號':
                candidate['slogan'] = content
            elif desc.xpath('text()').extract_first() == u'經歷':
                candidate['experience'] = content
            elif desc.xpath('text()').extract_first() == u'學歷':
                candidate['education'] = content
        candidate['name'] = re.sub('\s', '', candidate['name'])
        candidate['county'] = county
        candidate['constituency'] = normalize_constituency(candidate['desc'])
        img_link = candidate['picture']
        f_name = '%s_%d_%s.%s' % (candidate['county'], candidate['constituency'], candidate['name'], img_link.split('.')[-1].split('?')[0])
        f = '%s/%s' % (path, f_name)
        cmd = 'wget -N --no-check-certificate "%s" -O %s' % (img_link, f)
        subprocess.call(cmd, shell=True)
        candidate['image'] = u'%s/%s/%s/%s/%s' % (common.storage_domain(), 'councilors', '2018', u'中國國民黨', f_name)
    candidates.extend(cs)
with codecs.open('../../data/candidates/2018/kmt_councilors.json', 'w', encoding='utf-8') as ofile:
    json.dump(candidates, ofile, indent=2, ensure_ascii=False)
