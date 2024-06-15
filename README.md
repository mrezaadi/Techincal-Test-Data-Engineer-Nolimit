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
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/475e61c7-22a1-4c27-bfa8-3bb4e4c0b8c9)

Terminal find_software.py
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/c1cbc503-c9e0-442c-b719-9e26cc734036)

Terminal curl
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/b11e03a6-44cd-4326-a672-6c6ae4f65cfc)



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
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/de3d0a55-9163-4e65-9d80-2b90d510a8a9)

Terminal bash
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/9a35d4ad-6ed0-466f-bef7-32996741d844)

File json
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/2004ec7c-2a54-4eaf-9e88-02be13381848)



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
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/3b28354d-4252-4d28-80a6-20865653341d)

File json
![image](https://github.com/mrezaadi/Techincal-Test-Data-Engineer---Nolimit/assets/68578433/cca7a24b-fec2-4454-b08d-f10e7d550f48)


---

