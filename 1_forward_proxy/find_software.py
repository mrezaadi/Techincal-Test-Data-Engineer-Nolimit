import requests
from bs4 import BeautifulSoup

# Fungsi untuk mengambil konten HTML melalui proxy
def fetch_html_via_proxy(url, proxy):
    # Menetapkan proxy untuk HTTP dan HTTPS
    proxies = {
        'http': proxy,
        'https': proxy
    }
    # Mengirim permintaan GET ke URL melalui proxy
    response = requests.get(url, proxies=proxies)
    # Mengembalikan konten respons
    return response.content

# Fungsi untuk menghapus dan menghitung kemunculan kata dalam HTML
def remove_and_count_occurrences(html_content, word):
    # Menggunakan BeautifulSoup untuk mem-parse konten HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # Mencari elemen body dalam HTML
    body = soup.find('body')
    if body:
        # Menghitung jumlah kemunculan kata yang ditargetkan
        count = body.text.lower().count(word)
        # Mengambil teks dari body
        body = body.get_text()
        # Menghapus semua kemunculan kata yang ditargetkan dari teks body
        body_without_word = body.lower().replace(word, '')
        # Mengembalikan teks yang telah dimodifikasi dan jumlah kemunculan yang dihapus
        return body_without_word.strip(), count
    # Jika elemen body tidak ditemukan, kembalikan None dan 0
    return None, 0

def main():
    # Menetapkan alamat proxy
    proxy = 'http://localhost:9919'
    # Menetapkan URL target
    url = 'https://en.wikipedia.org/wiki/Proxy_server'

    # Mengambil konten HTML melalui proxy
    html_content = fetch_html_via_proxy(url, proxy)

    # Menghapus dan menghitung kemunculan kata "software"
    body_without_software, count_deleted = remove_and_count_occurrences(html_content, 'software')

    if body_without_software:
        # Menampilkan teks yang telah dimodifikasi tanpa kata "software"
        print(body_without_software)

    # Menampilkan jumlah kemunculan kata "software" yang dihapus
    print(f'Number of occurrences of "software" deleted: {count_deleted}')

if __name__ == '__main__':
    main()
