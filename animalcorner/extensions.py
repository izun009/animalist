import logging
from datetime import datetime
from pathlib import Path

from scrapy import signals


class RunFileLoggerExtension:
    def __init__(self, log_level="INFO", logs_dir="logs"):
        self.log_level = getattr(logging, str(log_level).upper(), logging.INFO)
        self.logs_dir = Path(logs_dir)
        self.handler = None
        self.log_path = None

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls(
            log_level=crawler.settings.get("LOG_LEVEL", "INFO"),
            logs_dir=crawler.settings.get("RUN_LOGS_DIR", "logs"),
        )
        crawler.signals.connect(extension.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(extension.spider_closed, signal=signals.spider_closed)
        return extension

    def spider_opened(self, spider):
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = self.logs_dir / f"{spider.name}_{timestamp}.log"

        self.handler = logging.FileHandler(self.log_path, encoding="utf-8")
        self.handler.setLevel(self.log_level)

        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        )
        self.handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.addHandler(self.handler)

        spider.logger.info("Run log file created: %s", self.log_path)

    def spider_closed(self, spider, reason):
        if self.handler is None:
            return

        stats = spider.crawler.stats.get_stats()
        spider.logger.info("Spider closed: reason=%s stats=%s", reason, stats)

        root_logger = logging.getLogger()
        root_logger.removeHandler(self.handler)
        self.handler.close()
        self.handler = None
