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


def convert(f_in, f_out='regional-councilors-constituencies-2014.geojson', filter=None):
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

            if filter:
                for rec in source:
                    if rec['properties']['COUNTYNAME'] == filter:
                        sink.write(rec)
            else:
                sink.write(rec)

def get_counties(f_in):
    with fiona.open(
            f_in,
            'r',
            driver='ESRI Shapefile',
            crs=fiona.crs.from_epsg(4326),
            encoding='utf-8') as source:
        return list({rec['properties']['COUNTYNAME'] for rec in source})

f_in = 'county-regional-constituencies.shp'
for county in get_counties(f_in):
    print county
    f_out = u'geojson/regional-councilors-constituencies-2014-%s.geojson' % county
    f_js_out = u'../../../voter_guide/static/js/regional-councilors-constituencies-2014-%s.js' % county
    if not os.path.isfile(f_out):
        convert(f_in, f_out, county)
    from_file = open(f_out)
    line = from_file.readline()
    line = 'var geodata = {'
    to_file = open(f_js_out, 'w')
    to_file.write(line)
    shutil.copyfileobj(from_file, to_file)
