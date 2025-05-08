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
