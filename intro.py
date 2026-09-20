# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:56:16 2026

@author: dhafi
"""

import cv2
import numpy as np

WARNA_FILTER = (0, 0, 255)


def terapkan_color_filter(image, warna):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    color_filter = np.zeros_like(image)
    
    for i in range(3):
        color_filter[:, :, i] = (gray * (warna[i] / 255.0)).astype(np.uint8)
        
    return color_filter

img_path = 'view.jpg'
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Gambar '{img_path}' tidak ditemukan!")
else:

    img_filtered = terapkan_color_filter(img, WARNA_FILTER)


    cv2.imshow('Gambar - Original', img)
    cv2.imshow('Gambar - Color Filter', img_filtered)
    
    print("Tekan tombol apa saja di keyboard untuk lanjut ke kamera...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Kamera tidak bisa dibuka, cek koneksi/driver kamera")
else:
    print("Membuka kamera... Tekan 'q' untuk keluar.")
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Gagal membaca frame dari kamera")
            break


        frame_filtered = terapkan_color_filter(frame, WARNA_FILTER)

        # Tampilkan Kamera
        cv2.imshow('Kamera - Original', frame)
        cv2.imshow('Kamera - Color Filter', frame_filtered)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

print("Selesai!")