# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest

from ..settings import *
from ..items import ZhihuItem

class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'search/')),
        Rule(SgmlLinkExtractor(allow=r'')),
    )

    def __init__(self):
        self.headers =HEADER
        self.cookies =COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies,
                              callback = self.parse_item)#jump to login page

    def parse_item(self, response):
        selector = Selector(response)

        item = ZhihuItem()

        # for ele in selector.xpath('//ul/li[@class="suggest-item"]/div/a/@href').extract():
        #    urls.append(ele)
        for ele in selector.xpath('//div[@class="story-content-answer"]/p/a/@href').extract():
            item['url'] = ele
            yield item
