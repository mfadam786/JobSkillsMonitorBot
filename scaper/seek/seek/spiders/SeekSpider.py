import scrapy
from ..get_seek_pages import get_seek_pages

class JobsSpider(scrapy.Spider):
    name = "seek"

    def start_requests(self):
        start_urls = get_seek_pages()
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("?")[-1]
        filename = f'jobs-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')