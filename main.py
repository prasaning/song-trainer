import os
import sys
import time
import glob
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.lyrics_spider import LyricsSpider

def run_scraper():
    print(f"[{datetime.now()}] Starting lyrics scraping...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'data/lyrics_{timestamp}.jsonl'
    settings = get_project_settings()
    settings.set('FEEDS', {output_file: {'format': 'jsonlines'}})
    process = CrawlerProcess(settings)
    process.crawl(LyricsSpider)
    process.start()
    print(f"[{datetime.now()}] Scraping completed!")

def train_model():
    print(f"[{datetime.now()}] Starting model training...")
    data_files = glob.glob('data/lyrics_*.jsonl')
    if not data_files:
        print("No data files found for training")
        return
    os.chdir('training')
    try:
        data_files_str = ' '.join(data_files)
        os.system(f'{sys.executable} train_model.py {data_files_str}')
    finally:
        os.chdir('..')
    print(f"[{datetime.now()}] Model training completed!")

def generate_lyrics(prompt, length=100):
    print(f"[{datetime.now()}] Generating lyrics starting with: {prompt}")
    print("Lyrics generation will be implemented in the next version")
    return f"Generated lyrics based on: {prompt}"

def continuous_operation():
    iteration = 1
    while True:
        print(f"\n=== Iteration {iteration} ===")
        run_scraper()
        train_model()
        if iteration % 5 == 0:
            generate_lyrics("In the city where the lights are bright", length=50)
        print(f"[{datetime.now()}] Sleeping for 6 hours...")
        time.sleep(6 * 60 * 60)
        iteration += 1

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    os.makedirs('training/results', exist_ok=True)
    os.makedirs('training/logs', exist_ok=True)
    try:
        continuous_operation()
    except KeyboardInterrupt:
        print("\nContinuous operation stopped by user")
