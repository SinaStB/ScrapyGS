import scrapy
from scrapy.linkextractors import LinkExtractor
import csv
import os
import datetime, pytz
import logging
import codecs

logging.disable('WARNING')

class scholarspider(scrapy.Spider):
    name = 'sch'
    # sch_names = []
    # start = 0

    #these urls will return html files with Information Systems scholars from Google Scholar website
    start_urls = ['https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:information_systems',]

    def parse(self, response):
        print(response.url)
        #storing local time of request and making a file name using it
        now = pytz.timezone("America/Chicago").localize(datetime.datetime.now())
        file_name = "IS scholars_GS" + now.strftime("%Y-%m-%d") + ".csv"

        #making the output file (if it does'nt exist already), naming it and writting the header row in it
        if os.path.exists(file_name):
            out_file = open(file_name, 'a')
            csv_writer = csv.writer(out_file)
        else:
            out_file = open(file_name, 'w')
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['name','GS_url','affiliation','citation_count','interests','interests_url'])

        # repeating = False

        #requesting HTML elements to fill the csv
        for scholar in response.css("div.gsc_1usr"):
            sch_name = scholar.css('h3.gs_ai_name a::text').get()
            sch_url = 'https://scholar.google.com/' + scholar.css('div.gs_ai_t a::attr(href)').get()
            aff = scholar.css('div.gs_ai_aff::text').get()
            cby = scholar.css('div.gs_ai_cby::text').get().replace('Cited by', '')
            int = scholar.css('div.gs_ai_int a::text').getall()
            int_url = scholar.css('div.gs_ai_int a::attr(href)').getall()
            csv_writer.writerow([sch_name,sch_url,aff,cby,int,int_url])

        next_page = response.url.split('?')[0] + '?' + response.css('.gs_btnPR::attr(onclick)').get().split('?')[1]
        # next_path = response.css('.gs_btnPR::attr(onclick)').get()
        next_page = next_page.replace("'", "")
        next_page = codecs.decode(next_page, 'unicode-escape')
        print(next_page)
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        #checks for duplicate names
        # if sch_name not in self.sch_names:
        #     csv_writer.writerow([sch_name,sch_url,aff,cby,int,int_url])
        #     self.sch_names.append(sch_name)
        #     self.start += 1
        # else:
        #     repeating = True

        #checks for pagination
        # if len(scholars) >= 10 and not repeating:
        #     url = response.url.split('&start=')[0] + "&start=" + str(self.start)
        #     yield scrapy.Request(
        #         url = url,
        #         callback = self.parse
        #     )
        # else:
        #     print('No page left')

        #closing the opened file
        out_file.close()
