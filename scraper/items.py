import scrapy

class LyricsItem(scrapy.Item):
    title = scrapy.Field()
    artist = scrapy.Field()
    lyrics = scrapy.Field()
    genre = scrapy.Field()
    source_url = scrapy.Field()
    language = scrapy.Field()
    year = scrapy.Field()
