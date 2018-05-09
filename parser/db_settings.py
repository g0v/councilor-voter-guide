#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import psycopg2
from psycopg2.extras import Json

def con():
    psycopg2.extensions.register_adapter(dict, Json)
    psycopg2.extensions.register_adapter(list, Json)
    conn = psycopg2.connect(dbname=os.getenv('COUNCIL_DATABASE_NAME', 'councilor'), host='localhost', user=os.getenv('DATABASE_USER', 'postgres'), password=os.getenv('DATABASE_PASSWORD', 'password'))
    return conn

def con_another():
    psycopg2.extensions.register_adapter(dict, Json)
    psycopg2.extensions.register_adapter(list, Json)
    conn = psycopg2.connect(dbname=os.getenv('LY_DATABASE_NAME', 'ly'), host='localhost', user=os.getenv('DATABASE_USER', 'postgres'), password=os.getenv('DATABASE_PASSWORD', 'password'))
    return conn
