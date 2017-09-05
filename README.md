councilor-voter-guide 
================

[議員投票指南](http://councils.g0v.tw/)        
[文件](http://beta.hackfoldr.org/voter_guide_tw)       

## Project Layout

-   crawler  
    各縣市議會的crawler：[doc](https://github.com/g0v/councilor-voter-guide/tree/master/crawler)
    
-   data  
    由上述crawler產出的各縣市原始JSON
    > hashlist_meeting_minutes-v141001.json: links map, 存放由meeting_minutes cralwer抓下的binaries [detail](https://github.com/g0v/councilor-voter-guide/tree/master/utils/bin-hash)  
    > candidates_2014.xlsx: 中選會公告的議員候選人  
    > cand-moi-direct-control-2018.json: [直轄市議員](http://cand.moi.gov.tw)  
    > cand-moi-county-control-2018.json: [縣市議員](http://cand.moi.gov.tw)  
    > T1.csv: [2014中選會釋出資料](https://github.com/ronnywang/vote2014/blob/master/webdata/data/T1.csv)  
    > [議員選後消失去哪了](https://docs.google.com/spreadsheets/d/1ohhFgdHrxFZPcM7J-RqUskgZX2zqpYoxufNnX8VL4Os)  

-   parser  
    將上述data下的JSON標準化後放入database：[doc](https://github.com/g0v/councilor-voter-guide/tree/master/parser)

-   voter\_guide  
    Web application using Django, [Environment Setup](https://github.com/g0v/councilor-voter-guide#for-website-pythondjango)
      
In Ubuntu 14.04 LTS
=================
## Website (Python/Django)

0.1 install basic tools
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
sudo apt-get install git python-pip python-dev python-setuptools postgresql libpq-dev
sudo easy_install virtualenv
```

0.2 set a password in your database(If you already have one, just skip this step)


```
sudo -u <username> psql -c "ALTER USER <username> with encrypted PASSWORD 'put_your_password_here';"
```
e.g.
```
sudo -u postgres psql -c "ALTER USER postgres with encrypted PASSWORD 'my_password';"
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
. venv/bin/activate        
pip install -r requirements.txt     
```

## Create db & restore data

We use Postgres 9.5, please set your database config in voter\_guide/local\_settings.py.        
Please create a database(e.g. voter\_guide), below will use voter\_guide for example
```
createdb -h localhost -U <username> voter_guide
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <username> -d voter_guide local_db.dump
```

## runserver
```
python manage.py runserver
```
Now you should able to see the web page at http://localhost:8000        

## Dumpdata(optional) 

```
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

## Mac Related Instructions

### Prepare Compiler

There are some python package written in C or C++ such as lxml. so a compiler is required. you can install a compiler via the following command:

```bash
xcode-select --install
```

### Prepare PostgreSQL

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
