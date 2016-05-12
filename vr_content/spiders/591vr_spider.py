import scrapy
from scrapy.http.request import Request
from scrapy.http import Headers
from scrapy.contrib.loader import ItemLoader
from vr_content.items import VrAppItem
import json


class AppSpider(scrapy.Spider):
    name = "android_app"
    allowed_domains = ["591vr.com"]
    start_urls = [
        "http://www.591vr.com/category2.html",
    ]
    page_urls = {page_index:
                     "http://www.591vr.com/category2.html?acid=&sort=0&eid=&phid=&rid=&page=%d" % page_index
                 for page_index in range(1, 10)}
    post_header = Headers()
    post_header.setlist("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    post_header.setlist("X-Requested-With", "XMLHttpRequest")

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


    def parse_download(self, response):
        response.meta['item']['download_url'] = json.loads(response.body)['obj']
        yield response.meta['item']

    def _get_download_post_body(self, xpath_node):
        download_args_str = xpath_node.xpath('./@onclick').extract()[0].strip()
        start = download_args_str.find('(')
        delimiter = download_args_str.find(',')
        end = download_args_str.find(')')
        return "id="+ download_args_str[start+1:delimiter] + "&pf=" + download_args_str[delimiter+1:end]

    def _get_detail_image_url(self, xpath_node):
        url = []
        for node in xpath_node.xpath('./li'):
            try:
                url.append(node.xpath('./img/@src').extract()[0].strip()[0:-5])
            except:
                url.append(node.xpath('./iframe/@src').extract()[0].strip()[0:-5])
        return url

    def _get_tags(self, xpath_node):
        tags = []
        for node in xpath_node.xpath('./p'):
            tags.append(node.xpath('./text()').extract()[0].strip())
        return tags


    def _get_app_type(self, xpath_node):
        value = ''
        is_begin = True
        for node in xpath_node.xpath('./span[2]/a'):
            if is_begin:
                value += node.xpath('./text()').extract()[0].strip() + '>'
                is_begin = False
            else:
                value += node.xpath('./text()').extract()[0].strip() + ' '
        return value[0:-1]

    def _get_file_size(self, file_size_str):
        value = "-1"
        last = file_size_str.find('M')
        if last == "-1":
            self.logger.error('can not find file size: %s', file_size_str)
        else:
            start = file_size_str.rfind(' ', 0, last)
            value = file_size_str[start + 1: last]
        return value

    def parse(self, response):
        yield Request("http://www.591vr.com/changeplatform.html", method="POST", body="pval=2",
                      dont_filter=True, headers=self.post_header, callback=self.reload_parse)

    def reload_parse(self, response):
        for page_index, url in self.page_urls.items():
            yield Request(url, dont_filter=True, meta={"page_index": page_index}, callback=self.page_parse)

    def page_parse(self, response):
        filename = response.url.split("/")[-2] + str(response.meta['page_index'])
        with open(filename, 'wb') as f:
            f.write(response.body)
        apps = response.xpath('//div[@class="deatils-bd"]')
        for i in range(len(apps)):
            app = apps[i]
            url = "http://www.591vr.com" + app.xpath('./a/@href').extract()[0]
            yield Request(url, dont_filter=True, callback=self.app_parse,
                          meta={"page_index": response.meta['page_index'], "app_index": str(i)})

    def app_parse(self, response):
        item = VrAppItem()
        item['app_index'] = response.meta['app_index']
        item['page_index'] = response.meta['page_index']
        item['os'] = "Android"

        item['name'] = response.xpath('//h3/text()').extract()[0].strip()
        item['publish_date'] = response.xpath('//p[@class="publish-date"]/text()').extract()[1].strip()

        file_size_mb = self._get_file_size(
            response.xpath('//div[@class="tool-s-details clearfix"]/p[@class="file-size"]/text()').extract()[0].strip())
        item['file_size_mb'] = file_size_mb
        item['language'] = response.xpath('//p[@class="tool-language"]/text()').extract()[0].strip()
        try:
            item['developer'] = response.xpath('//p[@class="tool-developer"]/span[2]/text()').extract()[0].strip()
        except:
            item['developer'] = 'empty'
        try:
            item['hardware_support'] =\
                response.xpath('//div[@class="tool-device clearfix"]/p/text()').extract()[0]
        except:
            item['hardware_support'] = 'empty'
        try:
            item['control_device'] =\
                response.xpath('//div[@class="tool-device mt5 clearfix"][1]/p/text()').extract()[0]
        except:
            item['control_device'] = 'empty'
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



