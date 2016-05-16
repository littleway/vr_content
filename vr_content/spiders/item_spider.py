import scrapy
from scrapy.http.request import Request
from scrapy.http import Headers
from vr_content.items import ItemFactory
import json


class ItemSpider(scrapy.Spider):
    name = "item"
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
            yield Request(url, dont_filter=True, callback=self.item_parse,
                          meta={"page_index": response.meta['page_index'], "item_index_in_page": str(i)})

    def item_parse(self, response):
        pass

    def _get_base_parsed_item(self, response):
        item = ItemFactory.create_item(self.name)
        item['item_url'] = response.url
        item['item_index_in_page'] = response.meta['item_index_in_page']
        item['page_index'] = response.meta['page_index']

        item['name'] = response.xpath('//h3/text()').extract()[0].strip()
        item['publish_date'] = self._str_post_process(
            response.xpath('//p[@class="publish-date"]/text()').extract()[1].strip())
        item['file_size_mb'] = self._get_file_size(
            response.xpath('//div[@class="tool-s-details clearfix"]/p[@class="file-size"]/text()').extract()[0].strip())
        item['language'] = self._str_post_process(
            response.xpath('//p[@class="tool-language"]/text()').extract()[0].strip())
        item['version'] = self._str_post_process(
            response.xpath('//p[@class="tool-version"]/text()').extract()[0])
        try:
            item['developer'] =\
                response.xpath('//p[@class="tool-developer"]/span[2]/text()').extract()[0].strip()
        except:
            item['developer'] = 'NULL'
        item['application_type'] = self._get_app_type(
            response.xpath('//div[@class="tool-device mt5 clearfix"][2]'))
        item['tags'] = self._get_tags(response.xpath('//div[@class="tool-type clearfix"]'))
        item['star_rating'] = len(response.xpath('//div[@class="tool-start clearfix"]/ul/li'))
        item['introduce'] = self._str_post_process(
            response.xpath('//div[@id="share_summary"]/text()').extract()[0].strip())
        item['icon_url'] = self._str_post_process(response.xpath('//img[@id="share-pic"]/@src').extract()[0])

        return item
        # post_body = self._get_download_post_body(response.xpath('//ul[@class="type-main clearfix"]/li/a'))
        # yield Request("http://www.591vr.com/downloadApp.html", method="POST", body=post_body,
        #               meta={'item': item}, headers=self.post_header, callback=self.parse_download)

    @staticmethod
    def parse_download(response):
        response.meta['item']['download_url'] = ItemSpider._str_post_process(json.loads(response.body)['obj'])
        yield response.meta['item']

    @staticmethod
    def _str_post_process(src_str):
        field_str = src_str.strip()
        if field_str == "":
            field_str = 'NULL'
        return field_str

    @staticmethod
    def _get_download_post_body(xpath_node):
        download_args_str = xpath_node.xpath('./@onclick').extract()[0].strip()
        start = download_args_str.find('(')
        delimiter = download_args_str.find(',')
        end = download_args_str.find(')')
        return "id=" + download_args_str[start+1:delimiter] + "&pf=" + download_args_str[delimiter+1:end]

    @staticmethod
    def _get_video_url(src_str):
        start = src_str.find('=')
        end = src_str.find('&img')
        return src_str[start+1:end]

    @staticmethod
    def _get_tags(xpath_node):
        tags = []
        for node in xpath_node.xpath('./p'):
            tags.append(
                ItemSpider._str_post_process(
                    node.xpath('./text()').extract()[0].strip()))
        return tags if len(tags) > 0 else "NULL"

    @staticmethod
    def _get_app_type(xpath_node):
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
        if last == -1:
            last = file_size_str.find('G')
            if last == -1:
                self.logger.error('can not find file size: %s', file_size_str)
                value = "0"
            else:
                start = file_size_str.rfind(' ', 0, last)
                value = str(float(file_size_str[start + 1: last]) * 1024)
        else:
            start = file_size_str.rfind(' ', 0, last)
            value = file_size_str[start + 1: last]
        return value
