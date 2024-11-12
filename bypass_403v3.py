import requests
import time
import json
import random
import re

# Prompt pengguna untuk URL target
url = input("Masukkan URL target (contoh: https://example.com): ")

# Daftar User-Agent dan Referer yang lebih lengkap
headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1"},
    {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"},
    {"User-Agent": "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"},
    {"User-Agent": "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"},
    {"User-Agent": "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)"},
]

referer_list = [
    "https://google.com",
    "https://facebook.com",
    "https://twitter.com"
]

cookies_list = [
    {},  # Tanpa cookie
    {"session_id": "example-session-cookie"}
]

# Fungsi untuk mendeteksi jenis web server
def detect_web_server():
    try:
        response = requests.head(url, timeout=5)
        server_header = response.headers.get("Server", "Tidak Terdeteksi")
        print(f"Jenis Web Server yang terdeteksi: {server_header}")
        return server_header
    except Exception as e:
        print(f"Error saat mendeteksi server: {e}")
        return "Tidak Terdeteksi"

# Fungsi untuk mencoba bypass 403 dan menyimpan konfigurasi yang berhasil
def attempt_bypass():
    server_type = detect_web_server()  # Pindai jenis web server
    for headers in headers_list:
        for referer in referer_list:
            for cookies in cookies_list:
                headers["Referer"] = referer
                try:
                    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
                    if response.status_code == 200:
                        print("Bypass berhasil dengan konfigurasi berikut:")
                        print("Headers:", headers)
                        print("Referer:", referer)
                        print("Cookies:", cookies)
                        
                        # Simpan konfigurasi berhasil ke file JSON, termasuk jenis server
                        with open("bypass_config.json", "w") as file:
                            json.dump({
                                "url": url,
                                "headers": headers,
                                "cookies": cookies,
                                "server_type": server_type
                            }, file)
                        
                        return True  # Berhenti jika berhasil
                    elif response.status_code == 403:
                        print("403 Forbidden - Coba konfigurasi berikutnya")
                    
                    # Tambahkan jeda acak antara 1-3 detik di setiap percobaan
                    time.sleep(random.uniform(1, 3))
                except requests.exceptions.RequestException as e:
                    print(f"Error pada permintaan: {e}")
    return False

# Jalankan percobaan bypass
if attempt_bypass():
    print("Konfigurasi berhasil disimpan di 'bypass_config.json'")
else:
    print("Bypass gagal setelah beberapa percobaan.")
