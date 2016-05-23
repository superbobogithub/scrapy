# -*- coding: utf-8 -*-
import scrapy
import re
from doubanbook.items import DoubanbookItem

#http://www.jianshu.com/p/fa614bea98eb  scrapy安装与真的快速上手——爬取豆瓣9分榜单
#http://www.jianshu.com/p/f030cba076a2  scrapy爬虫与Ajax动态页面——爬取拉勾网职位信息（1）



class DbbookSpider(scrapy.Spider):

    name = "dbbook"


    start_urls = (

          'https://www.douban.com/doulist/1264675//',
    )

    def parse(self, response):

        item = DoubanbookItem()
        selector = scrapy.Selector(response)
        books = selector.xpath('//div[@class="bd doulist-subject"]')

        for each in books:
            title = each.xpath('div[@class="title"]/a/text()').extract()[0]
            rate = each.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            author = re.search('<div class="abstract">(.*?)<br', each.extract(), re.S).group(1)
            title = title.replace(' ', '').replace('\n', '')
            author = author.replace(' ', '').replace('\n', '')
            # print 'title:' + title
            # print 'rate:' + rate
            # print author
            # print ''
            item['title'] = title
            item['rate'] = rate
            item['author'] = author
            yield  item
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                next = nextPage[0]
                print next
                yield scrapy.http.Request(next, callback=self.parse)
