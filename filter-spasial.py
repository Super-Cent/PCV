# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:32:32 2026

@author: dhafi
"""

import cv2
import numpy as np

# ==============================================================================
# 1. DEFINISI KERNEL FILTER SPASIAL (Diperkuat)
# ==============================================================================

# A. Smoothing Filter (Mean Filter 5x5 - Lebih terasa bedanya)
kernel_smoothing = np.ones((5, 5), np.float32) / 25.0

# B. Sharpening Filter (Kernel Tajam)
kernel_sharpening = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
], dtype=np.float32)


def terapkan_filter_spasial(image):
    """Menerapkan smoothing dan sharpening dengan penanganan overflow"""
    # 1. Smoothing (Mean Filter)
    img_smooth = cv2.filter2D(image, -1, kernel_smoothing)

    # 2. Sharpening dengan penanganan Float -> Clip -> Uint8 (Mencegah Gambar Pecah)
    # Konversi ke float32 dulu agar angka negatif/melebihi 255 tidak rusak
    img_float = image.astype(np.float32)
    sharp_float = cv2.filter2D(img_float, -1, kernel_sharpening)
    
    # Batasi nilai di rentang 0-255 lalu kembalikan ke uint8
    img_sharp = np.clip(sharp_float, 0, 255).astype(np.uint8)

    return img_smooth, img_sharp


# ------------------------------------------------------------------------------
# PROSES UTAMA (GAMBAR)
# ------------------------------------------------------------------------------
img_path = 'lucy.jpg'
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Gambar '{img_path}' tidak ditemukan!")
else:
    img_smooth, img_sharp = terapkan_filter_spasial(img)

    cv2.imshow('1. Gambar Original', img)
    cv2.imshow('2. Smoothing (Kabur Halus)', img_smooth)
    cv2.imshow('3. Sharpening (Tajam Bersih)', img_sharp)

    print("Tekan tombol apa saja di keyboard untuk lanjut ke kamera...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ------------------------------------------------------------------------------
# PROSES UTAMA (WEBCAM)
# ------------------------------------------------------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Kamera tidak dapat diakses.")
else:
    print("Membuka kamera... Tekan 'q' untuk keluar.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_smooth, frame_sharp = terapkan_filter_spasial(frame)

        cv2.imshow('Kamera - Original', frame)
        cv2.imshow('Kamera - Smoothing (Mean)', frame_smooth)
        cv2.imshow('Kamera - Sharpening', frame_sharp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

print("Selesai!")