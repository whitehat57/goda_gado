import os
import time
import json
from colorama import Fore, Style, init

# Inisialisasi colorama untuk mendukung warna di terminal
init(autoreset=True)

# Header dengan warna merah dan putih
def display_header():
    print(Fore.RED + "      ::::::::   ::::::::  :::::::::      :::            ::::::::      :::     :::::::::   ::::::::")
    print(Fore.RED + "    :+:    :+: :+:    :+: :+:    :+:   :+: :+:         :+:    :+:   :+: :+:   :+:    :+: :+:    :+:")
    print(Fore.RED + "   +:+        +:+    +:+ +:+    +:+  +:+   +:+        +:+         +:+   +:+  +:+    +:+ +:+    +:+")
    print(Fore.WHITE + "  :#:        +#+    +:+ +#+    +:+ +#++:++#++:       :#:        +#++:++#++: +#+    +:+ +#+    +:+ ")
    print(Fore.WHITE + " +#+   +#+# +#+    +#+ +#+    +#+ +#+     +#+       +#+   +#+# +#+     +#+ +#+    +#+ +#+    +#+  ")
    print(Fore.WHITE + " #+#    #+# #+#    #+# #+#    #+# #+#     #+#       #+#    #+# #+#     #+# #+#    #+# #+#    #+#   ")
    print(Fore.WHITE + " ########   ########  #########  ###     ###        ########  ###     ### #########   ########    " + Style.RESET_ALL + Fore.WHITE + " v1.0\n")

    print(Fore.RED + "bypasser 403 & API attack")
    print(Fore.RED + "coded by : Danz\n" + Style.RESET_ALL)

# Menampilkan menu utama
def display_menu():
    print(Fore.WHITE + "Menu :")
    print(Fore.CYAN + "\t[1] bypass 403")
    print(Fore.CYAN + "\t[2] API canon attack tanpa bypass\n")

# Fungsi untuk menjalankan script dengan nama tertentu
def run_script(script_name):
    try:
        print(Fore.YELLOW + f"Menjalankan {script_name}...")
        os.system(f"python3 {script_name}")
    except Exception as e:
        print(Fore.RED + f"Error saat menjalankan {script_name}: {e}")

def run_bypass_sequence():
    # Hapus file bypass_config.json jika sudah ada
    if os.path.exists("bypass_config.json"):
        os.remove("bypass_config.json")
    
    # Jalankan bypass_403v3.py
    print(Fore.YELLOW + "Memulai proses bypass...")
    run_script("bypass_403v3.py")
    
    # Tunggu dan cek file
    max_retries = 3
    retries = 0
    while retries < max_retries:
        if os.path.exists("bypass_config.json"):
            try:
                # Verifikasi file dapat dibaca
                with open("bypass_config.json", "r") as f:
                    json.load(f)
                print(Fore.GREEN + "Bypass berhasil, menjalankan canon attack...")
                time.sleep(2)
                run_script("canon_403.py")
                break
            except json.JSONDecodeError:
                print(Fore.RED + "File konfigurasi rusak, mencoba lagi...")
        else:
            print(Fore.YELLOW + f"Menunggu hasil bypass... ({retries + 1}/{max_retries})")
            time.sleep(2)
            retries += 1
    
    if retries >= max_retries:
        print(Fore.RED + "Bypass gagal, tidak dapat melanjutkan ke canon attack")

# Fungsi utama untuk memilih opsi
def main():
    while True:
        # Tampilkan header dan menu
        display_header()
        display_menu()

        # Ambil input dari pengguna
        choice = input(Fore.GREEN + "Pilih opsi: " + Style.RESET_ALL)

        if choice == "1":
            run_bypass_sequence()
        elif choice == "2":
            # Menjalankan API.py
            run_script("API.py")
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

        # Tanya apakah pengguna ingin kembali ke menu
        kembali = input(Fore.YELLOW + "\nKembali ke menu? (y/n): " + Style.RESET_ALL)
        if kembali.lower() != 'y':
            print(Fore.YELLOW + "Keluar dari program.")
            break

# Jalankan program utama
if __name__ == "__main__":
    main()
