# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.contrib.exporter import BaseItemExporter, JsonLinesItemExporter, JsonItemExporter
import os


class ReferenceDataPipeline(object):
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "reference.json"), "r") as reference_data_file:
            self.reference_data = json.load(reference_data_file)
            self.councilors = self.reference_data["councilors"]
            self.districts = self.reference_data["districts"]

    def process_item(self, item, spider):
        if spider.name == "councilors":
            # Add platfrom and birth from reference.json
            for councilor in self.councilors:
                if councilor["name"] == item["name"]:
                    item["platform"] = councilor["platform"]
                    item["birth"] = councilor["birth"]
                    break
            
            # Add district
            item["district"] = self.districts[item["constituency"]]

        return item
