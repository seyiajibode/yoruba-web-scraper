Yorùbá Web Scraper & Sentiment Labeling Toolkit
Overview
A comprehensive, user-friendly Python toolkit that:

Crawls Yorùbá web content — uses multithreaded scraping to gather text from news and blog sites.

Processes and cleans the data — removes noise, classifies language, and applies tone marks.

Enables manual sentiment labeling — via a lightweight local web interface (Flask app with pagination and skipping).

Perfect for building a Yorùbá dataset ready for NLP tasks like sentiment analysis.

Features
Multithreaded crawler using BeautifulSoup for fast, efficient extraction

Pagination & link-following logic to collect 500+ unique paragraphs

Text cleaning pipelines: remove URLs, hashtags, standardize casing

Language detection: sort content into Yorùbá, English, or mixed

Tone marking: adds diacritics to common Yorùbá words

Auto-tag sentiment using simple seed-word heuristics

Manual annotation UI: local Flask app with Next and Skip features

Prerequisites
Install dependencies with:

pip install -r requirements.txt
Typical libraries:

requests, beautifulsoup4, pandas

flask

Optionally: selenium or playwright for JS-heavy pages

Quick Start
Run the scraper

python scrape_yoruba_multithreaded.py
Collects at least 500 texts and saves them in yoruba_text_data.csv.

Clean and prepare data
python clean_text.py
python detect_language.py
python add_tone_marks.py
Output files appear under results/.

Optional auto-label sentiment


python auto_tag_sentiment.py
Manual labeling via web interface


cd web_labeler
python app.py
Open http://127.0.0.1:5000 — label or skip each entry; results saved in results/labeled_sentiment.csv.

File Structure
yoruba_scraper/
├── scrape_yoruba_multithreaded.py
├── clean_text.py
├── detect_language.py
├── add_tone_marks.py
├── auto_tag_sentiment.py
├── results/
│   ├── cleaned_data.csv
│   ├── data_with_language_info.csv
│   ├── data_with_tone_marks.csv
│   ├── auto_tagged_sentiment.csv
│   └── labeled_sentiment.csv
└── web_labeler/
    ├── app.py
    └── templates/label.html
Best Practices & Ethical Scraping
Respect robots.txt — follow the site’s crawl rules 
pitt.libguides.com

Throttle requests — use delays or randomized intervals to avoid overloading servers

Use valid headers/user agents — inhibits detection and blocking 

Persist data continuously to prevent data loss during crashes 

Logging — helpful for diagnosing issues with failed requests or parsing 

Avoid scraping sensitive or copyrighted content — always check Terms of Service
Medium

Why This Matters
This tool helps build high-quality Yorùbá datasets with minimal effort—ideal for researchers or developers in low-resource NLP settings. The tool is modular: each stage can be customized or extended easily.

What’s Next?
Add paid API or proxy rotation for heavy loads

Expand language detection accuracy

Export labeled data in JSONL or dataset-ready formats
