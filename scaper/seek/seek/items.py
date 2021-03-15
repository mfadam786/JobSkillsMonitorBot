# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeekItem(scrapy.Item):

    id = scrapy.Field()
    title = scrapy.Field()
    employer = scrapy.Field()
    main_content = scrapy.Field()
    date_listed = scrapy.Field()
    main_location = scrapy.Field()
    sub_location = scrapy.Field()
    job_hours = scrapy.Field()
    job_subsection = scrapy.Field()





