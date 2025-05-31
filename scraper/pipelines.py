import os
import json
import re
from datetime import datetime
from .items import LyricsItem

class LyricsPipeline:
    def __init__(self):
        os.makedirs('../data', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f'../data/lyrics_{timestamp}.jsonl'
        self.seen_items = set()

    def process_item(self, item, spider):
        if not isinstance(item, LyricsItem):
            return item
        item_id = f"{item['artist']}_{item['title']}".lower().replace(' ', '_')
        if item_id in self.seen_items:
            spider.logger.info(f"Skipping duplicate: {item['title']} by {item['artist']}")
            return item
        self.seen_items.add(item_id)
        lyrics = self.clean_lyrics(item['lyrics'])
        if not lyrics:
            spider.logger.info(f"Skipping empty lyrics: {item['title']} by {item['artist']}")
            return item
        item['lyrics'] = lyrics
        item['title'] = self.clean_text(item['title'])
        item['artist'] = self.clean_text(item['artist'])
        item['genre'] = self.clean_text(item['genre'])
        with open(self.output_file, 'a', encoding='utf-8') as f:
            line = json.dumps(dict(item), ensure_ascii=False)
            f.write(line + '\n')
        spider.logger.info(f"Processed: {item['title']} by {item['artist']}")
        return item

    def clean_lyrics(self, text):
        if not text:
            return None
        text = re.sub(r'\[.*?\]\s*', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) < 50:
            return None
        return text

    def clean_text(self, text):
        if not text:
            return "Unknown"
        text = re.sub(r'\s+', ' ', text).strip()
        return text.title()
