# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.utils.python import to_bytes


class PicturesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            # 做了一下判断，排除一些无效链接
            if re.match(r'http', url):
                yield Request(url)

    # 重新定义了一下存储路径，默认情况下是存在一个full文件夹里面
    def file_path(self, request, response=None, info=None):
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return '%s.jpg' % image_guid


    #def process_item(self, item, spider):
    #    return item
