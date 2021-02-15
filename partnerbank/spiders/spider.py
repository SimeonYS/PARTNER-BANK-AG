import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import PartnerbankItem

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.partnerbank.at/presse',
                  'https://www.partnerbank.at/news'
                  ]

    def parse(self, response):
        links = response.xpath('//header/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(PartnerbankItem())
        item.default_output_processor = TakeFirst()

        date = response.xpath('//span[contains(@class, "date")]/text()').get()
        title = ''.join(response.xpath('//h3[@class="post--title"]/text()|//h2//text()').getall())
        content = [text for text in response.xpath('//div[@class="page--description"]//text()|//div[@class="text"]/p//text()|//div[@class="text"]//ul//text()').getall() if text.strip()]
        content = re.sub(pattern, "", ''.join(content))


        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()