import psycopg2
from datetime import datetime
from scrapy.exceptions import DropItem
from dotenv import load_dotenv
import os

load_dotenv()


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

    def process_item(self, item, spider):
        now = datetime.utcnow()
        DEFAULT_OWNER_ID = 1

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
                DO UPDATE SET updated_at = EXCLUDED.updated_at
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
            for img_url in item.get("images", []):
                self.cur.execute("""
                    INSERT INTO animal_images (animal_id, url)
                    VALUES (%s, %s)
                """, (
                    animal_id,
                    img_url
                ))

            self.conn.commit()
            return item

        except DropItem:
            self.conn.rollback()
            raise

        except Exception as e:
            spider.logger.error(f"❌ DB error: {e}")
            self.conn.rollback()
            raise DropItem("Database error")

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
