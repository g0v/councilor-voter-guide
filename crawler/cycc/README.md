```
scrapy runspider councilors.py -o ../../data/cycc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/cycc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/cycc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/cycc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
