---

# Techincal Test Data Engineer - Nolimit

Repository ini dibuat oleh Muhammad Reza Adi Nugraha dalam rangka menjawab Techincal Test Data Engineer di perusahaan Nolimit. Repository ini terdiri dari tiga folder, masing-masing digunakan untuk menjawab setiap soal yang diberikan.

## Struktur Repository

- **1_forward_proxy**: Berisi kode untuk menjalankan forward proxy dan melakukan scraping HTML menggunakan proxy.
- **2_wikipedia_scraper_bash**: Berisi skrip Bash untuk melakukan scraping Wikipedia melalui proxy.
- **3_wikipedia_scraper_links**: Berisi skrip Python untuk melakukan scraping pada sejumlah link Wikipedia yang sudah ditentukan.

## 1_forward_proxy

Folder ini berisi kode untuk menjalankan forward proxy dan melakukan scraping HTML menggunakan proxy yang telah berjalan. Berikut adalah cara menggunakan folder ini:

### Cara Menggunakan

1. Jalankan file `proxy.py` dengan cara:

   ```bash
   python proxy.py
   ```

2. Buka terminal baru dan jalankan beberapa command line untuk melakukan scraping HTML menggunakan proxy yang telah berjalan. Contohnya:

   ```bash
   curl -x http://localhost:9919 https://google.com/search -vvv
   curl -x http://localhost:9919 https://en.wikipedia.org/wiki/Proxy_server -vvv
   ```

3. Untuk menghapus kata "software" pada respon HTML dan menghitung jumlah kemunculan kata "software", jalankan file `find_software.py` dengan cara:

   ```bash
   python find_software.py
   ```

### Gambar Contoh Hasil Running
Terminal file proxy.py
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/82148b4d-6943-4909-9d9e-06ad112d67b1)

Terminal find_software.py
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/de4a55d8-4652-4d90-bf7b-4824cde4b68b)

Terminal curl
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/29c7fd6c-4240-4ba9-8ce5-bcada91d8d10)

## 2_wikipedia_scraper_bash

Folder ini berisi skrip Bash untuk melakukan scraping Wikipedia melalui proxy. Berikut adalah cara menggunakan folder ini:

### Cara Menggunakan

1. Jalankan file `proxy.py` dengan cara:

   ```bash
   python proxy.py
   ```

2. Buka terminal Bash dan jalankan command line untuk melakukan scraping Wikipedia dengan contoh sebagai berikut:

   ```bash
   ./run_scraper.sh "https://en.wikipedia.org/wiki/Proxy_server"
   ./run_scraper.sh "https://en.wikipedia.org/wiki/Web_scraping"
   ./run_scraper.sh "https://en.wikipedia.org/wiki/Data_engineering" "http://localhost:9919"
   ./run_scraper.sh "https://en.wikipedia.org/wiki/Social_media" "http://localhost:9919"
   ```

### Gambar Contoh Hasil Running
Terminal file proxy.py
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/38c98fa6-8398-45db-9d36-6490f318acdc)

Terminal bash
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/a2a359c7-b114-4406-abb1-6dc50034d0b9)

File json
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/3f861887-208f-4bf4-9f76-82bd6ed27c46)

## 3_wikipedia_scraper_links

Folder ini berisi skrip Python untuk melakukan scraping pada sejumlah link Wikipedia yang sudah ditentukan. Berikut adalah cara menggunakan folder ini:

### Cara Menggunakan

1. Kumpulan link sudah tersedia di dalam source code.
2. Jalankan file `wikipedia_scraper_links.py` dengan cara:

   ```bash
   python wikipedia_scraper_links.py
   ```

### Gambar Contoh Hasil Running
Terminal wikipedia_scraper_links.py
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/88735b0c-b701-4400-b3c3-cb64200fabc1)

File json
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer-Nolimit/assets/68578433/a6e1676f-b915-48c3-8c08-f5a762adbd7c)

# Batasan dan Asumsi :

Scraper Wikipedia ini mengambil data dengan memanfaatkan tag HTML dari halaman https://en.wikipedia.org/wiki/{judul_artikel}. Oleh karena itu, untuk setiap halaman yang berbeda, perlu disesuaikan pengambilan data berdasarkan tag HTML yang digunakan.
---

