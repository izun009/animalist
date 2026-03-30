import logging
import psycopg2
import pymysql
from datetime import datetime
from scrapy.exceptions import DropItem
from dotenv import load_dotenv
import os

load_dotenv()

class PostgresPipeline:

    def __init__(self, crawler=None):
        self.crawler = crawler
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT", 5432)
        )
        self.cur = self.conn.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler=crawler)

    def process_item(self, item, spider=None):
        now = datetime.utcnow()
        DEFAULT_OWNER_ID = 1
        spider = spider or getattr(self.crawler, "spider", None)

        intro = item.get("introduction")
        if isinstance(intro, dict):
           intro = intro.get("p")
        item["introduction"] = intro

        try:
            #1 Insert animal
            self.cur.execute("""
                INSERT INTO animals (name, endpoint, introduction, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (endpoint)
                DO NOTHING
                RETURNING id
            """, (
                item["name"],
                item["endpoint"],
                item["introduction"],
                DEFAULT_OWNER_ID,
                now,
                now
            ))

            result = self.cur.fetchone()
            if not result:
                logger = spider.logger if spider else logging.getLogger(__name__)
                logger.info(f"Skipping existing animal: {item['endpoint']}")
                raise DropItem(f"Animal already exists: {item['endpoint']}")

            animal_id = result[0]

            #2 Insert facts
            facts = item.get("facts", [])

            for position, fact in enumerate(facts, start=1):

                title = fact.get("title")
                description = fact.get("description")

                # Normalize description
                if isinstance(description, list):
                    description = " ".join(description)

                if isinstance(description, dict):
                    description = description.get("p")

                self.cur.execute("""
                    INSERT INTO animal_facts (animal_id, title, description, position)
                    VALUES (%s, %s, %s, %s)
                """, (
                    animal_id,
                    title,
                    description,
                    position
                ))

            #3 Insert images
            for position, img_url in enumerate(item.get("images", []), start=1):
                self.cur.execute("""
                    INSERT INTO animal_images (animal_id, image_url, position)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                """, (
                    animal_id,
                    img_url,
                    position
                ))

            self.conn.commit()
            return item

        except DropItem:
            self.conn.rollback()
            raise

        except Exception as e:
            logger = spider.logger if spider else logging.getLogger(__name__)
            logger.error(f"DB error: {e}")
            self.conn.rollback()
            raise DropItem("Database error")

    def close_spider(self, spider=None):
        self.cur.close()
        self.conn.close()


class MySQLPipeline:

    def __init__(self, crawler=None):
        self.crawler = crawler
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        self.cur = self.conn.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler=crawler)

    def process_item(self, item, spider=None):
        now = datetime.utcnow()
        DEFAULT_OWNER_ID = 1
        spider = spider or getattr(self.crawler, "spider", None)

        intro = item.get("introduction")
        if isinstance(intro, dict):
           intro = intro.get("p")
        item["introduction"] = intro

        try:
            #1 Insert animal
            self.cur.execute("""
                INSERT IGNORE INTO animals (name, endpoint, introduction, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                item["name"],
                item["endpoint"],
                item["introduction"],
                DEFAULT_OWNER_ID,
                now,
                now
            ))

            # Get the inserted animal_id
            animal_id = self.cur.lastrowid
            if animal_id == 0:
                # If INSERT IGNORE didn't insert, find existing
                self.cur.execute("SELECT id FROM animals WHERE endpoint = %s", (item["endpoint"],))
                result = self.cur.fetchone()
                if not result:
                    logger = spider.logger if spider else logging.getLogger(__name__)
                    logger.info(f"Skipping existing animal: {item['endpoint']}")
                    raise DropItem(f"Animal already exists: {item['endpoint']}")
                animal_id = result[0]

            #2 Insert facts
            facts = item.get("facts", [])

            for position, fact in enumerate(facts, start=1):

                title = fact.get("title")
                description = fact.get("description")

                # Normalize description
                if isinstance(description, list):
                    description = " ".join(description)

                if isinstance(description, dict):
                    description = description.get("p")

                self.cur.execute("""
                    INSERT INTO animal_facts (animal_id, title, description, position)
                    VALUES (%s, %s, %s, %s)
                """, (
                    animal_id,
                    title,
                    description,
                    position
                ))

            #3 Insert images
            for position, img_url in enumerate(item.get("images", []), start=1):
                self.cur.execute("""
                    INSERT IGNORE INTO animal_images (animal_id, image_url, position)
                    VALUES (%s, %s, %s)
                """, (
                    animal_id,
                    img_url,
                    position
                ))

            self.conn.commit()
            return item

        except DropItem:
            self.conn.rollback()
            raise

        except Exception as e:
            logger = spider.logger if spider else logging.getLogger(__name__)
            logger.error(f"DB error: {e}")
            self.conn.rollback()
            raise DropItem("Database error")

    def close_spider(self, spider=None):
        self.cur.close()
        self.conn.close()
