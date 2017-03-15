```
scrapy runspider councilors.py -o ../../data/phcouncil/councilors.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider councilors_terms.py -o ../../data/phcouncil/councilors_terms.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider bills.py -o ../../data/phcouncil/bills.json -s FEED_EXPORT_ENCODING=utf-8
scrapy runspider meeting_minutes.py -o ../../data/phcouncil/meeting_minutes.json -s FEED_EXPORT_ENCODING=utf-8
```
