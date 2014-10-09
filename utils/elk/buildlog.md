## build log

Thu Oct  9 17:03:22 CST 2014

build y12docker/g0v-voter-guide:0.0.1

```
$ bash gc2mt.sh -t
$ bash gc2mt.sh -u y12docker/g0v-voter-guide:0.0.1
$ sudo docker images | grep voter
y12docker/g0v-voter-guide   0.0.1               7a5239e7fd94        22 seconds ago      1.2 GB
y12docker/g0v-voter-guide   test                6932227495c8        6 minutes ago       1.195 GB
$ sudo docker push y12docker/g0v-voter-guide:0.0.1

```


Tue Oct  7 18:43:18 CST 2014

rebuild from y12docker/estw:0.0.1

```
$ bash gc2mt.sh -t

```



Tue Oct  7 12:10:28 CST 2014

x['id'] = u"%s-%s-%s" % (x['name'],x['county'],x['election_year'])

```
$ curl http://192.168.2.73:9200/g0v-voter-guide/councilors/陳世榮-新北市-2010/
$ curl http://192.168.2.73:9200/g0v-voter-guide/councilors/陳世榮-新北市-2010/_termvector


$ curl 'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:治安&_source_include=platform'
hits.total = 52

$ curl 'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:兒童&_source_include=platform'
hits.total = 22

http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:(兒童 兒少)&_source_include=platform
hits.total = 23

$ curl 'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:(兒童 治安)&_source_include=platform'
hits.total = 66

$ curl  'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:治安 AND county:臺中市&_source_include=platform'
hits.total = 23

$ curl  'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:治安 AND county:新北市&_source_include=platform'
hits.total = 18

$ curl -XPOST 'http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?pretty=true&_source=false' -d '
{
    "query" : {
        "terms" : {"platform" : [ "治安" ]}
    },
    "aggs" : {
        "countys" : {
            "terms" : { "field" : "county" }
        }
    }
}

{
    "aggs" : {
        "countys" : {
            "terms" : { "field" : "county" }
        }
    }
}
'

  "aggregations" : {
    "countys" : {
      "buckets" : [ {
        "key" : "臺中市",
        "doc_count" : 23
      }, {
        "key" : "新北市",
        "doc_count" : 18
      }, {
        "key" : "臺北市",
        "doc_count" : 11
      } ]
    }
  }


```

Mon Oct  6 19:48:04 CST 2014

* push y12docker/estw:0.0.1

```
$ cd utils/elk
$ bash gc2mt.sh -t
$ curl http://docker_host:9200/g0v-voter-guide/councilors/_count
{"count":185,"_shards":{"total":5,"successful":5,"failed":0}}

$ curl http://192.168.2.73:9200/g0v-voter-guide/councilors/_search?q=platform:中港路

```

## Test Chinese Analysis Tokenizer

v141002

[Language Analyzers](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html)

