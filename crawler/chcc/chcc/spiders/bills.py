# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from chcc.items import Bills
from urlparse import urljoin

class Spider(scrapy.Spider):
    name = "bills"

    allowed_domains = ["www.chcc.gov.tw"]
    start_urls = ["http://www.chcc.gov.tw/content/review/review01.aspx?PType=1"]
    '''
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost/chcc_detail2.html"]
    '''
    def parse(self, response):
    	result=[]
    	sel = Selector(response)
    	index=sel.xpath(".//table[@bgcolor='#DBDBDB']/tr")
    	for index_idx in range(1, len(index)):
    		item = Bills()
    		table_links=index[index_idx].xpath(".//td/a/@href").extract()
    		print len(table_links)
    		for obj in table_links:
    			print obj
    			link=urljoin(response.url, obj)
    			print link
    			request=Request(link, callback=self.parse_table)
    			request.meta['item'] = item
    			yield request

    def parse_table(self, response):
    	sel = Selector(response)
    	item = response.request.meta['item']
    	table=sel.xpath(".//table[@bgcolor='#DBDBDB']/tr")
    	print 'parse_table=',len(table)
    	for table_idx in range(1,len(table)):
    		href=table[table_idx].xpath(".//td/a/@href").extract()[0]
    		link=urljoin(response.url, href)
    		request = Request(link, callback=self.parse_bill)
     		request.meta['item'] = item
     		yield request

    def parse_bill(self, response):
    	sel = Selector(response)
    	item = response.request.meta['item']
    	#item = Bills()

    	title=sel.xpath(".//span[@id='LbRT_title']/text()").extract()[0]
    	print title
    	table=sel.xpath(".//table[@bgcolor='#DBDBDB']/tr")
    	#print len(table)
    	item['county']=u'彰化縣'
    	item['election_year']='2009'
    	item['proposed_by']=[]
    	item['petitioned_by']=[]
    	item['motions']=[]
    	item['links']=response.url
    	id_index=response.url.find('=')
    	item['id']=response.url[id_index+1:]
    	print item['id']
    	committee_motion={}
    	#count=0
    	for detail in table:
    		#print count, len(item['motions'])
    		#count += 1
    		itemNames=detail.xpath(".//th")
    		itemInfo=detail.xpath(".//td")
    		#print itemNames[0].xpath("text()").extract()

    		for idx in range(0, len(itemNames)):
    			if itemNames[idx].re(u'審查意見'):
    				committee_motion={'motion':u'委員會審查意見', 'resolution':itemInfo[idx].xpath("text()").extract()[0], 'sitting': title}
    				item['motions'].append(committee_motion)
    				#print len(item['motions'])
    			if itemNames[idx].re(u'案號'):
    				item['bill_no']=itemInfo[idx].xpath("text()").extract()[0]
    				#print item['bill_no']
    			if itemNames[idx].re(u'類別'):
    				item['category']=itemInfo[idx].xpath("text()").extract()[0]
    				#print item['category']
    			if itemNames[idx].re(u'提案人'):
    				people=itemInfo[idx].xpath("text()").extract()[0]
    				persons=people.split(u'、')
    				print len(persons)
    				for obj in persons:
    					item['proposed_by'].append(obj)
    			if itemNames[idx].re(u'連署人') or itemNames[idx].re(u'附議人'):
    				people=itemInfo[idx].xpath("text()").extract()[0]
    				persons=people.split(u'、')
    				print len(persons)
    				for obj in persons:
    					item['petitioned_by'].append(obj)
    			if itemNames[idx].re(u'案由'):
    				#item['abstract']=itemInfo[idx].xpath("text()").extract()
    				texts=itemInfo[idx].xpath("text()").extract()
    				abstract=''
    				for obj in texts:
    					abstract += obj
    				#print abstract
    				item['abstract']=abstract
    			if itemNames[idx].re(u'說明'):
    				texts=itemInfo[idx].xpath("text()").extract()
    				description=''
    				for obj in texts:
    					description += obj
    				#print len(texts), description
    				item['description']=description
    			if itemNames[idx].re(u'大會決議'):
					print '大會決議'
					committee_motion={'motion':u'大會決議', 'resolution':itemInfo[idx].xpath("text()").extract()[0], 'sitting': title}
					item['motions'].append(committee_motion)
    	return item
