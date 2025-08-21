import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import urljoin, urlparse

# Yoruba content-rich websites
seed_urls = [
    'https://www.bbc.com/yoruba',
    'https://www.alaroye.org',
]

visited_links = set()
collected_texts = set()
output_file = 'yoruba_text_data.csv'
progress_file = 'scraper_progress.txt'
max_texts = 500

# Load already collected texts if any
if os.path.exists(output_file):
    df_existing = pd.read_csv(output_file)
    collected_texts.update(df_existing['text'].dropna().tolist())

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ''

def extract_text_from_page(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30]
    except Exception as e:
        print(f"[skip] {url}: {e}")
        return []

def extract_links(soup, base_url):
    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        if is_valid_url(full_url, urlparse(base_url).netloc):
            links.add(full_url)
    return links

def crawl_site(start_url):
    to_visit = {start_url}
    domain = urlparse(start_url).netloc

    while to_visit and len(collected_texts) < max_texts:
        url = to_visit.pop()
        if url in visited_links:
            continue
        print(f"🔗 Visiting: {url}")
        visited_links.add(url)
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Collect text
            new_texts = extract_text_from_page(url)
            for t in new_texts:
                if t not in collected_texts:
                    collected_texts.add(t)
                    print(f"✅ Collected [{len(collected_texts)}]: {t[:60]}...")
                    if len(collected_texts) >= max_texts:
                        break

            # Queue new links
            if len(collected_texts) < max_texts:
                new_links = extract_links(soup, url)
                to_visit.update(new_links - visited_links)

        except Exception as e:
            print(f"[fail] {url}: {e}")

# Main loop
print(f"🌍 Starting deep scrape with {len(collected_texts)} texts already collected...")
for seed in seed_urls:
    crawl_site(seed)
    if len(collected_texts) >= max_texts:
        break

# Save results
df = pd.DataFrame({'text': list(collected_texts)})
df.to_csv(output_file, index=False)
print(f"
🎉 Done! {len(collected_texts)} texts saved to {output_file}")