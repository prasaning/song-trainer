import scrapy
import re
from bs4 import BeautifulSoup
from ..items import LyricsItem

class LyricsSpider(scrapy.Spider):
    name = 'lyrics_spider'
    start_urls = [
        'https://www.lyrics.com/random.php',
        'https://www.azlyrics.com/'
    ]
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
    }

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics = self.extract_lyrics(soup)
        if not lyrics:
            return
        title = self.extract_title(soup, response.url)
        artist = self.extract_artist(soup, response.url)
        genre = self.extract_genre(soup)
        item = LyricsItem()
        item['title'] = title
        item['artist'] = artist
        item['lyrics'] = lyrics
        item['genre'] = genre
        item['source_url'] = response.url
        item['language'] = 'English'
        yield item
        for link in soup.find_all('a', href=True):
            href = link['href']
            if self.is_lyrics_link(href):
                yield response.follow(href, self.parse)

    def extract_lyrics(self, soup):
        containers = [
            {'id': 'lyric-body-text'},
            {'class': 'lyricsh'},
            {'class': re.compile(r'\blyrics\b')},
            {'id': re.compile(r'\blyrics\b')},
            {'class': re.compile(r'\btext\b')},
            {'id': re.compile(r'\btext\b')},
        ]
        for pattern in containers:
            container = soup.find('div', pattern)
            if container:
                text = container.get_text()
                text = re.sub(r'\s+', ' ', text).strip()
                return text
        return None

    def extract_title(self, soup, url):
        title = None
        title_selectors = [
            'h1#lyric-title',
            'h1', 'h2', 'title'
        ]
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                break
        if not title:
            if 'azlyrics.com' in url:
                parts = url.split('/')
                if len(parts) > 5:
                    title = parts[-1].replace('.html', '').replace('-', ' ').title()
        return title or "Unknown"

    def extract_artist(self, soup, url):
        artist = None
        artist_selectors = [
            'h2 a.lyric-artist',
            'h2 a', 'div.artist'
        ]
        for selector in artist_selectors:
            element = soup.select_one(selector)
            if element:
                artist = element.get_text().strip()
                break
        if not artist:
            if 'azlyrics.com' in url:
                parts = url.split('/')
                if len(parts) > 4:
                    artist = parts[4].replace('.html', '').replace('-', ' ').title()
        return artist or "Unknown"

    def extract_genre(self, soup):
        genre_selectors = [
            'a[href*="/genre/"]',
            'a[href*="/style/"]',
            'div.genre'
        ]
        for selector in genre_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return "Unknown"

    def is_lyrics_link(self, href):
        patterns = [
            r'/lyric/',
            r'/lyrics/',
            r'/song/',
            r'\.html$',
            r'\.php\?'
        ]
        return any(re.search(p, href) for p in patterns)
