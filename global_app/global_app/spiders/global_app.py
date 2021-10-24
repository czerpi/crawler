import scrapy
from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass


@dataclass
class URLData:
    scheme: str
    domain: str
    path: str

    @property
    def full_url(self) -> str:
        return str(self.scheme + "://" + self.domain + self.path)

    def __str__(self) -> str:
        return self.scheme + "://" + self.domain + self.path


class GlobalAppSpider(scrapy.Spider):
    download_delay = 0.5  # 500 ms of delay

    @staticmethod
    def url_parser(url: str) -> URLData:
        url_parser = urlparse(url)
        return URLData(url_parser.scheme, url_parser.netloc, url_parser.path)

    @classmethod
    def get_urls_in_batch(cls, response) -> list[list[URLData], list[URLData]]:
        local_urls: list[URLData] = list()
        foreign_urls: list[URLData] = list()
        urls_to_check = response.css('a::attr(href)').getall()

        def process_url(url_to_process: URLData) -> None:
            if url_to_process.domain.endswith('globalapptesting.com'):
                local_urls.append(url_to_process)
            elif url_to_process.domain:
                foreign_urls.append(url_to_process)

        for url in urls_to_check:
            if url.startswith('/'):
                url = response.urljoin(url)
                process_url(cls.url_parser(url))
            else:
                process_url(cls.url_parser(url))

        return local_urls, foreign_urls

    def start_requests(self):
        urls = [
            'https://www.globalapptesting.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        from_full_url = self.url_parser(response.url).full_url
        if response.status != 200:
            yield {
                'url': from_full_url,
                'next_url': '',
                'len_next_urls': 0,
                'next_full_urls_unique': '',
                'len_foreign_urls': 0,
                'foreign_urls_unique': '',
                'foreign_domains_unique': '',
                'request_status': response.status,
                'body_size': 0,
            }
        next_urls, foreign_urls = self.get_urls_in_batch(response)

        next_full_urls = [url.full_url for url in next_urls]
        foreign_full_urls = [url.full_url for url in foreign_urls]
        foreign_domains = [url.domain for url in foreign_urls]
        len_next_urls = len(next_full_urls)
        next_full_urls_unique = list(set(next_full_urls))
        len_foreign_urls = len(foreign_full_urls)
        foreign_urls_unique = list(set(foreign_full_urls))
        foreign_domains_unique = list(set(foreign_domains))
        body_size = len(response.body)

        for next_url in next_urls:
            yield {
                'url': from_full_url,
                'next_url': next_url.full_url,
                'len_next_urls': len_next_urls,
                'next_full_urls_unique': next_full_urls_unique,
                'len_foreign_urls': len_foreign_urls,
                'foreign_urls_unique': foreign_urls_unique,
                'foreign_domains_unique': foreign_domains_unique,
                'request_status': response.status,
                'body_size': body_size,
            }
            yield response.follow(
                next_url.full_url,
                meta={
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302]
                },
                callback=self.parse)



