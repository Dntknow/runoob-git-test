# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from . import mysql

class NcuscrapyPipeline:
    def process_item(self, item, spider):
        if re.match('软件|工程师|计算|技术|信息', item['job_recruitment']):
            mysql.in_sql(item['company_name'], item['recruit_type'], item['professionals'], item['job_recruitment'], item['url_href'], item['content'])
        return item
