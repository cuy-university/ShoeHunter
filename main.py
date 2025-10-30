import requests
from bs4 import BeautifulSoup
import csv
import os

#============================================
# 1. url yang akan di scrape
#============================================

url = "https://shopee.co.id/search?keyword=sepatu%20pria"

# Header, supaya shopee tidak blokir kita

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

print("menjalankan shoehunter...")
response = requests.get(url, headers=headers)

# Cek apakah berhasil terhubung ke Shopee

if response.status_code != 200:
    print(f"❌ Gagal mengakses Shopee! Status code: {response.status_code}")
    exit()

# ==========================
# 2. Parsing HTML dengan BeautifulSoup
# ==========================
soup = BeautifulSoup(response.text, "html.parser")

# Elemen produk di halaman Shopee biasanya mengandung <div> dengan role tertentu
# Tapi Shopee memakai dynamic loading (JS), jadi sebagian data tidak muncul.
# Jadi kita akan ambil elemen 'meta' atau 'script' sebagai contoh awal.

items = soup.find_all("div", class_="col-xs-2-4")  # ini bisa berubah
if not items:
    print("⚠️ Tidak ada produk yang terdeteksi (Shopee pakai dynamic page).")
    print("Kita akan buat contoh dummy data agar CSV tetap terbentuk.")
    items = [{"name": "Sepatu Nike Air", "price": "Rp 450.000", "link": url}]

# ==========================
# 3. Simpan ke file CSV
# ==========================
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "hasil_scraping.csv")

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Nama Produk", "Harga", "Link"])

    # Kalau hasil asli dari scraping
    if isinstance(items[0], dict):
        for i in items:
            writer.writerow([i["name"], i["price"], i["link"]])
    else:
        # Dummy row kalau elemen kosong
        writer.writerow(["Sepatu Contoh", "Rp 200.000", url])

print(f"✅ Data berhasil disimpan di: {output_path}")