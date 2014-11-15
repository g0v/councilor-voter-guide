# -*- coding: utf-8 -*-

# Scrapy settings for cycc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
from os.path import dirname

BOT_NAME = 'cycc'

SPIDER_MODULES = ['cycc.spiders']
NEWSPIDER_MODULE = 'cycc.spiders'
_PROJECT_PATH = dirname(dirname(dirname(dirname(__file__))))
sys.path.append(os.path.join(_PROJECT_PATH, 'crawler'))


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cycc (+http://www.yourdomain.com)'
