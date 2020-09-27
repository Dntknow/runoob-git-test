import scrapy
from scrapy import Request
#import requests
import re
import json
from ..items import NcuscrapyItem

class NcuSpider(scrapy.Spider):
    name = 'ncu'
    allowed_domains = ['jy.ncu.edu.cn/index']
    #start_urls = ['http://jy.ncu.edu.cn/module/onlines?menu_id=6505']
    # "Accept": "application / json, text / javascript, * / *; q = 0.01",
    # "Content- Type": "application / x - www - form - urlencoded; charset = UTF - 8",
    headers = {

        "Cookie": "Hm_lvt_9d62b12bee08da154fa2a80d8ee90355=1600667200,1600750240,1600937043; PHPSESSID=ST-410075-EWkrqHAm5XlEjhcR3T9C-cas; Hm_lpvt_9d62b12bee08da154fa2a80d8ee90355=1600943359",        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",

    }

    def start_requests(self):
        for i in range(1, 726):
            #n = 208 + i
            #url = 'http://jy.ncu.edu.cn/module/getonlines?start_page=1&keyword=&recruit_type=&count=15&start=1&_=1600944649828'
            url = 'http://jy.ncu.edu.cn/module/getonlines?start_page=1&keyword=&recruit_type=&count=15&start=%d&_=1600944649828' % (i)
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        #self.logger.debug(response.text)
        #data = json.loads(response.text)

        #print(response.json())
        data = response.json().get('data')
        print(data[0])

        for i in range(0, len(data)):
            it = dict(data[i])
            item = NcuscrapyItem()
            item['company_name'] = it.get('company_name')
            item['recruit_type'] = it.get('recruit_type')
            item['professionals'] = it.get('professionals')
            item['job_recruitment'] = it.get('job_recruitment')
            item['content'] = it.get('content')
            item['url_href'] = 'http://jy.ncu.edu.cn/detail/online?id=%s&menu_id=6505' % it.get('recruitment_id')
            yield item
            #print(item)

        '''
        for company in response.xpath('//*[@id="data_html"]/li[@class="item"]'):
            item = NcuscrapyItem()
            item.name = company.xpath('p/a[@class="item-link"]/text()')
            item.request = company.xpath('p[1]/text()')
            item.work = company.xpath('p[2]/text()')
            item.url_href = company.xpath('p/a[@class="item-link"]/@href')
            print(company)
        pass
        '''

