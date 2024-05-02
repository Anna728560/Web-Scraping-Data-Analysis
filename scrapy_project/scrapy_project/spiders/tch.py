import scrapy


class TchSpider(scrapy.Spider):
    name = "tch"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-python/"]

    def parse(self, response):
        pass
