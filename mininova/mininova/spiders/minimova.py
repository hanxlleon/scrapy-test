# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import MininovaItem


class MininovaSpider(CrawlSpider):

    name = 'mininova'
    allowed_domains = ['guokr.com']
    start_urls = ['http://www.guokr.com/post/689910']
    rules = [Rule(LinkExtractor(allow=['/post/\d+']), 'parse_torrent')]

    def parse(self, response):
        torrent = MininovaItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//title/text()").extract()
        torrent['description'] = response.xpath("//div[@id='articleContent']/p/text()").extract()
        torrent['size'] = response.xpath("//span[@class='post-like-num']/text()").extract()
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            for t in torrent.itervalues():
                if isinstance(t, list):
                    for i in t:
                        f.write(i.encode('utf-8'))
                else:
                    f.write(t)
        # return torrent