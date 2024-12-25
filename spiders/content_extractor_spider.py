import scrapy

from scrapy.exceptions import DropItem

from PyPDF2 import PdfReader

from pathlib import Path

from bs4 import BeautifulSoup

import csv

import io

class ContentExtractorSpider(scrapy.Spider):

    name = "content_extractor"

    # Specify the input file directly

    input_file = "test.csv"  # Replace with your actual file name
 
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.unscraped_links_file = f"unscraped-{self.input_file}"

        self.output_file = self.input_file.replace('.csv', '.jsonl')

        # Initialize the CSV for unscraped links

        with open(self.unscraped_links_file, mode="w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(["url", "reason"])

    def start_requests(self):

        input_path = Path(self.input_file)

        if not input_path.exists():

            self.logger.error(f"Input CSV file not found: {self.input_file}")

            return

        self.logger.info(f"Reading URLs from: {self.input_file}")

        with open(input_path, "r", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                url = row.get("url")

                last_modified = row.get("last_modified", "")

                if url:

                    yield scrapy.Request(

                        url=url,

                        callback=self.parse,

                        meta={"source_url": url, "last_modified": last_modified}

                    )

    def log_unscraped_link(self, url, reason):

        """Logs the unscraped link along with the reason."""

        with open(self.unscraped_links_file, mode="a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([url, reason])

    def parse_pdf(self, response):

        """Handles PDF content extraction."""

        try:

            pdf_reader = PdfReader(io.BytesIO(response.body))

            pdf_text = " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

            return pdf_text

        except Exception as e:

            self.log_unscraped_link(response.meta["source_url"], f"PDF parsing error: {e}")

            return None

    def parse_html(self, response):

        """Handles HTML content extraction using BeautifulSoup."""

        try:

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags

            for tag in soup(["script", "style", "nav", "header", "footer"]):

                tag.decompose()

            # Extract title and clean body text

            title = soup.title.string.strip() if soup.title else ""

            body_text = " ".join(soup.stripped_strings)

            return title, body_text

        except Exception as e:

            self.log_unscraped_link(response.meta["source_url"], f"HTML parsing error: {e}")

            return None, None

    def parse(self, response):

        source_url = response.meta.get("source_url", response.url)

        last_modified = response.meta.get("last_modified", "")

        # Determine content type

        content_type = response.headers.get("Content-Type", b"").decode()

        if "application/pdf" in content_type:

            pdf_text = self.parse_pdf(response)

            if pdf_text:

                yield {

                    "id": None,

                    "metadata": {

                        "source": source_url,

                        "title": "",  # PDFs generally don't have titles

                        "last_modified": last_modified,

                    },

                    "page_content": pdf_text,

                    "type": "PDF",

                }

        elif "text/html" in content_type:

            title, body_text = self.parse_html(response)

            if body_text:

                yield {

                    "id": None,

                    "metadata": {

                        "source": source_url,

                        "title": title,

                        "last_modified": last_modified,

                    },

                    "page_content": body_text,

                    "type": "HTML",

                }

        else:

            self.log_unscraped_link(source_url, f"Unsupported content type: {content_type}")

    def closed(self, reason):

        """Log completion and any summary statistics."""

        self.logger.info(f"Spider closed: {reason}")

        self.logger.info(f"Unscraped links saved to {self.unscraped_links_file}")

 