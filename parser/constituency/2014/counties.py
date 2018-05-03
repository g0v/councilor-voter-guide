#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import codecs
import scrapy
import shutil
import fiona
import fiona.crs


def convert(f_in, f_out, filter=None):
    with fiona.open(
            f_in,
            'r',
            driver='ESRI Shapefile',
            crs=fiona.crs.from_epsg(4326),
            encoding='utf-8') as source:
        with fiona.open(
                f_out,
                'w',
                driver='GeoJSON',
                crs = fiona.crs.from_epsg(3824),
                schema=source.schema,
                encoding='utf-8') as sink:

            for rec in source:
                if filter:
                    if rec['properties']['COUNTYNAME'] == filter:
                        sink.write(rec)
                else:
                    sink.write(rec)

f_in = 'counties.shp'
f_out = u'geojson/counties-2014.geojson'
f_js_out = u'../../../voter_guide/static/js/counties-2014.js'
if not os.path.isfile(f_out):
    convert(f_in, f_out)
from_file = open(f_out)
line = from_file.readline()
line = 'var geodata = {'
to_file = open(f_js_out, 'w')
to_file.write(line)
shutil.copyfileobj(from_file, to_file)
