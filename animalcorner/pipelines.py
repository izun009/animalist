# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo, psycopg2
from datetime import datetime
from psycopg2.extras import Json
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os

load_dotenv()

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
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT", 5432)
        )
        self.cur = self.conn.cursor()
        # self.cur.execute("""
        #     CREATE TABLE IF NOT EXISTS animals (
        #         id SERIAL PRIMARY KEY,
        #         name TEXT NOT NULL,
        #         images JSONB,
        #         introduction JSONB,
        #         facts JSONB,
        #         endpoint TEXT UNIQUE
        #     )
        # """)
        self.conn.commit()

    def process_item(self, item, spider):
        now = datetime.utcnow()
        DEFAULT_OWNER_ID = 1
        try:
            self.cur.execute("""
                INSERT INTO animals (name, images, introduction, facts, endpoint, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (endpoint) DO NOTHING
            """, (
                item.get("name"),
                Json(item.get("images")),
                Json(item.get("introduction")),
                Json(item.get("facts")),
                item.get("endpoint"),
                DEFAULT_OWNER_ID,
                now,
                now
            ))
            self.conn.commit()

        except Exception as e:
            spider.logger.error(f"❌ Error inserting item: {e}")
            self.conn.rollback()  # prevent 'InFailedSqlTransaction'

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


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
