from scrapy.http import Response
import scrapy
from selenium import webdriver


class TchSpider(scrapy.Spider):
    name = "tch"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-python/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def close(self, reason):
        self.driver.close()

    def parse(self, response: Response, **kwargs):

        for tech in response.css(".card-hover"):
            yield {
                "name": tech.css("h2>a::text").get(),
                "company": tech.css(".add-top-xs>span::text").get(),
            }

