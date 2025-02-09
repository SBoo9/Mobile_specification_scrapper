import scrapy
import pandas as pd



class Mobile_Specs_Spider(scrapy.Spider):
    name="mobiles"

    #Reading csv file
    def start_requests(self):
        df=pd.read_csv('mobile_links.csv')
        base_url="https://www.91mobiles.com"

        for _, row in df.iterrows():
            url= base_url+ row['ref_link']
            yield scrapy.Request(url=url, callback=self.parse, meta={'title':row['Name']})

    def parse(self,response):
        name = response.meta['title']
        rating= response.css('span.ratpt::text').get()
        price = response.css('span.store_prc[data-price]::text').get()
        #processor= response.css('label.spects_text.positive_value::text').get()
        #specs= response.css('label.specs_text.positive_value[title]::text').getall()
        titles=[]
        texts=[]
        labels=response.css('label.specs_txt.positive_value[title]')
        for label in labels:
            title=label.attrib.get('title','').strip()
            text=label.css('::text').get().strip()

            titles.append(title)
            texts.append(text)


        yield{
            'Title':name,
            'Rating': rating,
            'Price' : price,
            'Specification' : titles
        }



