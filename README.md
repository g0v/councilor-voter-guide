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
apt-get install libxml2-dev libxslt1-dev python-dev libffi-dev
pip install lxml
pip install Scrapy
pip install requests
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

0.1 install basic tools
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
sudo apt-get install git python-pip python-dev python-setuptools postgresql libpq-dev
easy_install virtualenv
```

0.2 set a password in your database(If you already have one, just skip this step)        
(you can use `whoami` to check your username, notice **&lt;username&gt;**  below, please replace with your own)

```
sudo -u <username> psql -c "ALTER USER <username> with encrypted PASSWORD 'put_your_password_here';"
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
cd voter_guide
virtualenv --no-site-packages venv      
source venv/bin/activate        
pip install -r requirements.txt     
```

## Restore data into database       
Please new a database(eg. voter_guide), below will use voter_guide for example
```
createdb -h localhost -U <username> voter_guide
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <username> -d voter_guide local_db.dump
```

## Django settings.py          
create and edit local_settings.py in councilor-voter-guide/voter_guide/voter_guide/ to configing your database parameter(notice **USER**, **PASSWORD** below) and **SECRET_KEY**
See [Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/) or maybe use [online generator](http://www.miniwebtool.com/django-secret-key-generator/) to get SECRET_KEY for convenience				
```
SECRET_KEY = '' # put random string inside and don't share it with anybody.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'voter_guide', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
```
Because local_settings.py is list in .gitignore, so this file won't be appear in source control, for safety.

## runserver
```
python manage.py runserver
```
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


CC0 1.0 Universal
=================
CC0 1.0 Universal       
This work is published from Taiwan.     
