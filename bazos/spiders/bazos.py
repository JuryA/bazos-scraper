import scrapy
from bazos.items import BazosItem


class BazosSpider(scrapy.Spider):
    name = 'bazos'
    start_urls = ['https://www.bazos.cz/']
    allowed_domains = ['bazos.cz']

    def parse(self, response):
        for categoryUrl in response.xpath('//span[@class="nadpisnahlavni"]/a/@href'):
            categoryUrl = categoryUrl.get()
            yield scrapy.Request(
                url=categoryUrl,
                callback=self.parse_category,
                meta={'categoryUrl': categoryUrl}
            )

    def parse_category(self, response):
        for categoryEl in response.xpath('//div[@class="barvaleva"]/a'):
            url = categoryEl.xpath('./@href').get()
            yield scrapy.Request(
                url=url if 'bazos' in url else f"{response.meta['categoryUrl'][:-1]}{url}",
                callback=self.parse_ad,
                meta={'category': categoryEl.xpath('./text()').get()}
            )

    def parse_ad(self, response):
        for adEl in response.xpath('//div[@class="inzeraty inzeratyflex"]'):
            yield BazosItem(
                title=adEl.xpath('.//h2[@class="nadpis"]/a/text()').get(),
                content=adEl.xpath('.//div[@class="popis"]/text()').get(),
                price=adEl.xpath('.//div[@class="inzeratycena"]/b/text()').get(),
                category=response.meta['category']
            )

