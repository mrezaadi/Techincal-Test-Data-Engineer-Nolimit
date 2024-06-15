import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = extract_title(soup)
        content = extract_content(soup)
        last_mod_date = extract_last_modified_date(soup)
        categories = extract_categories(soup)
        
        data = {
            'title': title,
            'url': url,
            'content': content,
            'createdAt': last_mod_date,
            'categories': categories
        }
        
        return data
    else:
        print(f"Gagal mengambil halaman: {response.status_code} - {response.reason}")
        return None

def extract_title(soup):
    title_span = soup.find('span', class_='mw-page-title-main')
    if title_span:
        title = title_span.text.strip()
    else:
        title = "Judul tidak ditemukan"
    return title

def extract_content(soup):
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text(strip=True).replace("\n", " ") for p in paragraphs])
    return content

def extract_last_modified_date(soup):
    last_mod_tag = soup.find('li', id='footer-info-lastmod')
    if last_mod_tag:
        last_mod_str = last_mod_tag.get_text(strip=True).replace('This page was last edited on ', '')
        date_str = last_mod_str.split(',')[0]
        time_str = last_mod_str.split(',')[1].split('(')[0].strip()
        timezone_str = last_mod_str.split('(')[1].split(')')[0] if '(' in last_mod_str else 'UTC'
        full_date_str = f"{date_str}, {time_str} ({timezone_str})"
        last_mod_datetime = datetime.strptime(full_date_str, '%d %B %Y, at %H:%M (%Z)')
        last_mod_date = last_mod_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        last_mod_date = "Last modification date not found"
    return last_mod_date

def extract_categories(soup):
    catlinks_div = soup.find('div', id='mw-normal-catlinks')
    categories = []
    if catlinks_div:
        category_items = catlinks_div.find('ul').find_all('li')
        categories = [item.get_text(strip=True) for item in category_items]
    return categories

# List untuk menyimpan data yang diambil
results = []

# Periksa apakah file 'scraped_data.json' sudah ada
if os.path.exists('scraped_data.json'):
    with open('scraped_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
else:
    existing_data = []

# URLs yang akan diambil
urls = [
    "https://en.wikipedia.org/wiki/Proxy_server",
    "https://en.wikipedia.org/wiki/Web_scraping",
    "https://en.wikipedia.org/wiki/Data_engineering",
    "https://en.wikipedia.org/wiki/Social_media"
    ]
# Iterasi melalui setiap URL, lakukan scraping data jika belum ada di existing_data, dan tambahkan hasilnya ke dalam list
index = 1
print("[WIKIPEDIA SCRAPER DIMULAI] ...\n")
for url in urls:
    url_found = False
    for item in existing_data:
        if item['url'] == url:
            print(f"{index}. URL '{url}' sudah diambil sebelumnya.")
            results.append(item)
            url_found = True
            break
    
    if not url_found:
        print(f"{index}. Melakukan scraping data dari: {url}")
        page_data = get_page_content(url)
        
        if page_data:
            print(f"Scraping berhasil untuk {url}")
            results.append(page_data)
            existing_data.append(page_data)  # Append data baru ke existing_data
        else:
            print(f"Gagal melakukan scraping data dari {url}")
    index += 1
    print()

# Simpan hasil ke dalam 'scraped_data.json'
with open('scraped_data.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Data yang diambil telah disimpan di scraped_data.json")
print("\n[WIKIPEDIA SCRAPER SELESAI]")
