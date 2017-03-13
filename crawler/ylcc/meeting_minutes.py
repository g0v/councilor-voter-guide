# -*- coding: utf-8 -*-
import scrapy
import time
import re
import os
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ylcc.items import MeetingMinutes
from crawler_lib import misc


class Spider(scrapy.Spider):
	name = "meeting"
	#allowed_domains = ["www.ylcc.gov.tw/index.php"]
	base_url = "http://www.ylcc.gov.tw"
	start_urls = [
		"http://www.ylcc.gov.tw/index.php?parent=201010080000097&inner=dload&menu=201008030000001",
		"http://www.ylcc.gov.tw/index.php?parent=201010080000098&keyword=&page=&inner=dload&menu=201008030000001"
	]
	download_delay = 0.5
	script_path = os.path.dirname(os.path.abspath(__file__))

	def parse(self, response):
		sel = Selector(response)
		for node in sel.xpath('//table//td/a[@class="link_dload2"]'):
			# exclude href with empty parent parameter
			url = node.xpath('@href').extract()[0]
			href_check = re.match(".*parent=(\d+)&.*", url)
			if (href_check):
				sitting_url = '%s/%s' % (self.base_url, url)
				yield Request(sitting_url, callback=self.parse_profile)
			else:
				print " %s not matched" % node.extract()


	def parse_profile(self, response):
		item = MeetingMinutes()
		sel = Selector(response)
		bill_url = sel.xpath(u'//table//td/a[contains(text(), "議員提案一覽表")]/@href').extract()
		if (bill_url):
			sitting = sel.xpath(u'//table/tr/td[@class="bg_dload" and @valign="middle"]/span[contains(text(),"第")]/text()').extract()
			# download bill
			download_url = '%s/%s' % (self.base_url, bill_url[0])
			filename = os.path.basename(bill_url[0])

			if re.search(u"定期會", sitting[0]):
				save_dir = self.script_path + '/../meeting_minutes/session/'
			else:
				save_dir = self.script_path + '/../meeting_minutes/extra_session/'

			file_path = save_dir + filename
			if not os.path.exists(save_dir):
				os.mkdir(save_dir)
			result = misc.download(download_url, file_path)
			if not result['skipped']:
				time.sleep(1)

			item['county'] = u'雲林縣'
			item['sitting'] = sitting[0]
			item['category'] = ''
			item['date'] = ''
			item['meeting'] = ''
			item['download_url'] = download_url
			yield item


