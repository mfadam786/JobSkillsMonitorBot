import scrapy
from ..get_seek_pages import get_seek_pages
from ..items import SeekItem

class JobsSpider(scrapy.Spider):
    name = "seek"


    start_urls = get_seek_pages()
    # for url in urls:
    #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        job = SeekItem()
        job["id"]= response.url.split("/")[-1]
        job["title"] = response.xpath('//span[@data-automation="job-detail-title"]//text()').get()
        job["employer"] = response.xpath('//span[@data-automation="advertiser-name"]//text()').get()
        job["main_content"] = response.xpath('//div[@data-automation="jobDescription"]//*[not(@data-automation="mobileTemplate")]//*[not(@type="text/css")]/text()').getall()
        job["date_listed"] = response.xpath('//dd[@data-automation="job-detail-date"]//text()').get()
        job["main_location"] = response.xpath('//section[@role="region"]/dl/dd[2]//text()').get()
        job["sub_location"] = response.xpath('//section[@role="region"]/dl/dd[2]/span/span/span/text()').get()
        job["job_hours"] = response.xpath('//section[@role="region"]/dl/dd[3]//text()').get()
        job["job_subsection"] = response.xpath('//section[@role="region"]/dl/div/dd/span/span/span/text()').get()
        yield job
