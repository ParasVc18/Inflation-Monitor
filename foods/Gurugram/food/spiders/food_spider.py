import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import date
today = date.today()
class food(scrapy.Spider):
    name = "food"
    start_urls = ['https://www.foodpanda.in/restaurants/city/gurgaon?currentUrl=https%3A%2F%2Fwww.foodpanda.in%2Frestaurants%2Fcity%2Fgurgaon&user_search=&sort=&sort=&page=1']
    BASE_URL= 'https://www.foodpanda.in'
    def parse(self, response):
        num=1
        for restaurant in response.xpath('//a[contains(@class,"vendor__inner")]/@href'):
            url=self.BASE_URL+restaurant.get()
            yield scrapy.Request(url, callback = self.parse_dir_contents)

        next_page='https://www.foodpanda.in/restaurants/city/gurgaon?currentUrl=https%3A%2F%2Fwww.foodpanda.in%2Frestaurants%2Fcity%2Fgurgaon&user_search=&sort=&sort=&page={num}'
        if num < 80:
            num=num+1
            yield response.follow(next_page, callback=self.parse)

    def parse_dir_contents(self,response):
        for item in response.xpath('//div[@class="menu-item__content-wrapper"]'):
            restaurant= response.xpath('//span[@itemprop="title"]/text()')[2].get()
            items= item.xpath('.//div[@class="menu-item__title"]/text()').get()
            price= item.xpath('.//div[@class="menu-item__variation__price "]/text()').get()
            df = pd.DataFrame({
                                "restaurant":[restaurant],
                                "items":[items],
                                "price":[price],
                                "date":[today]
                            })
            df["Restaurant"]=df["restaurant"].str.strip()
            df["ItemName"]=df["items"].str.strip()
            df["Cost"]=df["price"].str.strip()
            s=df["Cost"]
            a=str(s)
            a=a.split(".")
            df["Coster"]=float(a[1])
            for index, row in df.iterrows():
                yield{
                    "restaurant":row["Restaurant"],
                    "items":row["ItemName"],
                    "price":row["Coster"],
                    "date":row["date"],
                    }
