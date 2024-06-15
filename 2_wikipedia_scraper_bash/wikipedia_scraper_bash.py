import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_page_content(url, proxies=None):
    response = requests.get(url, proxies=proxies)
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
        print(f"Failed to fetch page: {response.status_code} - {response.reason}")
        return None

def extract_title(soup):
    title_span = soup.find('span', class_='mw-page-title-main')
    if title_span:
        title = title_span.text.strip()
    else:
        title = "Title not found"
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
        last_mod_date = "Date not found."
    return last_mod_date

def extract_categories(soup):
    catlinks_div = soup.find('div', id='mw-normal-catlinks')
    categories = []
    if (catlinks_div and catlinks_div.find('ul')):
        category_items = catlinks_div.find('ul').find_all('li')
        categories = [item.get_text(strip=True) for item in category_items]
    return categories

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scraper.py [url] [optional: proxy_url]")
        return
    
    url = sys.argv[1]
    proxy_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    
    # Load existing data if available
    if os.path.exists('scraped_data.json'):
        with open('scraped_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    # Check if URL has already been scraped
    url_found = False
    for item in existing_data:
        if item['url'] == url:
            print(f"URL '{url}' has already been scraped.")
            url_found = True
            break
    
    # Scrape if not already done
    if not url_found:
        print(f"Scraping data from: {url}")
        page_data = get_page_content(url, proxies)
        if page_data:
            existing_data.append(page_data)
            # Save the updated data
            with open('scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
            print(f"Scraping successful for {url}")
        else:
            print(f"Failed to scrape data from {url}")

if __name__ == "__main__":
    main()
