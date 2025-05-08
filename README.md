# Struktur Folder Pothole alert

    /pothole_alert_project
    │ 
    ├── pothole_alert.py             # Kode Python utama
    ├── requirements.txt             # Daftar pustaka Python
    ├── /output                      # Folder untuk hasil deteksi otomatis

Berikut adalah kode lengkap Python untuk aplikasi PotholeAlert yang mendeteksi lubang jalan dari citra drone menggunakan antarmuka GUI berbasis Tkinter. Kode ini mencakup:

* Pemilihan gambar

* Deteksi lubang jalan

* Tampilkan hasil deteksi di GUI

* Simpan hasil ke file

* Struktur yang rapi dan mudah dikembangkan

# Isi Folder Pothole alert
  # pothole_alert.py – Kode Lengkap

      import cv2
      import numpy as np
      from tkinter import Tk, filedialog, Label, Button, messagebox
      from PIL import Image, ImageTk
      import os

      # Fungsi deteksi lubang dan genangan air
      def detect_potholes(image_path):
      img = cv2.imread(image_path)
      if img is None:
        raise ValueError("Gambar tidak dapat dibaca.")

      # Skala ulang jika terlalu besar
      scale_percent = 70
      width = int(img.shape[1] * scale_percent / 100)
      height = int(img.shape[0] * scale_percent / 100)
      img = cv2.resize(img, (width, height))

      # Konversi ke grayscale dan HSV
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      # Threshold area gelap (lubang kering)
      blur = cv2.GaussianBlur(gray, (5, 5), 0)
      dark_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 4)

      # Deteksi warna genangan air (biru/abu muda)
      lower_water = np.array([90, 10, 50])
      upper_water = np.array([140, 255, 255])
      water_mask = cv2.inRange(hsv, lower_water, upper_water)

      # Gabungkan mask air dan gelap
      combined_mask = cv2.bitwise_or(dark_thresh, water_mask)

      # Hilangkan noise kecil
      kernel = np.ones((3, 3), np.uint8)
      clean_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel, iterations=2)

      # Temukan kontur
      contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      output = img.copy()
      pothole_count = 0

      for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Saring lubang kecil
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(output, "Lubang", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            pothole_count += 1

      return output, pothole_count

      # Fungsi untuk memilih gambar dan proses deteksi
      def open_image():
         path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
      if path:
        try:
            result, count = detect_potholes(path)
            save_path = os.path.join("output", os.path.basename(path))
            os.makedirs("output", exist_ok=True)
            cv2.imwrite(save_path, result)
            show_image(result)
            messagebox.showinfo("Sukses", f"Deteksi selesai!\nLubang terdeteksi: {count}\nHasil disimpan di: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

      # Tampilkan hasil gambar di GUI
      def show_image(img_cv):
       img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
       img_pil = Image.fromarray(img_rgb)
       img_pil = img_pil.resize((600, 400))
       img_tk = ImageTk.PhotoImage(img_pil)
       panel.configure(image=img_tk)
       panel.image = img_tk

      # GUI
      root = Tk()
      root.title("PotholeAlert - Deteksi Lubang Jalan Termasuk Genangan Air")
      root.geometry("800x600")
      root.configure(bg="#f0f0f0")

      Label(root, text="PotholeAlert", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=10)
      Label(root, text="Deteksi Lubang Jalan dari Citra Drone (Kering & Tergenang Air)", font=("Helvetica", 12), bg="#f0f0f0").pack()

      Button(root, text="Pilih Gambar Drone", command=open_image, font=("Helvetica", 12), bg="#008080", fg="white").pack(pady=15)

      panel = Label(root, bg="#f0f0f0")
      panel.pack(padx=10, pady=10)

      root.mainloop()
  # requirements.txt
    opencv-python
    numpy
    Pillow
  # Folder: output
# Link gambar untuk testing: https://raw.githubusercontent.com/mohamadfarisfadil/Pothole-alert/refs/heads/main/4248289897.jpg

# PotholeAlert: Aplikasi Deteksi Lubang Jalan Berbasis Citra Drone

Cara Running Python di Terminal/CMD Windows:
1. Langkah 1: Download Installer Python
    Klik link ini untuk langsung download versi stabil (64-bit):

    [🔗 Download Python 3.13.3 (Windows installer 64-bit)](https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe)

     Kalau laptop kamu 32-bit (jarang sekarang), beri tahu aku ya, biar kukasih link 32-bit.
2.  Langkah 2: Jalankan Installer
   
     a. Jalankan file .exe yang kamu unduh tadi.
    
     b. Penting: Centang opsi:
    
        ✅ Add Python 3.12 to PATH

     c. Klik "Install Now".
    
     d. Tunggu proses hingga selesai.
    
     e. Klik "Close" jika muncul "Setup was successful".
4. Langkah 3: Uji Instalasi
   Setelah itu, buka kembali Command Prompt dan ketik:
   
       python --version
   
       pip --version

5. Jika muncul versi seperti:
   
       Python 3.13.3
  
       pip 23.x.x

6. Langkah 4: Install Modul Python
   
    Lanjutkan dengan install modul yang dibutuhkan:
   
       pip install opencv-python numpy Pillow

# Kalau Tetap Gagal Bisa Ikuti Tutorial Di Bawah Ini!:

# 💡 Sementara, ini solusi umum tergantung masalahmu:
✅ Jika gagal download:

Coba unduh ulang pakai link ini (resmi dari Python.org):

    https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe

✅ Jika gagal install / muncul error saat install:

   Jalankan file .exe dengan klik kanan → Run as administrator.

   Pastikan centang "Add Python to PATH" saat proses awal.

   Kalau muncul error tertentu, beri tahu aku isi error-nya ya.

✅ Kalau sudah install tapi python masih tidak dikenali:

   Artinya PATH belum dikenali. Solusi:

   Restart laptop setelah instalasi Python.

  Buka cmd, lalu ketik:

    py --version

  Kalau ini muncul versi Python, bisa lanjut install paket dengan:

    py -m pip install opencv-python numpy Pillow
    
➡️ Apakah kamu sudah berhasil menginstal Python dan saat buka cmd, perintah python --version sekarang sudah berhasil dan menampilkan versi Python?

  Contoh output yang benar seperti ini:

    Python 3.12.3
    
Kalau sudah muncul, kita lanjut ke:
✅ LANJUT: Install Library Python untuk Proyek pothole_alert.py
  Ketik di cmd atau terminal:

    pip install opencv-python numpy Pillow

  Atau jika pip belum dikenali:

    python -m pip install opencv-python numpy Pillow
      
 Tunggu proses sampai selesai.

✅ Lalu: Jalankan Proyeknya
 Kalau file Python kamu misalnya bernama pothole_alert.py, jalankan dengan:

    python pothole_alert.py
    
Pastikan file-nya berada di folder yang sama dengan terminal kamu, atau navigasi ke folder tersebut dulu:

    cd C:\Users\nama_kamu\Documents\nama_folder

# ✅ LANGKAH LENGKAP: UBAH .py MENJADI .exe DI WINDOWS

1. Pastikan Python Sudah Terinstall

   Cek:
   
       python --version
       pip --version

Kalau sudah muncul versinya, lanjut.

2. Install PyInstaller
Ketik di CMD:

       pip install pyinstaller

Tunggu sampai selesai.

3. Ubah File .py Menjadi .exe
   
Masuk ke folder tempat file kamu:

       cd D:\Downloads\tugas_py
   
Kemudian ketik:

    pyinstaller --onefile tugas_py.py

Penjelasan:

--onefile: menghasilkan satu file .exe saja.

tugas_py.py: nama file Python kamu.

4. Temukan File .exe-nya

Setelah proses selesai:

File .exe kamu akan ada di folder:

    D:\Downloads\tugas_py\dist\tugas_py.exe

5. Jalankan .exe

Klik 2x pada tugas_py.exe di folder dist, atau jalankan via CMD:

    cd dist
    tugas_py.exe

# ✅ SOLUSI: Gunakan Python untuk Panggil pip
Coba jalankan ini dulu di CMD:

python -m pip install pyinstaller

Kalau python tidak dikenali, coba:

    py -m pip install pyinstaller

Ini memanggil pip secara langsung dari Python tanpa bergantung pada PATH.

🔧 Kalau Masih Gagal, Coba Cek Versi Python

Jalankan:

    python --version

Atau:

    py --version

Kalau semua itu tidak berhasil, berarti Python kamu memang belum terinstall dengan benar.

🛠️ Kalau Mau Pasang Ulang Python

Uninstall Python lama dari Settings → Apps.

Download ulang dari sini:

    https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe

Centang saat instalasi:

    ✅ Add Python to PATH
    
   Klik "Install Now".

Setelah itu, kamu bisa jalankan:

    python -m pip install pyinstaller

# ✅ Kalau Kamu Sudah Bisa Jalankan Python
Ketik ini di CMD:

    python -m pip install pyinstaller

Atau kalau pakai py:

    py -m pip install pyinstaller

Tunggu proses install selesai.

✅ Setelah Itu: Ubah .py Jadi .exe

Misalnya kamu punya file tugas_py.py di folder:

    D:\Downloads\tugas_py

Lakukan langkah ini:

Buka Command Prompt (CMD)

Masuk ke folder:

    cd D:\Downloads\tugas_py

Jalankan perintah:

    pyinstaller --onefile tugas_py.py

Kalau berhasil, nanti muncul folder baru bernama dist. Di dalamnya ada file ini:

    tugas_py.exe

Kamu bisa klik 2x atau jalankan dari CMD:

    cd dist
    tugas_py.exe

Kalau kamu ingin exe-nya tidak muncul jendela CMD (khusus untuk aplikasi GUI), bisa pakai:

    pyinstaller --onefile --noconsole tugas_py.py
