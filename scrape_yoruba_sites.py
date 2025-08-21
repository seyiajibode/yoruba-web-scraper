import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Yorùbá content sources (can be expanded)
urls = [
    'https://yorubanationvoice.com/',
    'https://www.bbc.com/yoruba',
    'https://www.alaroye.org/',
    'https://www.yorubaname.com/',
]

# File to track progress
progress_file = 'scraper_progress.txt'

# Load already scraped texts if any
collected_texts = set()
output_file = 'yoruba_text_data.csv'
if os.path.exists(output_file):
    df_existing = pd.read_csv(output_file)
    collected_texts.update(df_existing['text'].dropna().tolist())

# Load URL progress
start_index = 0
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        try:
            start_index = int(f.read().strip())
        except ValueError:
            start_index = 0

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20]
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return []

count = len(collected_texts)
print(f"Starting with {count} collected texts...")

while True:
    for i in range(start_index, len(urls)):
        url = urls[i]
        print(f"Scraping {url}...")
        texts = extract_text_from_url(url)
        for t in texts:
            if t not in collected_texts:
                collected_texts.add(t)
                count += 1
                if count % 50 == 0:
                    print(f"Collected {count} texts so far...")

        # Save progress every time we finish a URL
        start_index = i + 1
        with open(progress_file, 'w') as f:
            f.write(str(start_index))

        # Save output to CSV
        pd.DataFrame({'text': list(collected_texts)}).to_csv(output_file, index=False)

        # Stop condition (if you want at least 500)
        if count >= 500:
            print("Reached 500+ texts. Continuing until stopped manually...")

    # Reset index to continue looping
    start_index = 0
    with open(progress_file, 'w') as f:
        f.write(str(start_index))

    print("Looping through URLs again. Sleeping for 15 seconds...")
    time.sleep(15)