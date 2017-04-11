```
scrapy runspider suggestions.py -o ../../data/cyscc/suggestions.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors.py -o ../../data/cyscc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/cyscc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/cyscc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/cyscc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
