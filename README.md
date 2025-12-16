---

Minelt - Professional Litecoin Mining Software**Minelt** adalah perangkat lunak penambangan Litecoin (LTC) berbasis Python yang dikembangkan untuk efisiensi dan transparansi. Dibangun dengan algoritma hashing **Scrypt** asli dan protokol **Stratum V1**, Minelt mampu melakukan komunikasi *low-latency* dengan mining pool standar industri seperti `litecoinpool.org`.

Software ini dilengkapi dengan fitur deteksi perangkat keras cerdas (*Hardware Awareness*) yang memonitor spesifikasi CPU dan RAM secara *real-time* untuk memastikan stabilitas selama proses hashing.

---


## Screenshots

![Minelt Screenshot](https://github.com/sirrauf/Minelt/blob/main/Screenshoot/SS2.png?raw=true)
![Minelt Screenshot](https://github.com/sirrauf/Minelt/blob/main/Screenshoot/SS1.png?raw=true) *Example screenshot of the Minelt mining interface*

##📋 Table of Contents (ToC)* [Minelt - Professional Litecoin Mining Software](https://www.google.com/search?q=%23minelt---professional-litecoin-mining-software)
* [📋 Table of Contents (ToC)](https://www.google.com/search?q=%23-table-of-contents-toc)
* [✨ Key Features](https://www.google.com/search?q=%23-key-features)
* [📂 Project Structure](https://www.google.com/search?q=%23-project-structure)
* [⚙️ Prerequisites](https://www.google.com/search?q=%23%EF%B8%8F-prerequisites)
* [🚀 Installation](https://www.google.com/search?q=%23-installation)
* [🔧 Configuration](https://www.google.com/search?q=%23-configuration)
* [▶️ Usage](https://www.google.com/search?q=%23%EF%B8%8F-usage)
* [📊 Technical Details](https://www.google.com/search?q=%23-technical-details)
* [⚠️ Troubleshooting](https://www.google.com/search?q=%23%EF%B8%8F-troubleshooting)
* [📜 License & Credits](https://www.google.com/search?q=%23-license--credits)



---

##✨ Key Features* **Native Scrypt Algorithm:** Menggunakan implementasi C-binding `scrypt` untuk hashing yang valid dan akurat (bukan simulasi SHA256).
* **Hardware Awareness:** Mendeteksi dan menampilkan spesifikasi detail:
* CPU Brand & Model (Intel/AMD).
* Core Counts (Physical & Logical).
* RAM Usage & Total Capacity.
* Operating System Details.


* **Stratum V1 Protocol:** Implementasi penuh protokol TCP socket untuk menjaga koneksi stabil dengan pool.
* **Real-time Statistics:**
* Kalkulasi Hashrate (kH/s) secara *live*.
* Monitoring Shares (Accepted, Rejected, Stale).
* Uptime counter.


* **Low Resource Overhead:** Kode dioptimalkan untuk berjalan dengan *footprint* memori yang minim.

---

##📂 Project StructureBerikut adalah struktur direktori dari proyek Minelt:

```text
Minelt-Project/
│
├── minelt.py            # Core mining engine (Main Application)
├── requirements.txt     # Daftar dependensi library Python
├── account_pool.txt     # Konfigurasi Pool dan User (Optional/Legacy)
├── ltc_addrs.txt        # Daftar alamat wallet (Optional/Legacy)
└── README.md            # Dokumentasi Proyek

```

---

##⚙️ PrerequisitesSebelum menjalankan Minelt, pastikan sistem Anda memenuhi persyaratan berikut:

1. **Python 3.8 atau lebih baru**: [Download Python](https://www.python.org/downloads/)
2. **Microsoft Visual C++ Build Tools (Windows Only)**: Diperlukan untuk mengkompilasi library `scrypt`. [Download Build Tools](https://www.google.com/search?q=https://visualstudio.microsoft.com/visual-cpp-build-tools/).
3. **Koneksi Internet Stabil**: Wajib untuk protokol Stratum.

---

##🚀 InstallationIkuti langkah-langkah ini untuk menginstal dan menjalankan Minelt:

1. **Ekstrak Project**
Ekstrak file `.zip` atau `.rar` Minelt ke folder tujuan Anda.
2. **Buka Terminal / Command Prompt**
Navigasikan ke folder proyek:
```bash
cd path/to/Minelt-Project

```


3. **Install Dependencies**
Jalankan perintah berikut untuk menginstal library yang dibutuhkan (`scrypt`, `psutil`, `requests`, dll):
```bash
pip install -r requirements.txt

```


*(Catatan: Proses ini mungkin memakan waktu beberapa menit saat mengkompilasi scrypt).*

---

##🔧 ConfigurationKonfigurasi *default* saat ini diatur untuk **litecoinpool.org**. Untuk mengubah pengaturan mining, Anda dapat mengedit variabel di dalam file `minelt.py` pada bagian **Configuration** atau menyesuaikan logika pembacaan file eksternal.

**Default Configuration:**

* **Pool Host:** `eu.litecoinpool.org`
* **Port:** `3333`
* **Algorithm:** `Scrypt`

---

##▶️ UsageUntuk memulai proses mining, jalankan perintah berikut di terminal:

```bash
python minelt.py

```

**Tampilan Output:**
Saat berjalan, Minelt akan menampilkan:

1. **Hardware Info:** Detail spesifikasi PC Anda.
2. **Connection Status:** Log koneksi ke Pool.
3. **Mining Dashboard:** Baris status yang diperbarui setiap 5 detik berisi Speed (kH/s) dan Share status.

Contoh tampilan:

```text
SPEED: 12.50 kH/s | Uptime: 00:05:20 | Shares: 2/0 | Blocks: 0

```

---

##📊 Technical Details###Hardware IntegrationMinelt menggunakan library `psutil` dan `py-cpuinfo` untuk mengakses level rendah sistem operasi guna membaca topologi CPU dan manajemen memori. Ini memastikan script tidak membebani sistem di luar batas kapasitas RAM yang tersedia.

###Network ProtocolMenggunakan `socket` murni Python untuk komunikasi TCP asynchronous. Script menangani pesan JSON-RPC stratum seperti `mining.subscribe`, `mining.authorize`, `mining.notify`, dan `mining.submit`.

---

##⚠️ Troubleshooting**Q: Error `ModuleNotFoundError: No module named 'scrypt'`?**
A: Library scrypt belum terinstall. Pastikan C++ Build Tools sudah terinstall, lalu jalankan `pip install scrypt`.

**Q: Hashrate muncul tapi tidak ada saldo di Litecoinpool?**
A: Mining dengan CPU memiliki hashrate yang sangat kecil dibandingkan mesin ASIC. Anda membutuhkan waktu yang sangat lama untuk mendapatkan "Accepted Share" yang valid di difficulty jaringan saat ini. Ini adalah limitasi hardware, bukan kesalahan script.

**Q: Script tertutup sendiri (Crash)?**
A: Cek koneksi internet Anda. Script dirancang untuk berhenti jika koneksi ke pool terputus secara permanen untuk keamanan.

---

##📜 License & Credits**Developed by:** Ananda Rauf Maududi
**Version:** 2.0.0 (Production Build)
**License:** Private / Proprietary

*Software ini ditujukan untuk tujuan produksi dan eksperimen teknologi Blockchain.*