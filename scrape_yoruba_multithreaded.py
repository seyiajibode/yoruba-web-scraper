import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import concurrent.futures
import time
import os

seed_urls = [
    'https://www.voayoruba.com',
    'https://www.irohinodua.org',
    'https://www.iroyinowuro.com.ng',
    'https://www.awikonko.com.ng',
    'https://www.lidx.org/news/yo/',
]

visited_links = set()
collected_texts = set()
output_file = 'yoruba_text_data.csv'
max_texts = 60000
MAX_THREADS = 20

# Load existing texts
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
        return []

def extract_links(soup, base_url):
    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        if is_valid_url(full_url, urlparse(base_url).netloc):
            links.add(full_url)
    return links

def process_url(url):
    if url in visited_links or len(collected_texts) >= max_texts:
        return [], []
    visited_links.add(url)
    print(f"🔗 {url}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = extract_text_from_page(url)
        new_links = extract_links(soup, url)
        return texts, new_links
    except:
        return [], []

def crawl_multithreaded(start_urls):
    to_visit = set(start_urls)
    while to_visit and len(collected_texts) < max_texts:
        current_batch = list(to_visit)[:MAX_THREADS]
        to_visit -= set(current_batch)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [executor.submit(process_url, url) for url in current_batch]
            for future in concurrent.futures.as_completed(futures):
                texts, new_links = future.result()
                for t in texts:
                    if t not in collected_texts:
                        collected_texts.add(t)
                        print(f"✅ [{len(collected_texts)}] {t[:60]}...")
                for link in new_links:
                    if link not in visited_links:
                        to_visit.add(link)
        time.sleep(2)  # prevent hammering

# Start crawling
print(f"🚀 Starting multithreaded crawl with {len(collected_texts)} texts...")
for seed in seed_urls:
    crawl_multithreaded([seed])
    if len(collected_texts) >= max_texts:
        break

df = pd.DataFrame({'text': list(collected_texts)})
df.to_csv(output_file, index=False)
print(f"🎉 Done! {len(collected_texts)} texts saved to {output_file}")