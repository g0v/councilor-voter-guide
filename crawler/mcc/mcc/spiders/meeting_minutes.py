# -*- coding: utf-8 -*-
import re
import os
import json
import string
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import selenium
from selenium import webdriver
import pyvirtualdisplay
from pyvirtualdisplay import Display
from mcc.items import MeetingMinutes
from crawler_lib import parse
import csv
import zipfile
import xml.etree.ElementTree as ElementTree

'''
Data source:
http://mcc.digital.tpa.gov.tw/query.php?act=opendata
    for tag in "div.info_block/div.book_data"
        Tag = find "span.info_value[0]" in tag
        assert(Tag.text == '016z-[0-1][0-9]-[0-9][0-9]') where [0-1][0-9] is 屆數 and [0-9][0-9] is 冊數
        Excel = 'application.php?act=meta_download&target=%s' % Tag.text
        CSV = 'application.php?act=imglink_download&target=%s' % Tag.text
Instruction:
To login, get http://mcc.digital.tpa.gov.tw/index.php?act=GuestLogin
To link the open-data page after logged-in, get http://mcc.digital.tpa.gov.tw/index.php?act=opendata
To logout, get http://mcc.digital.tpa.gov.tw/index.php?act=logout
'''

'''
許願池：(YauHsien, 2014/11/24) 請幫我解決
1. 文獻標準「類、綱、目」號對應的類別名稱。
2. 多個 download_url 的表達法。
'''

class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ['digital.tpa.gov.tw']
    start_urls = ['http://mcc.digital.tpa.gov.tw/index.php?act=GuestLogin']
    meta_url_temp = 'http://mcc.digital.tpa.gov.tw/application.php?act=meta_download&target=%s'
    imglink_url_temp = 'http://mcc.digital.tpa.gov.tw/application.php?act=imglink_download&target=%s'
    download_delay = 2
    folder = None
    #---- helper ------
    number_map = None

    def __init__(self):
        fh = open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())
        self.number_map = make_number_map()

    def parse(self, response):
#       response = parse.get_decoded_response(response, 'Big5')
        return Request('http://mcc.digital.tpa.gov.tw/query.php?act=opendata', callback=self.parse1)

    def get_opendata_urls(self, response):
        for key in response.css('.info_block').xpath('div[@class="book_data"][1]')\
                           .css('.info_value::text').extract():
            yield (self.meta_url_temp % key, self.imglink_url_temp % key)

    def create_working_folder(self):
        try:
            os.system('mkdir %s' % self.folder)
        except:
            pass

    def remove_working_folder(self):
        try:
            os.system('rm -rf %s' % self.folder)
        except:
            pass

    def parse1(self, response):
#       response = parse.get_decoded_response(response, 'Big5')
        self.folder = '/tmp/cvg-%s' % self.__module__
        self.create_working_folder()
        urls = [ (xls, csv) for (xls, csv) in self.get_opendata_urls(response) ]
        urls.reverse()
        #urls1 = [urls[-1]] ## for debugging, eliminate urls to urls1, and use the following line
        #yield self.download_seq(urls1, [])
        yield self.download_seq(urls, [])

    def download_seq(self, urls, acc):
        if urls == []:
            return Request('http://mcc.digital.tpa.gov.tw/index.php?act=logout',
                          callback=self.parse_profile,
                          meta={'acc': acc})
        else:
            # closure for Request sequence
            urlx, urlc = urls[0]
            return Request(urlx,
                           callback=self.download_callback_1,
                           meta={'urlx': urlx, 'urlc': urlc, 'urls': urls[1:], 'acc': acc})

    def download_callback_1(self, response):
        urlx = response.meta['urlx']
        urlc = response.meta['urlc']
        urls = list(response.meta['urls'])
        acc = list(response.meta['acc'])
        xls = self.save_file(response)
        print('%s: %s' % ('crawled', urlx))
        return Request(urlc, callback=self.download_callback_2, meta={'urlc': urlc, 'xls': xls, 'urls': urls, 'acc': acc})

    def download_callback_2(self, response):
        urlc = response.meta['urlc']
        xls = response.meta['xls']
        urls = list(response.meta['urls'])
        acc = list(response.meta['acc'])
        csv = self.save_file(response)
        acc.extend([(xls,csv)])
        print('%s: %s' % ('crawled', urlc))
        return self.download_seq(urls, acc)

    def download(self, url):
        return Request(url, callback=self.save_file)

    def save_file(self, response):
        FileName = response.headers['Content-Disposition'].split('filename="')[1].split('"')[0]
        path = os.path.join(self.folder, FileName)
        with open(path, 'wb') as f:
            f.write(response.body)
        return path

    def parse_profile(self, response):
