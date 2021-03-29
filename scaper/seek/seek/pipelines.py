# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pathlib import Path
import pandas as pd
from datetime import datetime
from .items import SeekItem
import codecs



class SeekPipeline:

    def __init__(self):
        self.ids_seen = set()
        self.scraped_df = None
        self.scraped_path = Path("../out/scraped.csv")



    def open_spider(self, spider):

        if self.scraped_path.exists():
            self.scraped_df = pd.read_csv(self.scraped_path, comment="#", index_col="id")
            self.ids_seen = set(self.scraped_df.index.values)
        else:
            item = SeekItem()
            #print(item.fields.keys())
            self.scraped_df = pd.DataFrame(columns=item.fields.keys()).set_index("id")


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        line = adapter.asdict()
        id = line["id"]
       # print(id)
        if id in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:

            self.ids_seen.add(id)

            del line["id"]
            self.scraped_df.loc[id] = line

            return item

    def close_spider(self, spider):
        now = datetime.now()
        f = codecs.open(self.scraped_path, 'w', "utf-8")
        f.write(f"# Updated at {now.strftime('%H:%M:%S')} \n")
        self.scraped_df.to_csv(f, encoding="utf-8")
        f.close()

