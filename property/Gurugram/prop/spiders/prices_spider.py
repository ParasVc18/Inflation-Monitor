import scrapy
import re
import pandas as pd
from datetime import date
today = date.today()
class PropSpider(scrapy.Spider):
    name="prop"
    DOWNLOAD_DELAY=1
    start_urls=[
            'https://www.99acres.com/property-in-gurgaon-ffid?orig_property_type=23&search_type=QS&search_location=CP1&np_layout=xid_property_layout'
    ]
    def parse(self, response):
        for property in response.xpath('//div[@title="View Property Details"]'):
            price= property.xpath('.//span[@class="srpNw_price "]/text()').get()
            area= property.xpath('.//td[@class="_auto_areaValue"]/b/text()').get()
            sq=  property.xpath('.//td[@class="_auto_areaValue"]/span/text()').get()
            kind= property.xpath('.//td[@class="_auto_areaType"]/text()').get()
            address= property.xpath('.//th[@class="_srpttl"]/a/span/b/text()').get()
            society= property.xpath('.//a[@class="sName"]/b/text()').get()
            bhk= property.xpath('.//td[@class="_auto_bedroom"]/b/text()').get()
            config= property.xpath('.//td[@class="_auto_bath_balc_roadText"]/text()').get()
            avail= property.xpath('.//td[@class="_auto_possesionLabel"]/text()').get()
            psf= property.xpath('.//td[@class="_auto_ppu_area"]/text()').get()
            df=pd.DataFrame({
                            "price":[price],
                            "area":[area],
                            "psf":[psf],
                            "sq":[sq],
                            "kind":[kind],
                            "address":[address],
                            "society":[society],
                            "bhk":[bhk],
                            "config":[config],
                            "avail":[avail],
                            "date":[today]
                            })
            for index, row in df.iterrows():
                a=row["area"]
                b=str(a)
                b=b.split(" ")
                row["area"]=b[0]
                c=row["psf"]
                d=str(c)
                d=d.split("/")
                row["psf"]=d[0]
                s=str(row["price"])
                row["price"]=s[2:]
                if(str(row["psf"])!="None"):
                    if (str(row["sq"])=="Sq. Yards"):
                        row["area"]=9*float(row["area"])
                        row["psf"]=float(row["psf"])/9
                    elif (str(row["sq"])=="Sq. Meter"):
                        row["psf"]=float(row["psf"])/10.76
                        row["area"]=10.76*float(row["area"])
                    elif (str(row["sq"])=="Acres"):
                        row["area"]=43560*float(row["area"])
                        row["psf"]=float(row["psf"])/43560
                y=row["price"]
                x=str(y)
                x=x.split(" - ")
                x=x[0]
                if (re.findall("L\Z",x)):
                    x=x.split(" L")
                    row["price"]=int(float(x[0])*100000)
                elif (re.findall("Cr\Z",x)):
                    x=x.split(" Cr")
                    row["price"]=int(float(x[0])*10000000)
            df["availability"]=df["avail"].str.strip()
            df["configuration"]=df["config"].str.strip()
            for index, row in df.iterrows():
                yield{
                    "price":row["price"],
                    "area":row["area"],
                    "psf":row["psf"],
                    "kind":row["kind"],
                    "address":row["address"],
                    "society":row["society"],
                    "bhk":row["bhk"],
                    "config":row["configuration"],
                    "avail":row["availability"],
                    "date":row["date"]
                }
        next_page = response.xpath('//a[@class="pgselActive"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