```
$ bash gc2mt.sh -t
$ curl -XGET 'http://docker_host:9200/_analyze?pretty=true&analyzer=standard' \
  -d '三峽河龍埔里河堤外工程施工導致河流改道，造成對岸(介壽里)土地流失'

 {
  "tokens" : [ {
    "token" : "三",
    "start_offset" : 0,
    "end_offset" : 1,
    "type" : "<IDEOGRAPHIC>",
    "position" : 1
  }, {
    "token" : "峽",
    "start_offset" : 1,
    "end_offset" : 2,
    "type" : "<IDEOGRAPHIC>",
    "position" : 2
  }, {
    "token" : "河",
    "start_offset" : 2,
    "end_offset" : 3,
    "type" : "<IDEOGRAPHIC>",
    "position" : 3
  }, {
    "token" : "龍",
    "start_offset" : 3,
    "end_offset" : 4,
    "type" : "<IDEOGRAPHIC>",
    "position" : 4
  }, {
    "token" : "埔",
    "start_offset" : 4,
    "end_offset" : 5,
    "type" : "<IDEOGRAPHIC>",
    "position" : 5
  }, {
    "token" : "里",
    "start_offset" : 5,
    "end_offset" : 6,
    "type" : "<IDEOGRAPHIC>",
    "position" : 6
  }, {
    "token" : "河",
    "start_offset" : 6,
    "end_offset" : 7,
    "type" : "<IDEOGRAPHIC>",
    "position" : 7
  }, {
    "token" : "堤",
    "start_offset" : 7,
    "end_offset" : 8,
    "type" : "<IDEOGRAPHIC>",
    "position" : 8
  }, {
    "token" : "外",
    "start_offset" : 8,
    "end_offset" : 9,
    "type" : "<IDEOGRAPHIC>",
    "position" : 9
  }, {
    "token" : "工",
    "start_offset" : 9,
    "end_offset" : 10,
    "type" : "<IDEOGRAPHIC>",
    "position" : 10
  }, {
    "token" : "程",
    "start_offset" : 10,
    "end_offset" : 11,
    "type" : "<IDEOGRAPHIC>",
    "position" : 11
  }, {
    "token" : "施",
    "start_offset" : 11,
    "end_offset" : 12,
    "type" : "<IDEOGRAPHIC>",
    "position" : 12
  }, {
    "token" : "工",
    "start_offset" : 12,
    "end_offset" : 13,
    "type" : "<IDEOGRAPHIC>",
    "position" : 13
  }, {
    "token" : "導",
    "start_offset" : 13,
    "end_offset" : 14,
    "type" : "<IDEOGRAPHIC>",
    "position" : 14
  }, {
    "token" : "致",
    "start_offset" : 14,
    "end_offset" : 15,
    "type" : "<IDEOGRAPHIC>",
    "position" : 15
  }, {
    "token" : "河",
    "start_offset" : 15,
    "end_offset" : 16,
    "type" : "<IDEOGRAPHIC>",
    "position" : 16
  }, {
    "token" : "流",
    "start_offset" : 16,
    "end_offset" : 17,
    "type" : "<IDEOGRAPHIC>",
    "position" : 17
  }, {
    "token" : "改",
    "start_offset" : 17,
    "end_offset" : 18,
    "type" : "<IDEOGRAPHIC>",
    "position" : 18
  }, {
    "token" : "道",
    "start_offset" : 18,
    "end_offset" : 19,
    "type" : "<IDEOGRAPHIC>",
    "position" : 19
  }, {
    "token" : "造",
    "start_offset" : 20,
    "end_offset" : 21,
    "type" : "<IDEOGRAPHIC>",
    "position" : 20
  }, {
    "token" : "成",
    "start_offset" : 21,
    "end_offset" : 22,
    "type" : "<IDEOGRAPHIC>",
    "position" : 21
  }, {
    "token" : "對",
    "start_offset" : 22,
    "end_offset" : 23,
    "type" : "<IDEOGRAPHIC>",
    "position" : 22
  }, {
    "token" : "岸",
    "start_offset" : 23,
    "end_offset" : 24,
    "type" : "<IDEOGRAPHIC>",
    "position" : 23
  }, {
    "token" : "介",
    "start_offset" : 25,
    "end_offset" : 26,
    "type" : "<IDEOGRAPHIC>",
    "position" : 24
  }, {
    "token" : "壽",
    "start_offset" : 26,
    "end_offset" : 27,
    "type" : "<IDEOGRAPHIC>",
    "position" : 25
  }, {
    "token" : "里",
    "start_offset" : 27,
    "end_offset" : 28,
    "type" : "<IDEOGRAPHIC>",
    "position" : 26
  }, {
    "token" : "土",
    "start_offset" : 29,
    "end_offset" : 30,
    "type" : "<IDEOGRAPHIC>",
    "position" : 27
  }, {
    "token" : "地",
    "start_offset" : 30,
    "end_offset" : 31,
    "type" : "<IDEOGRAPHIC>",
    "position" : 28
  }, {
    "token" : "流",
    "start_offset" : 31,
    "end_offset" : 32,
    "type" : "<IDEOGRAPHIC>",
    "position" : 29
  }, {
    "token" : "失",
    "start_offset" : 32,
    "end_offset" : 33,
    "type" : "<IDEOGRAPHIC>",
    "position" : 30
  } ]
}
```

analyzer=chinese

