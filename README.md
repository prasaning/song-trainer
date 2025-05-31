# Lyrics Generation Ai

This project scrapes song lyrics from the web and trains an AI model to generate new lyrics.

## Project Structure

```
├── scraper/             # Web scraping components
│   ├── spiders/
│   │   └── lyrics_spider.py   # Scrapy spider for lyrics websites
│   ├── items.py         # Data structure for scraped lyrics
│   ├── pipelines.py     # Data processing pipeline
│   └── settings.py      # Scrapy configuration
├── training/            # Model training components
│   └── train_model.py   # Lyrics model training script
├── data/                # Storage for scraped lyrics (created at runtime)
├── main.py              # Main pipeline script
└── requirements.txt     # Python dependencies
```

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure scraping:
- Update `scraper/spiders/lyrics_spider.py` with actual lyrics website URLs
- Modify parsing logic in the `parse` method

## Usage

1. Run the full pipeline:
```bash
python main.py
```

2. The process will:
- Scrape lyrics from configured websites
- Store results in `data/lyrics.jsonl`
- Train the AI model on the collected lyrics
- Generate sample lyrics starting with a prompt

3. To only run scraping:
```bash
cd scraper
scrapy crawl lyrics_spider -o ../data/lyrics.jsonl
```

4. To only train the model:
```bash
cd training
python train_model.py
```

## Customization

- Modify model architecture in `training/train_model.py`
- Adjust training parameters (epochs, batch size, etc.)
- Add data preprocessing in `scraper/pipelines.py`
- Implement lyrics generation interface

## Important Notes

- Respect websites' terms of service and robots.txt
- Add proper error handling and rate limiting
- Consider legal implications of web scraping
- For production use, implement:
  - Distributed scraping
  - Model versioning
  - Continuous training pipeline
  - API endpoint for lyrics generation
