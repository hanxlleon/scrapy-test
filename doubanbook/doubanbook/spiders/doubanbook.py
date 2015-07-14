# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DoubanbookItem


class DoubanbookSpider(CrawlSpider):

    name = 'doubanbook'
    allowed_domains = ['douban.com']
    start_urls = ['http://book.douban.com']
    # rules = [Rule(LinkExtractor(allow=[r'tag/[^/]+/\?focus=book']), callback='parse_douban', process_request='add_cookie')]
    rules = [Rule(LinkExtractor(allow=[r'tag/[^/]+/\?focus=book']), callback='parse_douban')]

    def parse_douban(self, response):
        self.log("Fetch book list page: %s" % response.url)
        item = DoubanbookItem()
        item['url'] = response.url

        item['tag'] = response.xpath("//div[@class='title']/h1/text()").extract()[0]
        name_list = response.xpath("//div[@id='book']/dl/dd/a/text()").extract()
        star_list = response.xpath("//div[@id='book']/dl/dd/div[@class='rating']/span[2]/text()").extract()
        book_list = map(None, name_list, star_list)
        for book in book_list:
            item['name'], item['star'] = book
            yield item

    def add_cookie(self, request):
        request.replace(cookies=[{'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}])
        return request

