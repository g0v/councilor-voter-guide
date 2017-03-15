```
scrapy runspider councilors.py -o ../../data/kmcc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/kmcc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/kmcc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/kmcc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
