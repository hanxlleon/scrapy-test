# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DoubanbookItem


class DoubanbookSpider(CrawlSpider):

    name = 'doubanbook'
    allowed_domains = ['douban.com']
    start_urls = ['http://book.douban.com']
    rules = [Rule(LinkExtractor(allow=[r'tag/[^/]+/\?focus=book']), callback='parse_douban')]

    def parse_douban(self, response):
        item = DoubanbookItem()
        item['url'] = response.url

        # book_detail = response.xpath("//div[@id='book']/dl/dd")
        # item['name'] = book_detail.xpath("a/text()")
        # item['star'] = book_detail.xpath("div[@class='rating']/span[2]/text()")
        # item['name'] = response.xpath("//div[@id='book']/dl/dd/a/text()").extract()
        item['tag'] = response.xpath("//div[@class='title']/h1/text()").extract()[0]
        for name in response.xpath("//div[@id='book']/dl/dd/a/text()").extract():
            item['name'] = name
        # item['star'] = response.xpath("//div[@id='book']/dl/dd/div[@class='rating']/span[2]/text()").extract()
        for star in response.xpath("//div[@id='book']/dl/dd/div[@class='rating']/span[2]/text()").extract():
            item['star'] = star

        yield item
