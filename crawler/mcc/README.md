```
scrapy runspider councilors.py -o ../../data/mcc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/mcc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/mcc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/mcc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
