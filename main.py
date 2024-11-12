import os
import time
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

# Fungsi utama untuk memilih opsi
def main():
    while True:
        # Tampilkan header dan menu
        display_header()
        display_menu()

        # Ambil input dari pengguna
        choice = input(Fore.GREEN + "Pilih opsi: " + Style.RESET_ALL)

        if choice == "1":
            # Menjalankan bypass_403.py kemudian canon_403.py
            run_script("bypass_403v3.py")
            time.sleep(5)  # Tunggu sejenak sebelum menjalankan script berikutnya
            run_script("canon_403.py")
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
