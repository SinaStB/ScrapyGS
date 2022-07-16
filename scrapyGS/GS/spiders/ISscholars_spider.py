import scrapy
import csv
import os

class scholarspider(scrapy.Spider):
    name = 'IS_scholars'

    start_urls = ['https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:information_systems']

    def parse(self, response):

        scholars = response.css("div.gsc_1usr")

        for scholar in scholars:
            #scholar_names = scholars.css('a.gs_ai_name::text').get()
            print(scholar)
