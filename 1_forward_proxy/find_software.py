import requests
from bs4 import BeautifulSoup

def fetch_html_via_proxy(url, proxy):
    """
    Mengambil konten HTML dari URL menggunakan proxy yang ditentukan.

    Args:
    - url (str): URL yang akan diambil kontennya.
    - proxy (str): Alamat proxy yang akan digunakan (format 'http://host:port').

    Returns:
    - bytes: Konten HTML dalam bentuk bytes jika permintaan berhasil, None jika gagal.
    """
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        # Mengirim permintaan GET ke URL menggunakan proxy
        response = requests.get(url, proxies=proxies)
        return response.content
    except requests.exceptions.RequestException as e:
        # Menangani kesalahan jika permintaan gagal
        print(f'Error fetching {url} via proxy {proxy}: {str(e)}')
        return None

def remove_and_count_occurrences(html_content, word):
    """
    Menghapus semua kemunculan kata yang ditargetkan dari teks HTML dan menghitung kemunculannya.

    Args:
    - html_content (bytes): Konten HTML dalam bentuk bytes.
    - word (str): Kata yang akan dihapus dan dihitung kemunculannya dalam teks.

    Returns:
    - tuple: Dua elemen tuple yang berisi teks HTML yang telah dimodifikasi dan jumlah kemunculan kata yang dihapus. 
    (None, 0) jika tidak dapat menemukan elemen 'body' dalam HTML.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    if body:
        # Menghitung jumlah kemunculan kata yang ditargetkan
        count = body.text.lower().count(word)
        body_text = body.get_text()
        # Menghapus semua kemunculan kata yang ditargetkan dari teks body
        body_without_word = body_text.lower().replace(word, '')
        return body_without_word.strip(), count
    # Mengembalikan None dan 0 jika elemen 'body' tidak ditemukan
    return None, 0

def main():
    """
    Fungsi utama untuk mengambil konten HTML dari sebuah URL melalui proxy, 
    menghapus dan menghitung kemunculan kata "software" dalam teks HTML, 
    serta menampilkan hasilnya.
    """
    proxy = 'http://localhost:9919'
    url = 'https://en.wikipedia.org/wiki/Proxy_server'

    # Mengambil konten HTML dari URL menggunakan proxy
    html_content = fetch_html_via_proxy(url, proxy)

    if html_content:
        # Menghapus dan menghitung kemunculan kata "software" dalam teks HTML
        body_without_software, count_deleted = remove_and_count_occurrences(html_content, 'software')

        if body_without_software:
            print(body_without_software)

        # Menampilkan jumlah kemunculan kata "software" yang dihapus
        print(f'Jumlah kemunculan "software" yang dihapus: {count_deleted}')
    else:
        print(f'Gagal mengambil HTML dari {url} melalui proxy {proxy}')

if __name__ == '__main__':
    main()
