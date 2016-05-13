# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VrAppItem(scrapy.Item):
    # !!!attention here: once field change, change FIELDS_TO_EXPORT in setting as well
    # the page which the app belongs to
    page_index = scrapy.Field()
    app_index = scrapy.Field()
    os = scrapy.Field()
    name = scrapy.Field()
    publish_date = scrapy.Field()
    file_size_mb = scrapy.Field()
    language = scrapy.Field()
    developer = scrapy.Field()
    hardware_support = scrapy.Field()
    control_device = scrapy.Field()
    app_type = scrapy.Field()
    tags = scrapy.Field()
    star_rating = scrapy.Field()
    app_introduce = scrapy.Field()
    icon_url = scrapy.Field()
    detail_image_url = scrapy.Field()
    download_url = scrapy.Field()

