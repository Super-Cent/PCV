# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:50:33 2026

@author: dhafi
"""

import cv2
import numpy as np

def transformasi_negatif_manual(img_gray):
    return 255 - img_gray

def ekualisasi_histogram_manual(img_gray):
    height, width = img_gray.shape
    total_pixels = height * width

    histogram = np.zeros(256, dtype=int)
    for row in range(height):
        for col in range(width):
            pixel_val = img_gray[row, col]
            histogram[pixel_val] += 1


    pdf = histogram / total_pixels

    cdf = np.zeros(256, dtype=float)
    cdf_cumulative = 0.0
    for i in range(256):
        cdf_cumulative += pdf[i]
        cdf[i] = cdf_cumulative

    transform_map = np.round(cdf * 255).astype(np.uint8)

    img_equalized = np.zeros_like(img_gray)
    for row in range(height):
        for col in range(width):
            img_equalized[row, col] = transform_map[img_gray[row, col]]

    return img_equalized


img_path = 'lucy.jpg'
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Gambar '{img_path}' tidak ditemukan!")
else:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Pemanggilan Fungsi Manual
    img_negatif = transformasi_negatif_manual(gray_img)
    img_equalized = ekualisasi_histogram_manual(gray_img)

    # Tampilkan Hasil
    cv2.imshow('1. Grayscale Original', gray_img)
    cv2.imshow('2. Transformasi Intensitas (Negatif)', img_negatif)
    cv2.imshow('3. Ekualisasi Histogram Manual', img_equalized)

    print("Tekan tombol apa saja di keyboard untuk lanjut ke kamera...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Kamera tidak dapat diakses.")
else:
    print("Membuka kamera... Tekan 'q' untuk keluar.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_negatif = transformasi_negatif_manual(gray_frame)
        frame_equalized = ekualisasi_histogram_manual(gray_frame)

        cv2.imshow('Kamera - Grayscale Original', gray_frame)
        cv2.imshow('Kamera - Transformasi Negatif', frame_negatif)
        cv2.imshow('Kamera - Ekualisasi Histogram Manual', frame_equalized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

print("Selesai!")