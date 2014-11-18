# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ttcc.items import Councilor


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return ''

def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*年[\s]*
        (?P<month>[\d]+)[\s]*月[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.taitungcc.gov.tw"]
    start_urls = ["http://www.taitungcc.gov.tw/ourteam/01ourteam.html",]
    download_delay = 0.5

    def parse(self, response):
        councilor_index = {"1" : 10, "2" : 2, "3" : 2, "4" : 2, "5" : 1, "6" : 3, "7" : 2,
                        "8" : 1, "9" : 2, "10" : 1, "11" : 1, "12" : 1, "13" : 1, "14" : 1}

        nodes = []
        for index in councilor_index:
            list = range(councilor_index[index])
            if int(index) < 9:
                index = "0" + str(int(index)+1)
            else:
                index = str(int(index)+1)
            for i in list:
                if i < 9:
                    link = "http://www.taitungcc.gov.tw/ourteam/" + index + "ourteam_detail0" + str(i + 1) + ".html"
                else:
                    link = "http://www.taitungcc.gov.tw/ourteam/" + index + "ourteam_detail" + str(i + 1) + ".html"
                nodes.append(link)
        
        for node in nodes:
            yield Request(node, callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        item = Councilor()
        image_index =  sel.css('img').xpath('@src').extract()
        item_index = image_index[12][7:16]
        item['uid'] = item_index

        Councilor_Dict = {"01_name01" : ["張國洲", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail01.html"],
                        "01_name02" : ["陳志峰", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail02.html"],
                        "01_name03" : ["林參天", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail03.html"],
                        "01_name04" : ["李建智", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail04.html"],
                        "01_name05" : ["謝明珠", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail05.html"],
                        "01_name06" : ["饒慶鈴", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail06.html"],
                        "01_name07" : ["田石雄", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail07.html"],
                        "15_name01" : ["鄭安定", "台東市、綠島鄉、蘭嶼鄉", "false", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail08.html"],
                        "01_name09" : ["吳景愧", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail09.html"],
                        "01_name10" : ["黃秋", "台東市、綠島鄉、蘭嶼鄉", "true", "http://www.taitungcc.gov.tw/ourteam/02ourteam_detail10.html"],
                        "02_name01" : ["張卓然", "卑南鄉、延平鄉", "true", "http://www.taitungcc.gov.tw/ourteam/03ourteam_detail01.html"],
                        "02_name02" : ["張清忠", "卑南鄉、延平鄉", "true", "http://www.taitungcc.gov.tw/ourteam/03ourteam_detail02.html"],
                        "03_name01" : ["許進榮", "成功鎮、東河鄉、長濱鄉", "true", "http://www.taitungcc.gov.tw/ourteam/04ourteam_detail01.html"],
                        "03_name02" : ["林東滿", "成功鎮、東河鄉、長濱鄉", "true", "http://www.taitungcc.gov.tw/ourteam/04ourteam_detail02.html"],
                        "04_name01" : ["陳宏宗", "關山鎮、鹿野鄉、池上鄉、海端鄉", "true", "http://www.taitungcc.gov.tw/ourteam/05ourteam_detail01.html"],
                        "04_name02" : ["李振源", "關山鎮、鹿野鄉、池上鄉、海端鄉", "true", "http://www.taitungcc.gov.tw/ourteam/05ourteam_detail02.html"],
                        "05_name01" : ["李錦慧", "大武鄉、達仁鄉、金峰鄉、太麻里鄉", "true", "http://www.taitungcc.gov.tw/ourteam/06ourteam_detail01.html"],
                        "06_name01" : ["林琮翰", "平地原住民（臺東市）", "true", "http://www.taitungcc.gov.tw/ourteam/07ourteam_detail01.html"],
                        "06_name02" : ["陳。藍姆洛", "平地原住民（臺東市）", "true", "http://www.taitungcc.gov.tw/ourteam/07ourteam_detail02.html"],
                        "06_name03" : ["王清堅", "平地原住民（臺東市）", "true", "http://www.taitungcc.gov.tw/ourteam/07ourteam_detail03.html"],
                        "07_name01" : ["蔡義勇", "平地原住民（大武鄉、達仁鄉、金峰鄉、太麻里鄉、蘭嶼鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/08ourteam_detail01.html"],
                        "07_name02" : ["江堅壽", "平地原住民（大武鄉、達仁鄉、金峰鄉、太麻里鄉、蘭嶼鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/08ourteam_detail02.html"],
                        "08_name01" : ["張萬生", "平地原住民（關山鎮、池上鄉、鹿野鄉、海端鄉、延平鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/09ourteam_detail01.html"],
                        "09_name01" : ["嚴惠美", "平地原住民（成功鎮、東河鄉、長濱鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/10ourteam_detail01.html"],
                        "09_name02" : ["劉純歌", "平地原住民（成功鎮、東河鄉、長濱鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/10ourteam_detail02.html"],
                        "10_name01" : ["胡秋金", "山地原住民（成功鎮、卑南鄉、延平鄉、東河鄉、長濱鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/11ourteam_detail01.html"],
                        "11_name01" : ["余秀芳", "山地原住民（關山鎮、池上鄉、鹿野鄉、海端鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/12ourteam_detail01.html"],
                        "12_name01" : ["宋賢一", "山地原住民（金峰鄉、太麻里鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/13ourteam_detail01.html"],
                        "13_name01" : ["朱連濟", "山地原住民（大武鄉、達仁鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/14ourteam_detail01.html"],
                        "14_name01" : ["夏曼。瑪德能", "山地原住民（臺東市、綠島鄉、蘭嶼鄉）", "true", "http://www.taitungcc.gov.tw/ourteam/15ourteam_detail01.html"],}

        item['name'] = Councilor_Dict[item_index][0]
        item['constituency'] = u"第" + image_index[12][7:9] + u"選區"
        item['district'] = Councilor_Dict[item_index][1]
        item['image'] = 'http://www.taitungcc.gov.tw/ourteam/' + image_index[7]
        item['county'] = u"臺東縣"
        if item_index == "01_name06":
            item['title'] = u"議長"
        elif item_index == "04_name01":
            item['title'] = u"副議長"
        else:
            item['title'] = u"議員"
        item['election_year'] = '2009'
        item['term_start'] = '2010-03-01'
        item['term_end'] = {'date' : "2014-12-25"}
        item['in_office'] = Councilor_Dict[item_index][2]

        exp = sel.xpath('//table[@width="664"]/tr/td').extract()
        
        # Education 學歷
        edu1 = exp[0][24:].split("<br>\r\n")
        edu2 = []
        for i in edu1:
            i = i.split("</span>")
            for j in i:
                if "homepage_wo04" in j:
                    edu2 = edu2
                else:
                    edu2.append(j)
        edu2[-1] = edu2[-1][:-5]
        item['education'] = edu2
        
        # Experience 經歷
        exp1 = exp[1][63:].split("<br>\r\n")
        exp2 = []
        exp3 = []
        for i in exp1:
            i = i.split("</span>")
            for j in i:
                if "homepage_wo04" in j:
                    exp2 = exp2
                else:
                    j = j.split("<br>")
                    for k in j:
                        exp2.append(k.strip())
        exp2[-1] = exp2[-1][:-5]
        for i in exp2:
            if "strong" in i:
                break
            else:
                exp3.append(i)
        item['experience'] = exp3

        # Platform 政見
        plt1 = exp[2][24:].split("\r\n")
        plt2 = []
        for i in plt1:
            i = i.split("</span>")
            for j in i:
                if "homepage_wo04" in j:
                    plt2 = plt2
                elif j.strip() == "":
                    plt2 = plt2
                elif "<br>" in j:
                    plt2.append(j[:-4].strip())
                elif "</td>" in j:
                    plt2.append(j[:-5].strip())
                else:
                    plt2.append(j.strip())
        item['platform'] = plt2

        # Contact Information 聯絡資訊
        info = sel.xpath('//td[@width="80"]/following-sibling::*').extract()
        mail_info = sel.css('a').xpath('@href').extract()
        item['gender'] = info[0][4:5]
        item['party'] = info[1][40:-9]
        item['links'] = [{"note" : "議會個人官網", "url" : Councilor_Dict[item_index][3]}]
        if len(info) == 7:
            contact = {"voice" : info[2][20:-5], "fax" : info[3][20:-5], "address" : info[4][20:-5], "email" : mail_info[3][7:]}
            link = {"note" : "Facebook","url" : mail_info[4]}
            item['links'].append(link)
        elif len(info) == 5:
            if item_index == "15_name01":
                contact = {}
            else:
                contact = {"voice" : info[2][4:-5], "email" : mail_info[3][7:], "address" : info[4][4:-5]}
        else:
            contact = {"voice" : info[2][4:-5], "address" : info[3][4:-5]}
        contact_list = {"address" : u"通訊處", 
                        "voice" : u"電話", 
                        "fax" : u"傳真", 
                        "email" : u"電子郵件信箱"}
        item['contact_details'] = []
        for i in contact:
            item['contact_details'].append({"label" : contact_list[i], "type" : i, "value" : contact[i]})

        return item
