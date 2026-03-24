# Scrapy settings for animalcorner project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = "animalcorner"

SPIDER_MODULES = ["animalcorner.spiders"]
NEWSPIDER_MODULE = "animalcorner.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "animalcorner (+http://www.yourdomain.com)"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

#username = os.getenv("USERNAME_PROXY")
#password = os.getenv("PASSWORD_PROXY")
#PROXY_LIST = [
#     f"http://{username}:{password}@142.111.48.253:7030",
#     f"http://{username}:{password}@31.59.20.176:6754",
#     f"http://{username}:{password}@23.95.150.145:6114"
#]
#ROTATING_PROXY_LIST = PROXY_LIST
#RETRY_ENABLED = True
#RETRY_TIMES = 5

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
CLOSESPIDER_PAGECOUNT = 5 # limit the number of pages to crawl
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "animalcorner.middlewares.AnimalcornerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "animalcorner.middlewares.AnimalcornerDownloaderMiddleware": 100,
#    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "animalcorner.extensions.RunFileLoggerExtension": 500,
}

LOG_LEVEL = os.getenv("SCRAPY_LOG_LEVEL", "INFO")
RUN_LOGS_DIR = os.getenv("SCRAPY_RUN_LOGS_DIR", "logs")

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #"animalcorner.pipelines.MongoDBPipeline": 300,
   #"animalcorner.pipelines.DuplicatesPipeline": 300,
   #"animalcorner.pipelines.MySQLPipeline": 300,
   "animalcorner.pipelines.PostgresPipeline": 300
}

#MONGODB_URI = 'mongodb://izzun:1234@0.0.0.0:27017/?directConnection=true'
#MONGODB_DATABASE = 'animals'
#MONGODB_COLLECTION = 'animalsList'

CLOSESPIDER_ITEMCOUNT = 5

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
