import scrapy
import myglobal as mg
# from db_variable import *
# from scrapy_splash import SplashRequest
# import pymysql.cursors
# import pymongo
import mysqlconn
# import json

class QuotesSpider(scrapy.Spider):
    name = "detiknews"
    limit_reached = False

    def start_requests(self):

        url = 'https://news.detik.com/indeks/1'

        self.limit = 'https://news.detik.com/detiktv/d-5709772/polisi-pemasok-sabu-coki-pardede-punya-banyak-kenalan-artis'
        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.xpath('//div[@class="grid-row list-content"]').xpath('//article/div/div[@class="media__text"]/h3/a/@href').extract()
        next_page = response.xpath('//div[@class="pagination text-center mgt-16 mgb-16"]/a[last()]/@href').extract_first()

        print('============================items=====================================')
        print(next_page)

        for item in items:
            print(item)
            if item == self.limit:
                self.limit_reached = True
                break
            else:
                yield scrapy.Request(url=item, callback=self.parse_item)

        if self.limit_reached is False:
            yield scrapy.Request(url=next_page, callback=self.parse)
            

    def parse_item(self, response):
        title = response.xpath('//h1[@class="detail__title"]/text()').extract_first().strip()
        thumbnail = response.xpath('//figure/img/@src').extract_first()
        content = response.xpath('//div[@class="detail__body-text itp_bodycontent"]').extract_first()[47:][:-6].strip()
        date = response.xpath('//div[@class="detail__date"]/text()').extract_first().split(', ')[1].split(' ')
        clock = date[3] + ':00'
        date = date[2] + '-' + mg.month1[date[1]] + '-' + date[0]

        print(title)
        print(date)
        print(clock)

        val = (title, thumbnail, content, date, clock)
        mysqlconn.insert(val)