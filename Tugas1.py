# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:56:16 2026

@author: dhafi
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

WARNA_FILTER = (0, 0, 255)

if not cap.isOpened():
    print("Kamera tidak bisa dibuka, cek koneksi/driver kamera")
else:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Gagal membaca frame dari kamera")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        color_filter = np.zeros_like(frame)
        for i in range(3): 
            color_filter[:, :, i] = (gray * (WARNA_FILTER[i] / 255)).astype(np.uint8)

        cv2.imshow('Original', frame)
        cv2.imshow('Color Filter', color_filter)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()