```
$ curl -XGET 'http://docker_host:9200/_analyze?pretty=true&analyzer=chinese' \
  -d '三峽河龍埔里河堤外工程施工  致河流改道，造成對岸(介壽里)土地流失'
{
  "tokens" : [ {
    "token" : "三",
    "start_offset" : 0,
    "end_offset" : 1,
    "type" : "word",
    "position" : 1
  }, {
    "token" : "峽",
    "start_offset" : 1,
    "end_offset" : 2,
    "type" : "word",
    "position" : 2
  }, {
    "token" : "河",
    "start_offset" : 2,
    "end_offset" : 3,
    "type" : "word",
    "position" : 3
  }, {
    "token" : "龍",
    "start_offset" : 3,
    "end_offset" : 4,
    "type" : "word",
    "position" : 4
  }, {
    "token" : "埔",
    "start_offset" : 4,
    "end_offset" : 5,
    "type" : "word",
    "position" : 5
  }, {
    "token" : "里",
    "start_offset" : 5,
    "end_offset" : 6,
    "type" : "word",
    "position" : 6
  }, {
    "token" : "河",
    "start_offset" : 6,
    "end_offset" : 7,
    "type" : "word",
    "position" : 7
  }, {
    "token" : "堤",
    "start_offset" : 7,
    "end_offset" : 8,
    "type" : "word",
    "position" : 8
  }, {
    "token" : "外",
    "start_offset" : 8,
    "end_offset" : 9,
    "type" : "word",
    "position" : 9
  }, {
    "token" : "工",
    "start_offset" : 9,
    "end_offset" : 10,
    "type" : "word",
    "position" : 10
  }, {
    "token" : "程",
    "start_offset" : 10,
    "end_offset" : 11,
    "type" : "word",
    "position" : 11
  }, {
    "token" : "施",
    "start_offset" : 11,
    "end_offset" : 12,
    "type" : "word",
    "position" : 12
  }, {
    "token" : "工",
    "start_offset" : 12,
    "end_offset" : 13,
    "type" : "word",
    "position" : 13
  }, {
    "token" : "導",
    "start_offset" : 13,
    "end_offset" : 14,
    "type" : "word",
    "position" : 14
  }, {
    "token" : "致",
    "start_offset" : 14,
    "end_offset" : 15,
    "type" : "word",
    "position" : 15
  }, {
    "token" : "河",
    "start_offset" : 15,
    "end_offset" : 16,
    "type" : "word",
    "position" : 16
  }, {
    "token" : "流",
    "start_offset" : 16,
    "end_offset" : 17,
    "type" : "word",
    "position" : 17
  }, {
    "token" : "改",
    "start_offset" : 17,
    "end_offset" : 18,
    "type" : "word",
    "position" : 18
  }, {
    "token" : "道",
    "start_offset" : 18,
    "end_offset" : 19,
    "type" : "word",
    "position" : 19
  }, {
    "token" : "造",
    "start_offset" : 20,
    "end_offset" : 21,
    "type" : "word",
    "position" : 20
  }, {
    "token" : "成",
    "start_offset" : 21,
    "end_offset" : 22,
    "type" : "word",
    "position" : 21
  }, {
    "token" : "對",
    "start_offset" : 22,
    "end_offset" : 23,
    "type" : "word",
    "position" : 22
  }, {
    "token" : "岸",
    "start_offset" : 23,
    "end_offset" : 24,
    "type" : "word",
    "position" : 23
  }, {
    "token" : "介",
    "start_offset" : 25,
    "end_offset" : 26,
    "type" : "word",
    "position" : 24
  }, {
    "token" : "壽",
    "start_offset" : 26,
    "end_offset" : 27,
    "type" : "word",
    "position" : 25
  }, {
    "token" : "里",
    "start_offset" : 27,
    "end_offset" : 28,
    "type" : "word",
    "position" : 26
  }, {
    "token" : "土",
    "start_offset" : 29,
    "end_offset" : 30,
    "type" : "word",
    "position" : 27
  }, {
    "token" : "地",
    "start_offset" : 30,
    "end_offset" : 31,
    "type" : "word",
    "position" : 28
  }, {
    "token" : "流",
    "start_offset" : 31,
    "end_offset" : 32,
    "type" : "word",
    "position" : 29
  }, {
    "token" : "失",
    "start_offset" : 32,
    "end_offset" : 33,
    "type" : "word",
    "position" : 30
  } ]
}

```

analyezer=cjk

