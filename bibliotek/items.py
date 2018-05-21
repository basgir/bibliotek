# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Book(scrapy.Item):
    """Scrap item model that collect all required fields."""

    title = scrapy.Field()
    authorId = scrapy.Field()
    publisher  = scrapy.Field()
    published_date = scrapy.Field()
    description = scrapy.Field()
    isbn10  = scrapy.Field()
    isbn13  = scrapy.Field()
    categoryId  = scrapy.Field()
    booktype = scrapy.Field()
    language = scrapy.Field()    
    thumbnail = scrapy.Field()
    page_count = scrapy.Field()
    md5 = scrapy.Field()
    url_info = scrapy.Field()
    dl_link1 = scrapy.Field()
    dl_link2 = scrapy.Field()
    chosen_url = scrapy.Field()
    filepath = scrapy.Field()
