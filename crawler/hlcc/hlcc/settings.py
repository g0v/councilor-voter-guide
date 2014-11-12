# -*- coding: utf-8 -*-

# Scrapy settings for hlcc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys
from os.path import dirname


# add python path for crawler_lib
_PROJECT_PATH = dirname(dirname(dirname(dirname(__file__))))
sys.path.append(os.path.join(_PROJECT_PATH, 'crawler'))

BOT_NAME = 'hlcc'

SPIDER_MODULES = ['hlcc.spiders']
NEWSPIDER_MODULE = 'hlcc.spiders'
LOG_FILE = 'log.txt'

FEED_EXPORTERS = {
    'json': 'crawler_lib.misc.UnicodeJsonItemExporter',
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hlcc (+http://www.yourdomain.com)'
