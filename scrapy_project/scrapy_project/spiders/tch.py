from scrapy.http import Response
import scrapy
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


MONTHS = {
    "січня": "1",
    "лютого": "2",
    "березня": "3",
    "квітня": "4",
    "травня": "5",
    "червня": "6",
    "липня": "7",
    "серпня": "8",
    "вересня": "9",
    "жовтня": "10",
    "листопада": "11",
    "грудня": "12"
}


class TchSpider(scrapy.Spider):
    """
    This spider scrapes job details from work.ua.
    """
    name = "tch"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-python/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def close(self, reason):
        self.driver.close()

    def parse(self, response: Response, **kwargs):
        """
        Parse the list of job postings and follow the links to detailed pages.
        """
        for tech in response.css(".card-hover"):
            yield response.follow(
                tech.css('h2 > a::attr(href)').get(),
                callback=self.parse_detail_page
            )

        next_button = response.css(".pagination > li")[-1].css("a::attr(href)").get()
        if next_button:
            next_button = response.urljoin(next_button)
            yield scrapy.Request(next_button, callback=self.parse)

    def parse_detail_page(self, response: Response):
        """
        Parse the detailed job page.
        """
        self.driver.get(response.url)
        name_element = self.get_job_name()
        technology_list = self.get_technologies_block()
        posted_date = self.extract_posted_date()
        company_name = self.get_company_name()

        yield {
            "name": name_element,
            "technologies": technology_list,
            "posted_date": posted_date,
            "company": company_name
        }

    def get_job_name(self):
        name_element = self.driver.find_element(By.CSS_SELECTOR, "ol > li:last-child").text
        return name_element

    def get_technologies_block(self):

        try:
            self.check_all_technologies_button()
        except NoSuchElementException:
            return None
        finally:
            technologies_block = self.driver.find_element(By.CLASS_NAME, "toggle-block")
            technologies = technologies_block.find_elements(By.CLASS_NAME, "label-skill")

            technology_list = []

            for technology in technologies:
                technology_list.append(technology.text)

            return technology_list

    def extract_posted_date(self):
        posted_date_element = self.driver.find_element(By.CLASS_NAME, "text-default-7")
        posted_date_text = posted_date_element.text.replace("Вакансія від ", "").split(" ")

        return f"{posted_date_text[2]}-{int(MONTHS[posted_date_text[1]]):02d}-{int(posted_date_text[0]):02d}"

    def get_company_name(self):
        company_name_element = self.driver.find_element(
            By.CSS_SELECTOR, 'a[title^="Робота в"] > span.strong-500'
        )
        company_name = company_name_element.text

        return company_name

    def check_all_technologies_button(self):
        all_tech_button = self.driver.find_element(
            By.CSS_SELECTOR, "a.block-relative.link-icon.nowrap.w-100.text-center.js-toggle-btn"
        )
        all_tech_button.click()
