import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_page_content(url, proxies=None):
    """
    Mengambil konten halaman web dari URL yang diberikan.

    Args:
    - url (str): URL halaman web yang akan diambil kontennya.
    - proxies (dict, optional): Dictionary yang berisi proxy untuk permintaan HTTP dan HTTPS.

    Returns:
    - dict or None: Data halaman web yang telah diambil, termasuk judul, URL, konten, tanggal modifikasi terakhir, dan kategori. Mengembalikan None jika permintaan gagal atau konten tidak dapat diambil.
    """
    # Mengirim permintaan GET ke URL dengan menggunakan proxy jika disediakan
    response = requests.get(url, proxies=proxies)
    
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
    - str: Judul halaman web atau string default "Title not found" jika judul tidak ditemukan.
    """
    # Mencari elemen span dengan class mw-page-title-main yang berisi judul
    title_span = soup.find('span', class_='mw-page-title-main')
    
    # Mengambil teks judul jika ditemukan, jika tidak, mengembalikan string default
    if title_span:
        title = title_span.text.strip()
    else:
        title = "Title not found"
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
    - str: Tanggal modifikasi terakhir dalam format ISO 8601 (misalnya, 'YYYY-MM-DDTHH:MM:SSZ') atau string default "Date not found" jika tanggal tidak ditemukan.
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
        last_mod_date = "Date not found."
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
    
    # Jika div dan ul (daftar kategori) ditemukan
    if (catlinks_div and catlinks_div.find('ul')):
        # Mengambil semua elemen li yang merupakan item kategori
        category_items = catlinks_div.find('ul').find_all('li')
        
        # Mengambil teks dari setiap item kategori dan memasukkannya ke dalam daftar categories
        categories = [item.get_text(strip=True) for item in category_items]
    return categories

def main():
    """
    Fungsi utama untuk menjalankan proses scraping data dari halaman web.

    Menggunakan argumen dari baris perintah untuk URL dan opsional proxy_url.
    Menyimpan data yang telah di-scrape ke dalam file 'scraped_data.json'.
    """
    import sys
    # Memeriksa jumlah argumen yang diberikan dari baris perintah
    if len(sys.argv) < 2:
        print("Penggunaan: python scraper.py [url] [opsional: proxy_url]")
        return
    
    # Mengambil URL dari argumen baris perintah
    url = sys.argv[1]
    
    # Mengambil proxy_url jika disediakan sebagai argumen kedua
    proxy_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Menyiapkan dictionary proxies untuk digunakan jika proxy_url disediakan
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    
    # Muat data yang sudah ada jika tersedia dalam file 'scraped_data.json'
    if os.path.exists('scraped_data.json'):
        with open('scraped_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    # Periksa apakah URL sudah pernah di-scrape sebelumnya
    url_found = False
    for item in existing_data:
        if item['url'] == url:
            print(f"URL '{url}' sudah pernah di-scrape.")
            url_found = True
            break
    
    # Lakukan scraping jika URL belum pernah di-scrape sebelumnya
    if not url_found:
        print(f"Melakukan scraping data dari: {url}")
        # Panggil fungsi get_page_content untuk mengambil data halaman web
        page_data = get_page_content(url, proxies)
        
        # Jika data berhasil diambil, tambahkan ke existing_data dan simpan kembali ke 'scraped_data.json'
        if page_data:
            existing_data.append(page_data)
            
            # Simpan data yang telah di-update ke dalam file JSON
            with open('scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
            print(f"Scraping berhasil untuk {url}")
        else:
            print(f"Gagal melakukan scraping data dari {url}")

if __name__ == "__main__":
    main()
