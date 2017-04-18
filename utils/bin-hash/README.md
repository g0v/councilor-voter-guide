Run

```
$ git clone --depth 1 https://github.com/g0v/councilor-voter-guide
$ cd councilor-voter-guide
$ python utils/bin-hash/binhash.py -i meeting_minutes -w "http://0.y12.tw/g0v/councilor-voter-guide/" \
  > data/hashlist_meeting_minutes-v141001.json
$ HOST_PATH=$(cat data/hashlist_meeting_minutes-v141001.json | python -c 'import json,sys;o=json.load(sys.stdin);print o["host_path"]')
$ echo $HOST_PATH
$ curl $HOST_PATH
```

Test 

```
$ cd utils/bin-hash
$ nosetests
``
