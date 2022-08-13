import scrapy
import urllib
from scrapy import Selector

class ScholarSpider(scrapy.Spider):
    name = 'schs'
    allowed_domains = ['scholar.google.com']
    start_url = 'https://scholar.google.com/citations?'

    params = {
        'hl': 'en',
        'user': 'C-7sFjEAAAAJ',
        'view_op': 'list_works',
        'sortby': 'pubdate',
        'cstart': 0,
        'pagesize': '100'
    }
    custom_settings = {"FEEDS":{'items.json': {
        'format': 'json',
        'encoding': 'utf8',
    }}}

    def start_requests(self):
        req_url = f"{self.start_url}{urllib.parse.urlencode(self.params)}"
        yield scrapy.FormRequest(req_url,formdata={'json':'1'},callback=self.parse)


    def parse(self, response):
        if not response.json()['B']:
            return

        resp = Selector(text=response.json()['B'])
        for item in resp.css("tr > td > a[href^='/citations']::attr(href)").getall():
            inner_link = f"https://scholar.google.com{item}"
            yield scrapy.Request(inner_link,callback=self.parse_content)

        self.params['cstart']+=100
        req_url = f"{self.start_url}{urllib.parse.urlencode(self.params)}"
        yield scrapy.FormRequest(req_url,formdata={'json':'1'},callback=self.parse)


    def parse_content(self,response):
        content = {
            'authors': response.css(".gsc_oci_field:contains('Author') + .gsc_oci_value::text").get(),
            'journal': response.css(".gsc_oci_field:contains('Journal') + .gsc_oci_value::text").get(),
            'date': response.css(".gsc_oci_field:contains('Publication date') + .gsc_oci_value::text").get(),
            'abstract': response.css("#gsc_oci_descr .gsh_csp::text").get()
        }
        yield content