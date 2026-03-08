## News Scraper Application
Aplikasi scraping berita berbasis GUI yang dibangun menggunakan Python, PyQt5, dan Selenium. Aplikasi ini memungkinkan pengguna untuk mengambil artikel berita dari berbagai website berita secara otomatis, lengkap dengan filter tanggal, progress bar, dan fitur export data.

## Teknologi yang digunakan
- Bahasa        : Python 
- GUI           : PyQt5
- Web Scraping  : Selenium (chromedriver)
- Export Data   : Pandas, XlsxWriter
- Threading     : QThread (PyQt5)
- Date Parsing  : python-dateutil

## Cara Install
### 1. Clone repositori
  -  git clone https://github.com/syqlladp/News-Scraper-kel4.git
  -  cd News-Scraper-kel4
### 2. Install Dependencies
   pip install -r requirements.txt

## Cara Menjalankan
ketik "python main.py"

## Panduan Penggunaan
Langkah-langkah:
### 1. Masukkan URL :
  Isi kolom "URL Berita" dengan link halaman kategori  berita.
  Contoh: https://tekno.kompas.com
  Contoh: https://health.kompas.com
  Contoh: https://news.detik.com
### 2. Set Limit Artikel :
   Tentukan berapa banyak artikel yang ingin di-scrape (default: 20).
### 3. Set Delay :
   Atur jeda antar request dalam detik (default: 2 detik, disarankan minimal 2).
### 4. Set Rentang Tanggal :
   Pilih Start Date dan End Date untuk memfilter artikel berdasarkan tanggal terbit.
### 5. Klik "Start Scraping" :
   Proses scraping akan berjalan, progress bar akan bergerak, dan log akan muncul di panel kanan.
### 6. Lihat Hasil :
   Artikel yang berhasil di-scrape akan tampil di tabel dengan kolom: Judul, Tanggal, Isi, URL.
### 7. Export Data :
   Klik "Export Excel" atau "Export CSV" untuk menyimpan hasil ke file.
### 8. Clear:
   Klik tombol "Clear" untuk membersihkan tabel dan memulai scraping baru.

## Tips:
- Gunakan rentang tanggal yang sesuai dengan artikel terbaru di website (biasanya 1–2 minggu terakhir).
- Website yang direkomendasikan: subdomain Kompas (tekno, health, lifestyle, nasional) dan Detik (news.detik.com, finance.detik.com).

## Website yang didukung
- Kompas        : https://tekno.kompas.com              ✅ Berhasil
- Detik         : https://news.detik.com                ✅ Berhasil
- Antara News   : https://www.antaranews.com/berita     ✅ Berhasil
- CNN Indonesia :https://www.cnnindonesia.com/nasional  ⚠️ Tergantung JS load

## Preview Tampilan
1. Tampilan Awal
<img width="1300" height="740" alt="image" src="https://github.com/user-attachments/assets/1bc05fa2-a5c7-4610-adbe-8e6fb732aede" />

2. Proses Scraping Berjalan
<img width="1301" height="742" alt="image" src="https://github.com/user-attachments/assets/41443c00-7eec-4395-a69e-389589888ad8" />

3. Hasil Scraping di Tabel
<img width="1299" height="738" alt="image" src="https://github.com/user-attachments/assets/6ee04f3c-fcda-49f7-b70d-ea96bbdf3f84" />

4. Export Excel Berhasil
<img width="1304" height="741" alt="image" src="https://github.com/user-attachments/assets/cba4c52c-78cf-445a-ba96-5c739f5628a5" />

<img width="1919" height="1099" alt="image" src="https://github.com/user-attachments/assets/73eda49d-3da4-4e47-97d3-e9f2f2b5a8df" />


## Catatan
- Aplikasi menggunakan Selenium dalam mode headless (tanpa membuka browser secara visual).
- Proses scraping berjalan di background thread sehingga GUI tidak freeze.
- Log scraping disimpan otomatis ke file logs.txt.
- Filter tanggal bekerja berdasarkan tanggal terbit artikel yang diambil dari meta tag atau atribut datetime pada elemen HTML.

## Author
- Falisha Reyhana  		: 251524067
- Najla Gianneta Agisny 	: 251524080
- Syahid Azzam Alkaf		: 251524089
- Syaqila Dwina Putri		: 251524090
