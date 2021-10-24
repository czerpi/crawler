from scrapy.crawler import CrawlerProcess
from global_app.global_app.spiders.global_app import GlobalAppSpider


def run_crawler(filename: str):
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                f"{filename}.csv": {"format": "csv"},
            },
        }
    )

    process.crawl(GlobalAppSpider, name=filename)
    process.start()


if __name__ == "__main__":
    run_crawler("global_app")
