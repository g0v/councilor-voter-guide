# -*- coding: utf-8 -*-

# Scrapy settings for hcc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
from os.path import dirname

_PROJECT_PATH = dirname(dirname(dirname(dirname(__file__))))
sys.path.append(os.path.join(_PROJECT_PATH, 'crawler'))

BOT_NAME = 'hcc'

SPIDER_MODULES = ['hcc.spiders']
NEWSPIDER_MODULE = 'hcc.spiders'
LOG_FILE = 'log.txt'

FEED_EXPORTERS = {
    'json': 'crawler_lib.misc.UnicodeJsonItemExporter',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hcc (+http://www.yourdomain.com)'
