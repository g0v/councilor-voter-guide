```
scrapy runspider suggestions.py -o ../../data/hlcc/suggestions.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors.py -o ../../data/hlcc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/hlcc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/hlcc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/hlcc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
