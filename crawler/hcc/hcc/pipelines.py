# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.contrib.exporter import BaseItemExporter, JsonLinesItemExporter, JsonItemExporter


class HccPipeline(object):
    def process_item(self, item, spider):
        return item


def encode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = encode_list(item)
        elif isinstance(item, dict):
            item = encode_dict(item)
        rv.append(item)
    return rv


def encode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = encode_list(value)
        elif isinstance(value, dict):
            value = encode_dict(value)
        rv[key] = value
    return rv


class UnicodeJsonItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        JsonItemExporter.__init__(self, file, ensure_ascii=False, **kwargs)

    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(',\n')
        itemdict = dict(self._get_serialized_fields(item))
        itemdict = encode_dict(itemdict)
        self.file.write(self.encoder.encode(itemdict))
