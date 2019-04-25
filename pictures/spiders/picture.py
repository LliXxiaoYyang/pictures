# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy import Request

from pictures.items import PicturesItem


class PictureSpider(scrapy.Spider):
    name = 'picture'
    #allowed_domains = ['www.win4000.com/wallpaper_2285_0_10_1.html']
    start_urls = ['http://www.win4000.com/wallpaper_2285_0_10_1.html']
    headers = {
        'User-Agent':'Mozilla/5.0(Windows NT 6.1;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/73.0.3683.86Safari / 537.36',
    }

    def start_requests(self):
        for i in range(1,6):
            url = 'http://www.win4000.com/wallpaper_2285_0_10_%s.html'%str(i)
            yield Request(url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        #item = PicturesItem()
        #image_urls = response.xpath('//div[@class="main"]/div/div/div/div/div/div/a/img/@src')
        '''
        image_urls = response.xpath('//div[@class="main"]/div/div/div/div/div/div/a/img/@src').extract_first()
        item['image_urls'] = image_urls
        yield item
        '''
        imgs = response.xpath('//div[@class="w1180 clearfix"]/div/div/div/div/div/ul[@class="clearfix"]/li')
        for img in imgs:
            urls = img.xpath('a/@href').extract()[0]

            yield Request(urls,callback=self.parse_2,dont_filter=True)

    def parse_2(self, response):
        #img_urls = response.xpath('//div[@class="main"]/div/div/div/div/div/div[3]/a/@href').extract()[0]
        img_urls = response.xpath('//div[@class = "paper-conyral"]/a/@href').extract()[0]
        img_url = img_urls.replace('big','detail')
        urls = img_url[:-5]+"_"
        for i in range(2,5):
            url = urls+str(i)+'.html'
            yield Request(url,callback=self.parse_3,dont_filter=True)


    def parse_3(self,response):
        #image_urls = response.xpath('//div[@class="main"]/div/div/div/div/div/div[2]/a/@href')
        image_urls = response.xpath('//div[@class="paper-down"]/a/@href').extract()[0]
        image_url = image_urls[:-5]
        item = PicturesItem()
        img = []
        img.append(image_url)
        item['image_urls'] = img
        yield item









   #def parse(self, response):
   #    item = PicturesItem()
   #    imgs = response.xpath('//div[@class="w1180 clearfix"]/div/div/div/div/div/ul[@class="clearfix"]/li')
   #    for img in imgs:
   #        image_urls = img.xpath('a/img/@data-original').extract()
   #     #   item['image_urls'] = image_urls
   #        yield item


   #    all_urls = response.xpath('//a/@href').extract()
   #    for url in all_urls:
   #        url = urljoin(self.start_urls,url)
   #        yield Request(url,callback=self.parse)
