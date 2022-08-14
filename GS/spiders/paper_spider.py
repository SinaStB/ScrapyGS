import scrapy
import csv
import os
import datetime, pytz
import logging
import codecs

logging.disable('WARNING')

class paper_spider(scrapy.Spider):
    name = 'gsp'

    #this url will return html files (each Information Systems scholar) from Google Scholar website
    start_urls = ['https://scholar.google.com/citations?user=JSFG_zIAAAAJ&hl=en', 'https://scholar.google.com/citations?hl=en&user=v85lvpkAAAAJ']

    def parse(self, response):
        print(response.url)
        #storing local time of request and making a file name using it
        now = pytz.timezone("America/Chicago").localize(datetime.datetime.now())
        file_name = "each IS scholars_GS" + now.strftime("%Y-%m-%d") + ".csv"

        #making the output file (if it doesn't exist already), naming it and writting the header row in it
        if os.path.exists(file_name):
            out_file = open(file_name, 'a', newline='', encoding="utf-8", errors='ignore')
            csv_writer = csv.writer(out_file)
        else:
            out_file = open(file_name, 'w', newline='', encoding="utf-8", errors='ignore')
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['scholar','title','paper_url','year','co-authors','journal','Cited By','cited_urls'])

        #requesting HTML elements to fill the csv
        for paper in response.css("tr.gsc_a_tr"):
            title = paper.css('td.gsc_a_t a::text').get()
            paper_url = 'https://scholar.google.com/' + paper.css('td.gsc_a_t a::attr(href)').get()
            coauthors = paper.css('div.gs_gray::text')[0].get()
            journal = paper.css('div:nth-of-type(2).gs_gray::text').get()
            cby = paper.css('td.gsc_a_c a::text').get()
            cby_urls = paper.css('td.gsc_a_c a::attr(href)').get()
            year = paper.css('td.gsc_a_y span::text').get()
            sch_name = response.css('div#gsc_prf_in::text').get()
            csv_writer.writerow([sch_name,title,paper_url,year,coauthors,journal,cby,cby_urls])

        # #getting url from next button and turn it into usable url
        # next_page = response.url.split('?')[0] + '?' + response.css('.gs_btnPR::attr(onclick)').get().split('?')[1]
        # next_page = next_page.replace("'", "")
        # next_page = codecs.decode(next_page, 'unicode-escape')

        # if next_page is None:
        #     print('No page left')
        # else:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        #closing the opened file
        out_file.close()
