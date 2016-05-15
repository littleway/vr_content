# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VrItem(scrapy.Item):
    page_index = scrapy.Field()
    item_index_in_page = scrapy.Field()
    name = scrapy.Field()
    publish_date = scrapy.Field()
    file_size_mb = scrapy.Field()
    language = scrapy.Field()
    version = scrapy.Field()
    developer = scrapy.Field()
    application_type = scrapy.Field()
    tags = scrapy.Field()
    star_rating = scrapy.Field()
    introduce = scrapy.Field()
    icon_url = scrapy.Field()
    detail_image_url = scrapy.Field()
    download_url = scrapy.Field()


class VrAppItem(VrItem):
    # !!!attention here: once field change, change FIELDS_TO_EXPORT in setting as well
    # the page which the app belongs to
    os = scrapy.Field()
    hardware_support = scrapy.Field()
    control_device = scrapy.Field()


class VrMovieItem(VrItem):
    pass


class ItemFactory(object):
    @staticmethod
    def create_item(item_type):
        if item_type == "android_app":
            return VrAppItem()
        elif item_type == "movie":
            return VrMovieItem()
        else:
            scrapy.logger.error("can not match Item: item_type=%s", item_type)
            return None

