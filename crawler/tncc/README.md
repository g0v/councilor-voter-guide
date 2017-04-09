```
scrapy runspider suggestions.py -o ../../data/tncc/suggestions.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors.py -o ../../data/tncc/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/tncc/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/tncc/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/tncc/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
