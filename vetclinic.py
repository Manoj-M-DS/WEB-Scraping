import scrapy


class VetclinicSpider(scrapy.Spider):
    name = 'vetclinic'
    start_urls = ['http://www.findalocalvet.com/']

    def parse(self, response):
        cities = response.css('#SideByCity .itemresult a::attr(href)').getall()
        for city in cities:
            link = response.urljoin(city)
            yield scrapy.Request(link, callback=self.parsecity)


    def parsecity(self, response):
        clinincs = response.css('.org::attr(href)').getall()
        for clinic in clinincs:
            link = response.urljoin(clinic)
            yield scrapy.Request(link, callback=self.parseclinic)
        
        Nextpage = response.css('a.dataheader:contains("Next")::attr(href)').get()
        if Nextpage:
        
           Nextlink = response.urljoin(Nextpage)
           yield scrapy.Request(Nextlink, callback=self.parsecity)        

    def parseclinic(self, response):
        
        yield {
           
           '  Name  ' : response.css('.Results-Header h1::text').get(),
           '  city  ' : response.css('.locality::text').get(),          
           '  state  ' : response.css('.region::text').get(),        
           '  phone  ' : response.css('.Phone::text').get(),
           '  site  ' : response.url,
           }           