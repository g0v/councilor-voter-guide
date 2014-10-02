
## prettyjson.py

print the pretty json stdout

```
$ cd crawler/tccc
$ scrapy crawl councilors -o /tmp/test.json
$ python ../../utils/prettyjson.py /tmp/test.json
```

print the item[3] pretty json stdout

```
$ python ../../utils/prettyjson.py /tmp/test.json 3
```

save the pretty json file

```
$ python ../../utils/prettyjson.py /tmp/test.json /tmp/pretty.json
```