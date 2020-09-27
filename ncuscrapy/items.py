# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy import Item, Field

class NcuscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    recruit_type = scrapy.Field()
    professionals = scrapy.Field()
    job_recruitment = scrapy.Field()
    content = scrapy.Field()
    url_href = scrapy.Field()
    pass
