parser
================

## Layout

| folder      | script                     | remark                                           |
|-------------|----------------------------|--------------------------------------------------|
| councilors  | councilors.py              | 議員基本資料                                     |
|             | political\_contribution.py | 議員的政治獻金                                   |
|             | candidates.py              | 候選人，如當過議員會作連結，所以需先有議員資料   |
| bills       | bills.py                   | 議案，如為議員提出的會作連結，所以需先有議員資料 |
| suggestions | suggestions.py             | 議員配合款，會與議員作連結，所以需先有議員資料   |
| votes       | \*/votes.py                | 出缺席和表決，會與議員作連結，所以需先有議員資料 |
|             | file2txt.py                | 會議記錄轉為純文字                               |

## Restore data into database       
Please new a database(eg. voter\_guide), below will use voter\_guide for example
```
createdb -h localhost -U <username> voter_guide
cd councilor-voter-guide/voter_guide/
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <username> -d voter_guide local_db.dump
```

## Database setting          
create and edit db_settings.py in councilor-voter-guide/parser/ to configing your database parameter(notice **dbname**,
**username** and **password**       
```
# db_settings.py
import psycopg2
from psycopg2.extras import Json

def con():
    psycopg2.extensions.register_adapter(dict, Json)
    psycopg2.extensions.register_adapter(list, Json)
    conn = psycopg2.connect(dbname='voter_guide', host='localhost', user='username', password='password')
    return conn
```
Because db_settings.py is list in .gitignore, so this file won't be appear in source control, for safety.
