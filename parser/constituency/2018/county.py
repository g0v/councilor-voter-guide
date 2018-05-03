#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import codecs
import scrapy
import subprocess


#cmd = 'wget -Nc "http://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=72874C55-884D-4CEA-B7D6-F60B0BE85AB0" -O county.zip'
#subprocess.call(cmd, shell=True)
#cmd = "unzip -l county.zip | awk '/.zip/{print $4}'"
#zip_file = subprocess.check_output(cmd, shell=True).strip()
#cmd = 'unzip county.zip'
#subprocess.call(cmd, shell=True)

import fiona
import fiona.crs


f_in = 'COUNTY_MOI_1070330.shp'
f_out = 'county.json'

def convert(f_in, f_out):
    with fiona.open(f_in, 'r',
            driver='ESRI Shapefile',
            encoding='Big5') as source:
        with fiona.open(
                f_out,
                'w',
                driver='GeoJSON',
                schema=source.schema,
                encoding='utf-8') as sink:

            for rec in source:
                sink.write(rec)

convert(f_in, f_out)
