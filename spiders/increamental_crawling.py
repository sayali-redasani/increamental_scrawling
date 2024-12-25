from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import json
import os
from urllib.parse import urljoin
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from email.utils import parsedate_to_datetime

class IncrementalSpider(CrawlSpider):
    name = 'incremental_spider'
    
    allowed_domains = ['triveniturbines.com']
    start_urls = ['https://www.triveniturbines.com/']
    
    rules = (
        Rule(
            LinkExtractor(
                deny_domains=['account.amd.com', 'library.amd.com', 'ontrack.amd.com'],
                canonicalize=True,
                deny_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'mp4', 'mp3', 
                               'zip', 'rar', 'exe', 'tar', 'gz', 'deb', 'docs', 'docx', 
                               'xls', 'xlsm', 'rpm.digests', 'rpm.sig', 'deb.digests', 'deb.sig'],
                deny=(
                    r'login',
                    r'sign-up',
                    r'register',
                    r'registration',
                    r'create-account',
                    r'userloginpage',
                    r'\?.*',
                ),
            ),
            callback='parse_item',
            follow=True,
            process_request='process_request'
        ),
    )
    
    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True
            }
        },
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 10,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,  # Add delay between requests
        'COOKIES_ENABLED': False,
        'DEPTH_LIMIT': 5,
    }

    def __init__(self, *args, **kwargs):
        super(IncrementalSpider, self).__init__(*args, **kwargs)
        self.urls_data = {}  # Store URL data with last modified dates
        os.makedirs('data', exist_ok=True)
        self.state_file = 'data/spider_state.json'
        self.load_state()

    def load_state(self):
        """Load previous crawl state"""
        try:
            with open(self.state_file, 'r') as f:
                self.urls_data = json.load(f)
            self.logger.info(f"Loaded {len(self.urls_data)} URLs from previous state")
        except FileNotFoundError:
            self.logger.info("No previous state found, starting fresh")
            self.urls_data = {}

    def save_state(self):
        """Save current state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.urls_data, f)
        self.logger.info(f"Saved {len(self.urls_data)} URLs to state file")

    def get_last_modified(self, response):
        """Get last modified date from response"""
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            try:
                return parsedate_to_datetime(last_modified.decode('utf-8')).isoformat()
            except:
                pass
        # If no valid Last-Modified header, use current time
        return datetime.utcnow().isoformat()

    def should_process_url(self, url, last_modified):
        """Check if URL should be processed"""
        if url not in self.urls_data:
            self.logger.info(f"New URL found: {url}")
            return True
        
        stored_date = self.urls_data[url].get('last_modified')
        if not stored_date:
            return True
        
        try:
            stored_dt = datetime.fromisoformat(stored_date)
            current_dt = datetime.fromisoformat(last_modified)
            should_process = current_dt > stored_dt
            
            if should_process:
                self.logger.info(f"Content changed for URL: {url}")
            else:
                self.logger.info(f"Content unchanged for URL: {url}")
            
            return should_process
        except Exception as e:
            self.logger.error(f"Error comparing dates for {url}: {str(e)}")
            return True

    def process_request(self, request, spider):
        """Process request before sending"""
        url = request.url
        if url in self.urls_data:
            # Add If-Modified-Since header for incremental crawling
            last_modified = self.urls_data[url].get('last_modified')
            if last_modified:
                request.headers['If-Modified-Since'] = last_modified
        return request

    def parse_pdf(self, response):
        """Extract text from PDF"""
        try:
            reader = PdfReader(BytesIO(response.body))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {response.url}: {e}")
            return ""

    def parse_item(self, response):
        """Parse individual pages"""
        current_url = response.url
        self.logger.info(f"Parsing URL: {current_url}")
        # lang = response.xpath('//html/@lang').get()
        # if not (lang and lang.lower().startswith('en')):
        #     self.logger.info(f"Skipping non-English page: {current_url} (lang: {lang})")
        #     return

        current_depth = response.meta.get('depth', 0)
        
        last_modified = self.get_last_modified(response)
        
        # Check if we need to process this URL
        if not self.should_process_url(current_url, last_modified):
            self.logger.info(f"Skipping unchanged content: {current_url}")
            return
        
        if current_url.lower().endswith('.pdf'):
                content = self.parse_pdf(response)
                title = "PDF Document"
        else:
            # Extract HTML content
            title = response.css('h1::text').get() or response.css('title::text').get()
            content = " ".join(response.css('p::text').getall())

        
        try:
            # Extract data
            data = {
                'url': current_url,
                'title': title,
                # 'content': ' '.join(response.css('p::text').getall()),
                'last_modified': last_modified,
                'depth': current_depth,
                'crawl_time': datetime.utcnow().isoformat()
            }
            
            # Update stored data
            self.urls_data[current_url] = {
                'last_modified': last_modified,
                'last_crawled': datetime.utcnow().isoformat()
            }
            
            self.logger.info(f"Successfully extracted data from {current_url}")
            yield data

        except Exception as e:
            self.logger.error(f"Error parsing {current_url}: {str(e)}")

    def closed(self, reason):
        """Called when spider is closed"""
        self.save_state()
        self.logger.info(f"Spider closed: {reason}")
        self.logger.info(f"Total URLs in state: {len(self.urls_data)}")
# items.py (optional, for structured data)
# from scrapy import Item, Field

# class WebpageItem(Item):
#     url = Field()
#     title = Field()
#     content = Field()
#     last_modified = Field()

# middlewares.py (optional, for custom request/response handling)
# from scrapy import signals
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
# from scrapy.utils.response import response_status_message

# class CustomRetryMiddleware(RetryMiddleware):
#     def process_response(self, request, response, spider):
#         if response.status in self.retry_http_codes:
#             reason = response_status_message(response.status)
#             return self._retry(request, reason, spider) or response
#         return response