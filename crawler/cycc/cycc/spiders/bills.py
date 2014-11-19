# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from cycc.items import Bills
from urlparse import urljoin
import os
import json

class Spider(scrapy.Spider):
    name = "bills"
    
    allowed_domains = ["www.cycc.gov.tw"]
    start_urls = ["http://www.cycc.gov.tw/form3/index.asp?m=99&m1=7&m2=24&sid="]
    '''
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost/cy17_u.html"]
    '''
    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'meetingTitle.json'), 'r')
        self.meetingTitle = json.loads(fh.read())

    def parse(self, response):
    	sel = Selector(response)
    	item = []

    	for sid in range(1,18):
    		link=response.url+str(sid)
    		#print link
    		request=Request(link, callback=self.parse_page)
	    	request.meta['item'] = item
	    	yield request

    def parse_page(self, response):
    	sel = Selector(response)
    	item = response.request.meta['item']

    	pages=sel.xpath(".//a[@class='link-page']/@href")
    	print len(pages)
    	for page_idx in range(1,len(pages)+2):
    		link=response.url+'&page='+str(page_idx)
    		print link
	    	request=Request(link, callback=self.parse_bill)
	    	request.meta['item'] = item
	    	yield request

    def parse_bill(self, response):
    	sel = Selector(response)
    	#itemResult = response.request.meta['item']
    	itemResult=[]
    	sid=''
    	title=''
    	#itemResult=[]
  	
    	tables=sel.xpath(".//table[@bgcolor='#37B7FB']")
    	print len(tables)
    	for table in tables:
    		detailes=table.xpath(".//tr")
    		#print len(detailes)
    		item = Bills()

    		item['proposed_by']=[]
    		item['petitioned_by']=[]
    		item['motions']=[]
    		item['category']='unknown'
    		item['bill_no']='none'
    		item['links']=response.url
    		for detail in detailes:
    			itemNames=detail.xpath(".//th")
    			itemInfo=detail.xpath(".//td/span")
    			committee_motion={}

    			for idx in range(0, len(itemNames)):
    				if itemNames[idx].re(u'[\s]*類[\s]*別[\s]*'):
    					infos=itemInfo[idx].xpath("text()").extract()
    					if len(infos):
    						item['category']=itemInfo[idx].xpath("text()").extract()[0]		
    					#print item['category']
    				if itemNames[idx].re(u'[\s]*編[\s]*號[\s]*'):
    					item['bill_no']=itemInfo[idx].xpath("text()").extract()[0]		
    					#print item['bill_no']
    					meeting_id_startidx=response.url.find('sid=')+4
		    			subUrl=response.url[meeting_id_startidx:]
		    			meeting_id_endidx=subUrl.find('&')
		    			sid=subUrl[:meeting_id_endidx]
		    			#print sid
		    			title=self.meetingTitle[sid]
		    			#print title
		    			bill_id=sid+'_'+item['category']+'_'+item['bill_no']
		    			item['id']=bill_id
		    			print item['id']    			
    				if itemNames[idx].re(u'[\s]*提[\s]*案[\s]*人'):
	    				people=itemInfo[idx].xpath("text()").extract()[0].replace(u'\r\n', u'\u3000')
	    				persons=people.split(u'\u3000')
	    				#print len(persons)
	    				for obj in persons:
	    					#print obj
	    					if len(obj):
	    						names=obj.split(u' ')

		    					name_count=0;
		    					#print len(names)
		    					while(name_count<len(names)):
		    						if len(names[name_count])==0:
		    							name_count +=1
		    							continue
		    						if len(names[name_count])==1:
		    							if (name_count+2) < len(names):
		    								proposed_name=names[name_count]+names[name_count+2]
		    							else:
		    								proposed_name=names[name_count]+names[len(names)-1]
		    							name_count += 3
		    						else:
		    							proposed_name=names[name_count]
		    							name_count += 1
		    						#print proposed_name
	    							item['proposed_by'].append(proposed_name)
	    			if itemNames[idx].re(u'[\s]*連[\s]*署[\s]*人') or itemNames[idx].re(u'[\s]*附[\s]*議[\s]*人'):
	    				if itemInfo[idx].xpath("text()").extract():
		    				people=itemInfo[idx].xpath("text()").extract()[0].replace(u'\r\n', u'\u3000')

		    				persons=people.split(u'\u3000')
		    				#print len(persons)
		    				for obj in persons:
		    					names=obj.split(u' ')

		    					name_count=0;
		    					#print len(names)
		    					while(name_count<len(names)):
		    						if len(names[name_count])==0:
			    						name_count +=1
			    						continue	
		    						if len(names[name_count])==1:
		    							if (name_count+2) < len(names):
		    								petitioned_name=names[name_count]+names[name_count+2]
		    							else:
		    								petitioned_name=names[name_count]+names[len(names)-1]
		    							name_count += 3
		    						else:
		    							petitioned_name=names[name_count]
		    							name_count += 1
		    						#print petitioned_name	
		    						item['petitioned_by'].append(petitioned_name)
	    			if itemNames[idx].re(u'[\s]*案[\s]*由'):
	    				#item['abstract']=itemInfo[idx].xpath("text()").extract()
	    				texts=itemInfo[idx].xpath("text()").extract()
	    				abstract=''
	    				for obj in texts:
	    					abstract += obj.replace('\r\n','')
	    				item['abstract']=abstract	
    				if itemNames[idx].re(u'[\s]*理[\s]*由'):
	    				texts=itemInfo[idx].xpath("text()").extract()
	    				description=''
	    				for obj in texts:
	    					description += obj.replace('\r\n','')	
	    				item['description']=description
    				if itemNames[idx].re(u'[\s]*決[\s]*議[\s]*'):
    					print '大會決議'
    					committee_motion={'motion':u'大會決議', 'resolution':itemInfo[idx].xpath("text()").extract()[0], 'sitting':title}
    					item['motions'].append(committee_motion)
    				if itemNames[idx].re(u'[\s]*審[\s]*查[\s]*意[\s]*見'):
    					committee_motion={'motion':u'委員會審查意見', 'resolution':itemInfo[idx].xpath("text()").extract()[0],'sitting':title}
    					item['motions'].append(committee_motion)
    		itemResult.append(item)		

    	return itemResult			
    					