## Elasticsearch

Service

* kibana http://docker_host:8080/
* [plugin] elastic HQ http://docker_host:9200/_plugin/HQ/
* [plugin] elastic Head http://docker_host:9200/_plugin/head/


## RUN a prebuild image

Prerequirements :

* [boot2docker for OS X and Windows](https://github.com/boot2docker/boot2docker)
* [docker/docker](https://github.com/docker/docker)

[y12docker/g0v-voter-guide Repository | Docker Hub Registry - Repositories of Docker Images](https://registry.hub.docker.com/u/y12docker/g0v-voter-guide/)

Notice : the download of y12docker/g0v-voter-guide is a very large file size (1~Gb).

```
$ sudo docker pull y12docker/g0v-voter-guide:0.0.1
$ sudo docker run -p 8080:8080 -p 9200:9200 -d y12docker/g0v-voter-guide:v141002
```


## Elasticsearch Query

```
$ cd utils/elk
$ curl -XGET 'http://es_host:9200/g0v-voter-guide/councilors/_search' \
  -d '{"query":{"query_string":{"query":"county:(新北市 OR 臺中市) AND name:陳*" }}}' | python ../prettyjson.py | more
```

## Build a prebuild image

Prerequirements :

* [boot2docker for OS X and Windows](https://github.com/boot2docker/boot2docker)
* [docker/docker](https://github.com/docker/docker)
* [jpetazzo/nsenter](https://github.com/jpetazzo/nsenter)

BUILD

```
$ cd utils/elk
$ bash gc2mt.sh -t
$ docker ps
$ bash gc2mt.sh -u testimage:v1
$ bash gc2mt.sh -s
```

RUN

```
$ docker run -p 8080:8080 -p 9200:9200 -d testimage:v1
```
