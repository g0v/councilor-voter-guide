# Scrapy settings for taipei project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kcc'

SPIDER_MODULES = ['kcc.spiders']
NEWSPIDER_MODULE = 'kcc.spiders'
LOG_FILE = 'log.txt'
REDIRECT_ENABLED = False
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 302]
COOKIES_ENABLED = False
COOKIES_DEBUG = True
DUPEFILTER_DEBUG = True
#DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taipei (+http://www.yourdomain.com)'
