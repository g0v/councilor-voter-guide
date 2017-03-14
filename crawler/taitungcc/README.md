```
scrapy runspider councilors.py -o ../../data/taitungcc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/taitungcc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/taitungcc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/taitungcc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
