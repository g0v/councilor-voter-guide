#! /usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import Json

def con():
    psycopg2.extensions.register_adapter(dict, Json)
    psycopg2.extensions.register_adapter(list, Json)
    conn = psycopg2.connect(dbname='councilor', host='localhost', user='postgres', password='postgres')
    return conn
