import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_page_content(url):
    """
    Mengambil konten halaman web dari URL yang diberikan.

    Args:
    - url (str): URL halaman web yang akan diambil kontennya.

    Returns:
    - dict or None: Data halaman web yang telah diambil, termasuk judul, URL, konten, tanggal modifikasi terakhir, dan kategori. Mengembalikan None jika permintaan gagal atau konten tidak dapat diambil.
    """
    # Mengirim permintaan GET ke URL
    response = requests.get(url)
    
    # Memeriksa jika permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Menginisialisasi objek BeautifulSoup untuk parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mengekstrak judul halaman
        title = extract_title(soup)
        
        # Mengekstrak konten utama dari halaman (paragraf)
        content = extract_content(soup)
        
        # Mengekstrak tanggal modifikasi terakhir dari footer halaman
        last_mod_date = extract_last_modified_date(soup)
        
        # Mengekstrak kategori-kategori dari halaman
        categories = extract_categories(soup)
        
        # Menyusun data dalam bentuk dictionary
        data = {
            'title': title,
            'url': url,
            'content': content,
            'createdAt': last_mod_date,
            'categories': categories
        }
        
        return data
    else:
        # Menampilkan pesan jika permintaan tidak berhasil
        print(f"Gagal mengambil halaman: {response.status_code} - {response.reason}")
        return None

def extract_title(soup):
    """
    Ekstrak judul dari halaman web menggunakan objek BeautifulSoup.

    Args:
    - soup (BeautifulSoup): Objek BeautifulSoup yang mewakili halaman web.

    Returns:
    - str: Judul halaman web atau string default "Judul tidak ditemukan" jika judul tidak ditemukan.
    """
    # Mencari elemen span dengan class mw-page-title-main yang berisi judul
    title_span = soup.find('span', class_='mw-page-title-main')
    
    # Mengambil teks judul jika ditemukan, jika tidak, mengembalikan string default
    if title_span:
        title = title_span.text.strip()
    else:
        title = "Judul tidak ditemukan"
    return title

def extract_content(soup):
    """
    Ekstrak konten teks dari paragraf pada halaman web menggunakan objek BeautifulSoup.

    Args:
    - soup (BeautifulSoup): Objek BeautifulSoup yang mewakili halaman web.

    Returns:
    - str: Konten teks dari halaman web, disatukan dan dibersihkan dari karakter tambahan.
    """
    # Mencari semua elemen paragraf pada halaman
    paragraphs = soup.find_all('p')
    
    # Menggabungkan teks dari setiap paragraf dan membersihkannya dari karakter tambahan
    content = ' '.join([p.get_text(strip=True).replace("\n", " ") for p in paragraphs])
    return content

def extract_last_modified_date(soup):
    """
    Ekstrak tanggal terakhir modifikasi dari halaman web menggunakan objek BeautifulSoup.

    Args:
    - soup (BeautifulSoup): Objek BeautifulSoup yang mewakili halaman web.

    Returns:
    - str: Tanggal modifikasi terakhir dalam format ISO 8601 (misalnya, 'YYYY-MM-DDTHH:MM:SSZ') atau string default "Last modification date not found" jika tanggal tidak ditemukan.
    """
    # Mencari elemen footer-info-lastmod yang berisi informasi terakhir modifikasi
    last_mod_tag = soup.find('li', id='footer-info-lastmod')
    
    # Mengambil tanggal modifikasi jika ditemukan
    if last_mod_tag:
        # Mengambil teks informasi modifikasi terakhir
        last_mod_str = last_mod_tag.get_text(strip=True).replace('This page was last edited on ', '')
        
        # Memisahkan tanggal dan waktu dari informasi yang diambil
        date_str = last_mod_str.split(',')[0]
        time_str = last_mod_str.split(',')[1].split('(')[0].strip()
        
        # Mengambil zona waktu jika tersedia, jika tidak, menggunakan default UTC
        timezone_str = last_mod_str.split('(')[1].split(')')[0] if '(' in last_mod_str else 'UTC'
        
        # Menggabungkan informasi dalam format lengkap
        full_date_str = f"{date_str}, {time_str} ({timezone_str})"
        
        # Mengubah format string ke objek datetime
        last_mod_datetime = datetime.strptime(full_date_str, '%d %B %Y, at %H:%M (%Z)')
        
        # Mengubah format datetime ke ISO 8601 dan mengembalikan sebagai string
        last_mod_date = last_mod_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        # Mengembalikan string default jika informasi tanggal tidak ditemukan
        last_mod_date = "Last modification date not found"
    return last_mod_date

def extract_categories(soup):
    """
    Ekstrak kategori-kategori dari halaman web menggunakan objek BeautifulSoup.

    Args:
    - soup (BeautifulSoup): Objek BeautifulSoup yang mewakili halaman web.

    Returns:
    - list: Daftar kategori-kategori dari halaman web atau list kosong jika tidak ditemukan kategori.
    """
    # Mencari div dengan id mw-normal-catlinks yang berisi daftar kategori
    catlinks_div = soup.find('div', id='mw-normal-catlinks')
    categories = []
    
    # Jika div ditemukan
    if catlinks_div:
        # Mencari elemen ul (daftar kategori) di dalamnya
        category_items = catlinks_div.find('ul').find_all('li')
        
        # Mengambil teks dari setiap item kategori dan memasukkannya ke dalam daftar categories
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
    "https://en.wikipedia.org/wiki/Social_media",
    "https://en.wikipedia.org/wiki/Social_media"
]

# Iterasi melalui setiap URL, lakukan scraping data jika belum ada di existing_data, dan tambahkan hasilnya ke dalam list
index = 1
print("[WIKIPEDIA SCRAPER DIMULAI] ...\n")
for url in urls:
    url_found = False
    
    # Periksa setiap item dalam existing_data
    for item in existing_data:
        if item['url'] == url:
            print(f"{index}. URL '{url}' sudah diambil sebelumnya.")
            results.append(item)
            url_found = True
            break
    
    # Jika URL belum pernah diambil sebelumnya, lakukan scraping data dari URL tersebut
    if not url_found:
        print(f"{index}. Melakukan scraping data dari: {url}")
        page_data = get_page_content(url)
        
        # Jika scraping berhasil, tambahkan data ke results dan existing_data
        if page_data:
            print(f"Scraping berhasil untuk {url}")
            results.append(page_data)
            existing_data.append(page_data)  # Append data baru ke existing_data
        else:
            print(f"Gagal melakukan scraping data dari {url}")
    
    # Tambahkan baris kosong untuk memisahkan setiap iterasi URL
    print()
    index += 1

# Simpan hasil ke dalam 'scraped_data.json'
with open('scraped_data.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Data yang diambil telah disimpan di scraped_data.json")
print("\n[WIKIPEDIA SCRAPER SELESAI]")
