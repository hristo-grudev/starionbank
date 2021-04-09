import scrapy

from scrapy.loader import ItemLoader

from ..items import StarionbankItem
from itemloaders.processors import TakeFirst


class StarionbankSpider(scrapy.Spider):
	name = 'starionbank'
	start_urls = ['https://starionbank.com/About/Who-We-Are/News']

	def parse(self, response):
		post_links = response.xpath('//a[@class="card-border h-100"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="card-text pt-3 pt-lg-5"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//h2/text()').get()

		item = ItemLoader(item=StarionbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
