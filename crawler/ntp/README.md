```
scrapy runspider suggestions.py -o ../../data/ntp/suggestions.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors.py -o ../../data/ntp/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/ntp/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/ntp/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/ntp/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