#       response = parse.get_decoded_response(response, 'Big5')
        acc = list(response.meta['acc'])
        items = []
        map(lambda(xlsx, csv): self.parse_profile1(xlsx, csv, items), acc)
        self.remove_working_folder()
        return items

    def parse_profile1(self, xlsx, csv, acc):
        for item in self.parse_profile2(xlsx_to_csv(xlsx), csv):
            acc.append(item)

    def parse_profile2(self, csv1, csv2):
        #items = []
        ImgRepo = load_images(csv2)
        with open(csv1, 'r') as csvfile:
            reader = csv.reader(csvfile, dialect=csv.excel)
            for i in 1,2,3:
                reader.next()
            for row in reader:
                if all([x == '' for x in row]):
                    continue
                try:
                    #------ Take Image URLs ----------
                    class0 = row[1]
                    class1 = row[9]
                    class2 = row[2]
                    image_number_start = int(row[18].split('.')[0])
                    image_number_end = int(row[19].split('.')[0])
                    image_type = row[18].split('.')[1]
                    image_names = map(lambda n: '%s-%s-%s-%04d.%s' % (class0, class1, class2, n, image_type),
                                      [i for i in xrange(image_number_start, image_number_end+1)])
                    image_urls = filter(lambda x: x is not None,
                                        map(lambda name: ImgRepo[name] if name in ImgRepo else None, image_names))
                    #------ Produce Items ------------
                    item = MeetingMinutes()
                    item['county'] = u'苗栗縣'
                    item['sitting'] = unicode(row[7], 'utf-8')  #------------- 抓「案由」
                    item['category'] = '%s.%s.%s' % (row[3], row[4], row[5]) # 抓標準分類「類、綱、目」號
                    item['date'] = unicode(row[22], 'utf-8')
                    item['meeting'] = take_meeting_number(unicode(row[13], 'utf-8'), self.number_map) # 抓「會議別」
                    item['download_url'] = string.join(image_urls, ',')
                    ##print('%s: %s' % ('yield', item))
                    yield item
                except Exception as ex:
                    continue #暫且將不完整的輸入資料，以及錯誤的輸入資料，給跳過
            csvfile.close()

#-------------------------------------------
#
# helpers
#

def load_images(csv2):
    result = {}
    with open(csv2, 'r') as csvfile:
        reader = csv.reader(csvfile, dialect=csv.excel)
        reader.next()
        for row in reader:
            image_name = row[3]
            image_link = u'http://%s' % row[4]
            result.update({image_name: image_link})
        csvfile.close()
    return result

def make_number_map():
    mp = {}
    map(lambda (k,v): mp.update({k: v}), zip(u'一二三四五六七八九', [1,2,3,4,5,6,7,8,9]))
    return mp

def take_meeting_number(word, mp):
    matchTerm = re.search(u'第(?P<num>.+)次會議', word, re.X)
    if matchTerm:
        ## 連續中文數字轉阿拉伯數字尚未處理
        #n = reduce(lambda x, y: x*10+y, map(lambda k: mp[k], matchTerm.group('num').split(u'十')))
        return matchTerm.group('num')
    else:
        return None

#-------------------------------------------
#
# .xlsx to .csv
#

def unzip(Filename):
    zipfile.ZipFile(Filename).extractall('/tmp')
    return '/tmp/xl'

def take_sharedStrings(Filename):
    xmlns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    result = {}
    running_path = []
    meet_si = False
    t_bag = None
    for event, node in ElementTree.iterparse(Filename, events=('start','end')):
        if event == 'start' and not meet_si:
            running_path.extend([node.tag])
            if node.tag == '{%s}si' % (xmlns):
                meet_si = True
                t_bag = ''
        if meet_si and event == 'end' and node.tag == '{%s}t' % (xmlns):
            t_bag = t_bag + node.text
        if event == 'end' and meet_si:
            running_path = running_path[:-1]
            meet_si = False
            result.update({len(result): t_bag})
        if event == 'end':
            node.clear()
    return result

def take_rows(Filename, sharedStrings):
    xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns_r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    running_path = []
    running_row = None
    for event, node in ElementTree.iterparse(Filename, events=('start','end')):
        if event == 'start':
            running_path.extend([node.tag])
            if '/'.join(running_path) == '{%s}worksheet/{%s}sheetData/{%s}row' % (xmlns, xmlns, xmlns):
                running_row = []
            if '/'.join(running_path) == '{%s}worksheet/{%s}sheetData/{%s}row/{%s}c' % (xmlns, xmlns, xmlns, xmlns):
               running_type = node.attrib['t'] if 't' in list(node.attrib) else None
        if event == 'end':
            if '/'.join(running_path) == '{%s}worksheet/{%s}sheetData/{%s}row/{%s}c/{%s}v' % (xmlns, xmlns, xmlns, xmlns, xmlns):
                if running_type == 's':
                    running_row.extend([sharedStrings[int(node.text)]])
                else:
                    running_row.extend([node.text])
            if '/'.join(running_path) == '{%s}worksheet/{%s}sheetData/{%s}row/{%s}c' % (xmlns, xmlns, xmlns, xmlns) and len(node._children) == 0:
                running_row.extend([''])
            if '/'.join(running_path) == '{%s}worksheet/{%s}sheetData/{%s}row' % (xmlns, xmlns, xmlns):
                yield(running_row)
            running_path = running_path[:-1]
            node.clear()

def xlsx_to_csv(filepath):
    filepath1 = '%s.csv' % filepath
    path = unzip(filepath) # to generate unzipped file at /tmp/xl/
    sharedStrings = take_sharedStrings('/tmp/xl/sharedStrings.xml')
    f = open(filepath1, 'w')
    c = csv.writer(f, lineterminator='\n')
    for row in take_rows('/tmp/xl/worksheets/sheet1.xml', sharedStrings):
        c.writerows([[s.encode('utf-8') for s in row]])
    f.close()
    try:
        os.system('rm -rf /tmp/xl')
    except:
        pass
    return filepath1
