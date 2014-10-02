import os
import subprocess
import urllib2
import requests
from scrapy.http import HtmlResponse, Request
from scrapy.utils.url import canonicalize_url
import json
from scrapy.contrib.exporter import BaseItemExporter, JsonLinesItemExporter, JsonItemExporter


def append_contact(item, contact_type, label, value):
    item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})


def append_contact_list(item, contact_type, label, value_list):
    for value in value_list:
        item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})


def append_motion(item, motion, resolution=None, date=None, sitting=None):
    if not 'motions' in item:
        item['motions'] = []
    data = {'motion': motion, 'resolution': resolution, 'date': date}
    if sitting: data['sitting'] = sitting
    item['motions'].append(data)


def download(url, file_path, force_redownload=False):
    skipped = not force_redownload and os.path.exists(file_path)
    retcode = None

    if not skipped:
        cmd = 'wget -c -O "%s" %s' % (file_path, url)
        retcode = subprocess.call(cmd, shell=True)

    return {
        'success': skipped or retcode == 0,
        'skipped': skipped,
        'code': retcode
    }


def get_response(url, meta={}):
    url = canonicalize_url(url)
    r = requests.get(url)

    res = r.text
    final_url = r.url

    to_encoding = 'utf-8'
    response = HtmlResponse(url=final_url, body=res, encoding=to_encoding)
    response.request = Request(url, meta=meta)

    return response


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def rows_to_pairs(rows):
    """convert to list of td pairs"""
    pairs = []
    for row in rows:
        tds = row.xpath('td')
        chunk_list = list(chunks(tds, 2))
        pairs += chunk_list
    return pairs

class UnicodeJsonItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        JsonItemExporter.__init__(self, file, ensure_ascii=False, **kwargs)
    
    def encode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self.encode_list(item)
            elif isinstance(item, dict):
                item = self.encode_dict(item)
            rv.append(item)
        return rv


    def encode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self.encode_list(value)
            elif isinstance(value, dict):
                value = self.encode_dict(value)
            rv[key] = value
        return rv
    
    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(',\n')
        itemdict = dict(self._get_serialized_fields(item))
        itemdict = self.encode_dict(itemdict)
        self.file.write(self.encoder.encode(itemdict))
