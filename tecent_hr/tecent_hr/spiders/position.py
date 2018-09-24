# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PositionSpider(CrawlSpider):
    name = 'position'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        # 获取title
        item['title'] = response.xpath("//td[@id='sharetitle']/text()").extract_first()
        # print(item)
        tr_list = response.xpath("//table[contains(@class,'tablelist textl')]/tr")[1:4]
        # print(tr_list)
        # 获取工作地点
        item['location'] = tr_list[0].xpath("./td[1]/text()").extract_first()
        # 职位类型
        item['type'] = tr_list[0].xpath("./td[2]/text()").extract_first()
        # 职位数量
        item['number'] = tr_list[0].xpath("./td[3]/text()").extract_first()
        responsibility = tr_list[1].xpath(".//ul[@class='squareli']/li/text()").extract()
        # 职位职责
        item['responsibility'] = ''.join(responsibility)
        # 职位要求
        require = tr_list[2].xpath(".//ul[@class='squareli']/li/text()").extract()
        item['require'] = ''.join(require)

        # 抛出item，把item交给引擎
        yield item




