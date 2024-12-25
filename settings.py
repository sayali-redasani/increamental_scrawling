# Scrapy settings for web_scrapping_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "web_scrapping_spider"

SPIDER_MODULES = ["web_scrapping_spider.spiders"]
NEWSPIDER_MODULE = "web_scrapping_spider.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "web_scrapping_spider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
 
# Enable and configure the AutoThrottle extension (disabled by default)

# See https://docs.scrapy.org/en/latest/topics/autothrottle.html

AUTOTHROTTLE_ENABLED = True

# The initial download delay

AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies

AUTOTHROTTLE_MAX_DELAY = 60

SCRAPYCLOUD_API_KEY = "28d9a2e222744f56b3b248a27e9c37c8"

SCRAPYCLOUD_PROJECT_ID = 789625

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

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

FEED_EXPORT_ENCODING = "utf-8"
 
DEPTH_LIMIT = 10
 
DEPTH_PRIORITY = 1  # Positive value for BFS

SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'  # FIFO for disk queue

SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'  # FIFO for memory queue
 
#DEPTH_PRIORITY = -1  # Negative value for DFS

#SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'  # LIFO for disk queue

#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'  # LIFO for memory queue
 
LOG_LEVEL = 'DEBUG'

# LOG_FILE  = 'spider.log'
 
# DEFAULT_REQUEST_HEADERS = {

#     # Prioritize HTML (text/html) first, then PDF (application/pdf)

#     "Accept": "text/html, application/xhtml+xml, application/pdf, application/xml;q=0.9, */*;q=0.8",  

#     "Accept-Language": "en-US,en;q=0.9",  # Preferred language for the content (English)

#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

#     "X-Requested-With": "XMLHttpRequest",

# }
 
# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# AutoThrottle extension — Scrapy 2.12.0 documentation
 