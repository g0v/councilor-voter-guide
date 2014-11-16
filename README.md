councilor-voter-guide 
================

[議員投票指南](http://councils.g0v.tw/)        
[Hackpad 開發討論區](https://g0v.hackpad.com/KjfdRZ08FZ3)       
[Hackpad 意見回饋](https://g0v.hackpad.com/--5PNuk4XGGrj)

## Project Layout Introduce

-   crawler  
    各縣市議會的crawler，各crawler名稱與功用如下：  
    > councilors: 現任議員資料  
    > councilors_terms: 歷屆議員資料（不一定包含現任的資料）  
    > bills: 議案資料  
    > meeting_minutes: 議事錄資料（開會出缺席、表決）
    
-   data  
    由上述crawler產出的各縣市原始JSON
    > util/prettyjson.py: 產出indent好讀版的JSON, [README](https://github.com/g0v/councilor-voter-guide/tree/master/utils)  
    > pretty_format: 放置上述產出的各縣市好讀版JSON  
    > hashlist_meeting_minutes-v141001.json: links map, 存放由meeting_minutes cralwer抓下的binaries [detail](https://github.com/g0v/councilor-voter-guide/tree/master/utils/bin-hash)  
    > candidates_2014.xlsx: 中選會公告的議員候選人  

-   parser  
    將上述data下的JSON標準化後放入database（如果你只是需要完整的database，可直接跳至[Restore DB](https://github.com/g0v/councilor-voter-guide#restore-data-into-database)） 
    > councilors/councilors.py: 處理現任和歷屆議員資料  
    > councilors/candidates.py: 處理候選人資料  
    > bills/bills.py: 處理議案資料   
    > votes/: 出缺席、表決資料，各縣市、各屆分開處理  

-   voter\_guide  
    Web application using Django, [Enviroment Setup](https://github.com/g0v/councilor-voter-guide#for-website-pythondjango)
      
In Ubuntu 12.04 LTS
=================
## For Crawler (Scrapy 0.24.4)

[Scrapy offcial install doc](http://doc.scrapy.org/en/latest/intro/install.html)
```
sudo apt-get install libxml2-dev libxslt1-dev python-dev libffi-dev python-pip
sudo pip install lxml
sudo pip install Scrapy
sudo pip install requests
```
After install scrapy, you can run commands to test, below using tcc(臺北市議會) for example:
```
cd crawler/tcc
scrapy crawl bills
scrapy crawl councilors
scrapy crawl councilors_terms
scrapy crawl meeting
```
If you want to output json file:
```
cd crawler/tcc
scrapy crawl bills -o bills.json -t json
scrapy crawl councilors -o bills.json -t json
scrapy crawl councilors_terms -o bills.json -t json
scrapy crawl meeting -o bills.json -t json
```

## For Website (Python/Django)

install basic tools
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
sudo apt-get install git python-pip python-dev python-setuptools postgresql libpq-dev
sudo easy_install virtualenv
```

## Clone source code from GitHub to local

It is quite big now. please be patient. don't use command like git --depth
```
git clone https://github.com/g0v/councilor-voter-guide.git       
cd councilor-voter-guide/voter_guide/
```

## Start virtualenv and install packages         
(if you don' mind packages installed into your local environment, just `pip install -r requirements.txt`)
```
virtualenv --no-site-packages venv      
source venv/bin/activate        
pip install -r requirements.txt     
```

## Load Data to your database

We use SQLite as the default database, if you want to use another database, please set your database engine in local_settings.py.

## Create Table & restore data

Create Table

``` 
python manage.py syncdb --noinput 
```

This step may take some time, be patient.

```
python manage.py loaddata db.json
```

## Dumpdata 

```
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

## runserver
```
python manage.py runserver
```
Now you should able to see the web page at http://localhost:8000        


## Mac Related Instructions

###Prepare Compiler

There are some python package written in C or C++ such as lxml. so a compiler is required. you can install a compiler via the following command:

```bash
xcode-select --install
```



###Prepare PostgreSQL

You can install the packaged app [here](http://postgresapp.com).
put the app in your Application folder and click it to start. 

And please add the following line to your ~/.bash_profile

```bash
export PATH=/Applications/Postgres.app/Contents/Versions/9.3/bin/:$PATH

```

please change the version number 9.3 if you download a different version of PostgreSQL. 

after you add the PATH environment variable, source it. 

```bash
source ~/.bash_profile
```

if you don't add the PATH variable, installation of psycopg2 will not success. 

## Web Docker [c3h3 / g0v-cvg-web](https://registry.hub.docker.com/u/c3h3/g0v-cvg-web/)
## How to use this images

### First Step: Download and Extract pgdata 

```
git clone https://github.com/c3h3/g0v-cvg-pgdata.git && cd g0v-cvg-pgdata && tar xfzv 47821274c242ce68f2d8d18d4bb0d050d6481311.tar.gz
```
- After that, you will get pgdata dir. 
- Assume pgdata's absolute path is "your_pgdata"
 

### Second Step: RUN postgres with pgdata

```
docker run --name pgdb -v your_pgdata:/var/lib/postgresql/data postgres:9.3
```

If you want to use pgadmin connect with your db, you could also forwarding the port out ... with command ...

```
docker run --name pgdb -p 5432:5432 -v your_pgdata:/var/lib/postgresql/data postgres:9.3
```

- "your_pgdata" is pgdata's absolute path in previous step.


### Third Step: RUN web linked with pgdb

```
docker run --name g0v-cvg-web --link pgdb:postgres -p port_on_host:8000 -d c3h3/g0v-cvg-web
```
- "port_on_host" is the port forwarding out to your host, which you could find your web on http://localhost:port_on_host


## Crawler Docker [c3h3 / g0v-cvg-crawler](https://registry.hub.docker.com/u/c3h3/g0v-cvg-crawler/)


## How to use this images

### Run Scarpy Server:

```
docker run --name g0v -p forward_port:6800 -v outside_items:/items -v outside_logs:/logs -d c3h3/g0v-cvg-crawler
```
- "forward_port" is the port you want to forward into docker image (EXPOSE 6800)
- "outside_items" is the directory you want to mount into docker image as /items 
- "outside_logs" is the directory you want to mount into docker image as /logs 

### Link Scarpy Server for Deploy and Submit Job:

```
docker run --link g0v:g0v -it c3h3/g0v-cvg-crawler /bin/bash
```

### Example of Deploy ttc:

in a running docker instance which linked with g0v (Scarpy Server), you can use the following command to deploy tcc crawler to server:

```
cd /tmp/g0v-cvg/crawler/tcc && python deploy.py
```

### Example of Crawl ttc.bills :

in a running docker instance which linked with g0v (Scarpy Server), you can use the following command to deploy tcc crawler to server:

```
cd /tmp/g0v-cvg/crawler/bin && python crawl_tcc_bills.py
```




CC0 1.0 Universal
=================
CC0 1.0 Universal       
This work is published from Taiwan.     
