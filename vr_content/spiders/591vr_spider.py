import scrapy
from scrapy.http.request import Request
from scrapy.http import Headers


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.591vr.com/category2.html",
    ]
    select_android_header = Headers()
    select_android_header.setlist("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    select_android_header.setlist("X-Requested-With", "XMLHttpRequest")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.home_parse)

    def home_parse(self, response):
        yield Request("http://www.591vr.com/changeplatform.html", method="POST", body="pval=2",
                      dont_filter=True, headers=self.select_android_header, callback=self.reload_parse)

    def reload_parse(self, response):
        yield Request("http://www.591vr.com/category2.html", dont_filter=True, callback=self.page_parse)

    def page_parse(self, response):
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def my_parse(self, response):
        print response.headers

    def parse(self, response):
        print response.headers
        return