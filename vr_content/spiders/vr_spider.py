from scrapy.http.request import Request
from vr_content.items import VrAppItem
from vr_content.spiders.item_spider import ItemSpider
import json


class MovieSpider(ItemSpider):
    name = "movie"
    page_urls = {page_index:
                      "http://www.591vr.com/category1.html?acid=&sort=0&eid=&phid=&rid=&page=%d" % page_index
                 for page_index in range(1, 11)}

    def start_requests(self):
        for page_index, url in self.page_urls.items():
            yield Request(url, dont_filter=True, meta={"page_index": page_index}, callback=self.page_parse)

    def item_parse(self, response):
        item = self._get_base_parsed_item(response)
        # different to app html
        try:
            item['developer'] = self._str_post_process(
                response.xpath('//p[@class="tool-developer"]/text()').extract()[0].strip())
        except:
            item['developer'] = 'NULL'
        item['application_type'] = self._get_app_type(
            response.xpath('//div[@class="tool-device mt5 clearfix"]'))

        post_body = self._get_download_post_body(response.xpath('//ul[@class="type-main clearfix"]/li/a'))
        yield Request("http://www.591vr.com/downloadApp.html", method="POST", body=post_body,
                      meta={'item': item}, headers=self.post_header, callback=self.parse_download)


class AppSpider(ItemSpider):
    name = "android_app"
    allowed_domains = ["591vr.com"]
    start_urls = [
        "http://www.591vr.com/category2.html",
    ]
    page_urls = {page_index:
                     "http://www.591vr.com/category2.html?acid=&sort=0&eid=&phid=&rid=&page=%d" % page_index
                 for page_index in range(1, 10)}

    def parse(self, response):
        yield Request("http://www.591vr.com/changeplatform.html", method="POST", body="pval=2",
                      dont_filter=True, headers=self.post_header, callback=self.reload_parse)

    def reload_parse(self, response):
        for page_index, url in self.page_urls.items():
            yield Request(url, dont_filter=True, meta={"page_index": page_index}, callback=self.page_parse)

    def item_parse(self, response):
        item = self._get_base_parsed_item(response)
        item['os'] = "Android"
        try:
            item['hardware_support'] =\
                response.xpath('//div[@class="tool-device clearfix"]/p/text()').extract()[0]
        except:
            item['hardware_support'] = 'NULL'
        try:
            item['control_device'] =\
                response.xpath('//div[@class="tool-device mt5 clearfix"][1]/p/text()').extract()[0]
        except:
            item['control_device'] = 'NULL'
        item['detail_image_url'] = self._get_detail_image_url(response.xpath('//ul[@class="rslides"]'))

        download_node = response.xpath('//span[@class="type-text fl"]/i[@class="ui-icon android-ico"]')
        download_node = download_node.xpath('../..')
        post_body = self._get_download_post_body(download_node)
        yield Request("http://www.591vr.com/downloadApp.html", method="POST", body=post_body,
                      meta={'item': item}, headers=self.post_header, callback=self.parse_download)

    @staticmethod
    def parse_download(response):
        download_url = json.loads(response.body)['obj']
        if download_url.find(".apk") == -1:
            return
        response.meta['item']['download_url'] = ItemSpider._str_post_process(json.loads(response.body)['obj'])
        yield response.meta['item']

    @staticmethod
    def _get_detail_image_url(xpath_node):
        url = []
        for node in xpath_node.xpath('./li'):
            try:
                url.append(ItemSpider._str_post_process(node.xpath('./img/@src').extract()[0].strip()[0:-5]))
            except:
                # url.append(ItemSpider._get_video_url(node.xpath('./iframe/@src').extract()[0]))
                pass
        return url

    # # for one app test
    # def start_requests(self):
    #     yield Request("http://www.591vr.com/detail1349.html", callback=self.app_test)

    # for one app test
    def app_test(self, response):
        item = VrAppItem()
        item['app_index'] = "0"
        item['page_index'] = "1"
        item['os'] = "1"

        item['name'] = response.xpath('//h3/text()').extract()[0].strip()
        item['publish_date'] = response.xpath('//p[@class="publish-date"]/text()').extract()[1].strip()

        file_size_mb = self._get_file_size(
            response.xpath('//div[@class="tool-s-details clearfix"]/p[@class="file-size"]/text()').extract()[0].strip())
        item['file_size_mb'] = file_size_mb
        item['language'] = response.xpath('//p[@class="tool-language"]/text()').extract()[0].strip()
        item['developer'] = response.xpath('//p[@class="tool-developer"]/span[2]/text()').extract()[0].strip()
        item['hardware_support'] =\
            response.xpath('//div[@class="tool-device clearfix"]/p/text()').extract()[0]
        item['control_device'] =\
            response.xpath('//div[@class="tool-device mt5 clearfix"][1]/p/text()').extract()[0]
        item['app_type'] = self._get_app_type(
            response.xpath('//div[@class="tool-device mt5 clearfix"][2]'))
        item['tags'] = self._get_tags(response.xpath('//div[@class="tool-type clearfix"]'))
        item['star_rating'] = len(response.xpath('//div[@class="tool-start clearfix"]/ul/li'))
        item['app_introduce'] = response.xpath('//div[@id="share_summary"]/text()').extract()[0].strip()
        item['icon_url'] = response.xpath('//img[@id="share-pic"]/@src').extract()[0]
        item['detail_image_url'] = self._get_detail_image_url(response.xpath('//ul[@class="rslides"]'))

        post_body = self._get_download_post_body(response.xpath('//ul[@class="type-main clearfix"]/li/a'))
        yield Request("http://www.591vr.com/downloadApp.html", method="POST", body=post_body,
                      meta={'item': item}, headers=self.post_header, callback=self.parse_download)