```
$ curl -XGET 'http://docker_host:9200/_analyze?pretty=true&analyzer=cjk' \
  -d '三峽河龍埔里河堤外工程施工導致  流改道，造成對岸(介壽里)土地流失'
{
  "tokens" : [ {
    "token" : "三峽",
    "start_offset" : 0,
    "end_offset" : 2,
    "type" : "<DOUBLE>",
    "position" : 1
  }, {
    "token" : "峽河",
    "start_offset" : 1,
    "end_offset" : 3,
    "type" : "<DOUBLE>",
    "position" : 2
  }, {
    "token" : "河龍",
    "start_offset" : 2,
    "end_offset" : 4,
    "type" : "<DOUBLE>",
    "position" : 3
  }, {
    "token" : "龍埔",
    "start_offset" : 3,
    "end_offset" : 5,
    "type" : "<DOUBLE>",
    "position" : 4
  }, {
    "token" : "埔里",
    "start_offset" : 4,
    "end_offset" : 6,
    "type" : "<DOUBLE>",
    "position" : 5
  }, {
    "token" : "里河",
    "start_offset" : 5,
    "end_offset" : 7,
    "type" : "<DOUBLE>",
    "position" : 6
  }, {
    "token" : "河堤",
    "start_offset" : 6,
    "end_offset" : 8,
    "type" : "<DOUBLE>",
    "position" : 7
  }, {
    "token" : "堤外",
    "start_offset" : 7,
    "end_offset" : 9,
    "type" : "<DOUBLE>",
    "position" : 8
  }, {
    "token" : "外工",
    "start_offset" : 8,
    "end_offset" : 10,
    "type" : "<DOUBLE>",
    "position" : 9
  }, {
    "token" : "工程",
    "start_offset" : 9,
    "end_offset" : 11,
    "type" : "<DOUBLE>",
    "position" : 10
  }, {
    "token" : "程施",
    "start_offset" : 10,
    "end_offset" : 12,
    "type" : "<DOUBLE>",
    "position" : 11
  }, {
    "token" : "施工",
    "start_offset" : 11,
    "end_offset" : 13,
    "type" : "<DOUBLE>",
    "position" : 12
  }, {
    "token" : "工導",
    "start_offset" : 12,
    "end_offset" : 14,
    "type" : "<DOUBLE>",
    "position" : 13
  }, {
    "token" : "導致",
    "start_offset" : 13,
    "end_offset" : 15,
    "type" : "<DOUBLE>",
    "position" : 14
  }, {
    "token" : "致河",
    "start_offset" : 14,
    "end_offset" : 16,
    "type" : "<DOUBLE>",
    "position" : 15
  }, {
    "token" : "河流",
    "start_offset" : 15,
    "end_offset" : 17,
    "type" : "<DOUBLE>",
    "position" : 16
  }, {
    "token" : "流改",
    "start_offset" : 16,
    "end_offset" : 18,
    "type" : "<DOUBLE>",
    "position" : 17
  }, {
    "token" : "改道",
    "start_offset" : 17,
    "end_offset" : 19,
    "type" : "<DOUBLE>",
    "position" : 18
  }, {
    "token" : "造成",
    "start_offset" : 20,
    "end_offset" : 22,
    "type" : "<DOUBLE>",
    "position" : 19
  }, {
    "token" : "成對",
    "start_offset" : 21,
    "end_offset" : 23,
    "type" : "<DOUBLE>",
    "position" : 20
  }, {
    "token" : "對岸",
    "start_offset" : 22,
    "end_offset" : 24,
    "type" : "<DOUBLE>",
    "position" : 21
  }, {
    "token" : "介壽",
    "start_offset" : 25,
    "end_offset" : 27,
    "type" : "<DOUBLE>",
    "position" : 22
  }, {
    "token" : "壽里",
    "start_offset" : 26,
    "end_offset" : 28,
    "type" : "<DOUBLE>",
    "position" : 23
  }, {
    "token" : "土地",
    "start_offset" : 29,
    "end_offset" : 31,
    "type" : "<DOUBLE>",
    "position" : 24
  }, {
    "token" : "地流",
    "start_offset" : 30,
    "end_offset" : 32,
    "type" : "<DOUBLE>",
    "position" : 25
  }, {
    "token" : "流失",
    "start_offset" : 31,
    "end_offset" : 33,
    "type" : "<DOUBLE>",
    "position" : 26
  } ]
}
```
