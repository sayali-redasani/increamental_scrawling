import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
 
class UrlSpider(CrawlSpider):
    name = 'url_spider'
    allowed_domains = ['amd.com']  # triveniturbines.com
    start_urls = ['http://www.amd.com/en']  # https://www.triveniturbines.com/
 
    rules = (
        Rule(
            LinkExtractor(
                deny_domains=['account.amd.com', 'library.amd.com', 'ontrack.amd.com'],
                canonicalize=True,
                deny_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'mp4', 'mp3', 'zip', 'rar', 'exe', 'tar', 'gz', 'deb', 'docs', 'docx', '.xls', '.xlsm', 'rpm.digests', 'rpm.sig', 'deb.digests', 'deb.sig'],
                deny=(
                    r'login',         # URLs with 'login'
                    r'sign-up',       # URLs with 'signup'
                    r'register',      # URLs with 'register'
                    r'registration',
                    r'create-account', # Other common patterns for registration
                    r'userloginpage',
                    r'\?.*',
                ),
            ),
            callback='parse_item',
            follow=True
        ),
    )
 
    def parse_item(self, response):
        # Extract the language from the <html> tag
        lang = response.xpath('//html/@lang').get()
 
        # If 'lang' attribute exists and starts with 'en' (case-insensitive), process the page
        if lang and lang.lower().startswith('en'):
            # Extract the Last-Modified header if present
            last_modified = response.headers.get('Last-Modified', b'').decode('utf-8')
            # Extract depth and URL
            current_depth = response.meta.get('depth', 0)
           
            yield {
                'url': response.url,
                'last_modified': last_modified if last_modified else '',  # Return empty string if not present
                'language': str(lang),
                'depth' : str(current_depth)
            }
        else:
            # Skip the non-English pages by returning nothing  
            self.logger.info(f"Skipping non-English page: {response.url}")