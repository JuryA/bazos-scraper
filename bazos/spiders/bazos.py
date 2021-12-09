import scrapy
from bazos.items import BazosItem


class BazosSpider(scrapy.Spider):
    name = 'bazos'
    start_urls = ['https://www.bazos.cz/']
    allowed_domains = ['bazos.cz']

    def parse(self, response):
        for category_href in response.xpath('//span[@class="nadpisnahlavni"]/a/@href'):
            category_url = category_href.get()
            yield scrapy.Request(
                url=category_url,
                callback=self.parse_category,
                meta={'category_url': category_url[:-1]}
            )

    def parse_category(self, response):
        for category_el in response.xpath('//div[@class="barvaleva"]/a'):
            url = category_el.xpath('./@href').get()
            yield scrapy.Request(
                url=url if 'bazos' in url else f"{response.meta['category_url']}{url}",
                callback=self.parse_ad,
                meta={'category': category_el.xpath('./text()').get(), 'category_url': response.meta['category_url']}
            )

    def parse_ad(self, response):
        next_page_url = response.xpath('//div[@class="strankovani"]/a[last()]/@href').get()
        yield scrapy.Request(
                url=next_page_url if 'bazos' in next_page_url else f"{response.meta['category_url']}{next_page_url}",
                callback=self.parse_ad,
                meta={'category': response.meta['category'], 'category_url': response.meta['category_url']}
            )
        for ad_el in response.xpath('//div[@class="inzeraty inzeratyflex"]'):
            yield BazosItem(
                title=ad_el.xpath('.//h2[@class="nadpis"]/a/text()').get(),
                content=ad_el.xpath('.//div[@class="popis"]/text()').get(),
                price=ad_el.xpath('.//div[@class="inzeratycena"]/b/text()').get(),
                category=response.meta['category'],
                location=ad_el.xpath('.//div[@class="inzeratylok"]/text()').get(),
                views=ad_el.xpath('.//div[@class="inzeratyview"]/text()').get(),
                url=ad_el.xpath('.//h2[@class="nadpis"]/a/@href').get()
            )

