from scrapy import Selector
from scrapy.http import Response
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By


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
                "technologies": self.parse_technologies_block(response, tech),
                "posted_date": self.extract_posted_date(response, tech),
            }

    def open_job_page(self, response: Response, tech: Selector):
        detailed_url = tech.css("h2>a::attr(href)").get()
        self.driver.get(response.urljoin(detailed_url))

    def parse_technologies_block(self, response: Response, tech: Selector):
        self.open_job_page(response, tech)

        technologies_block = self.driver.find_element(By.CLASS_NAME, "toggle-block")
        technologies = technologies_block.find_elements(By.CLASS_NAME, "label-skill")

        technology_list = []

        for technology in technologies:
            technology_list.append(technology.text)

        return technology_list

    def extract_posted_date(self, response: Response, tech: Selector):
        self.open_job_page(response, tech)

        posted_date_element = self.driver.find_element(By.CLASS_NAME, "text-default-7")
        posted_date_text = posted_date_element.text.replace("Вакансія від ", "")

        return posted_date_text


