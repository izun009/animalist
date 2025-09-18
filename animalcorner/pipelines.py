# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo, psycopg2
from psycopg2.extras import Json
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class DuplicatesPipeline:
    def __init__(self):
        self.seen = set()  # memory only (resets every run)

    def process_item(self, item, spider):
        endpoint = item.get("endpoint") # unique identifier

        if endpoint in self.seen:
            raise DropItem(f"Duplicate item found: {endpoint}")
        else:
            self.seen.add(endpoint)
            return item

class PostgresPipeline:

    def __init__(self):
        hostname='localhost'
        db='animalsdb'
        user='animals'
        password='P455w0rd53cr3t'
        port='5432'

        self.conn = psycopg2.connect(host=hostname,user=user,password=password,dbname=db)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS animals( 
            id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
            name varchar(100) not null, 
            introduction TEXT not null, 
            facts TEXT not null, 
            endpoint varchar(255) not null, 
            images varchar(255) not null)""")
    

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname="animalsdb",
            user="animals",
            password="P455w0rd53cr3t",
            host="0.0.0.0",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO animals (name, images, introduction, facts, endpoint)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (endpoint) DO NOTHING
        """, (
            item.get("name"),
            item.get("images"),
            Json(item.get("introduction")),
            Json(item.get("facts")),
            item.get("endpoint")
        ))
        self.conn.commit()
        return item


# class MongoDBPipeline:
#     def __init__(self, mongo_uri, mongo_db, mongo_collection):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.mongo_collection = mongo_collection

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGODB_URI'),
#             mongo_db=crawler.settings.get('MONGODB_DATABASE'),
#             mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.collection = self.db[self.mongo_collection]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.db[self.mongo_collection].insert_one(dict(item))
#         return item
