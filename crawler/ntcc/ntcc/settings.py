# -*- coding: utf-8 -*-

# Scrapy settings for ntcc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ntcc'

SPIDER_MODULES = ['ntcc.spiders']
NEWSPIDER_MODULE = 'ntcc.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ntcc (+http://www.yourdomain.com)'
#ITEM_PIPELINES = {
#        'ntcc.pipelines.NtccPipeline': 100
#        }
