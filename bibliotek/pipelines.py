# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
# import pymysql.cursors
import json
from scrapy.settings import Settings
import requests
from scrapy.utils.serialize import ScrapyJSONEncoder
import urllib

class BibliotekPipeline(object):
    def process_item(self, item, spider):
        return item

class APICallerPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.encoder = ScrapyJSONEncoder()

    def close_spider(self, spider):
        return True

    def process_item(self, item, spider):
        
        url = "http://127.0.0.1:5000/books"
        headers = {'Content-Type': 'application/json'}
        response_data = requests.request("POST", url, data=self.encoder.encode(item), headers=headers)

        if response_data.status_code == 201:
            print("The book '{}' has been saved into the database".format(item['title']))
        return item


    def checkIfAlreadyExists(self, item):
        pass