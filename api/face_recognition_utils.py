# face_recognition_utils.py
import os
import numpy as np
import time

def get_esp32_image(url=None):
    """Mock capturing image from ESP32 camera"""
    print(f"Mock: Capturing image from {url}")
    return np.zeros((480, 640, 3), dtype=np.uint8)  # Return a black image

def extract_face_encoding(image_path_or_array):
    """Mock extracting face encoding"""
    print(f"Mock: Extracting face encoding from {'image file' if isinstance(image_path_or_array, str) else 'image array'}")
    # Return a random encoding vector (128-dimensional)
    return np.random.rand(128), None

def recognize_face(image, profiles):
    """Mock face recognition"""
    print(f"Mock: Recognizing face against {len(profiles)} profiles")
    
    if not profiles:
        return None, "No profiles found"
    
    # Mock a match with the first profile
    matches = [(profiles[0].id, (0, 0, 0, 0))]
    
    return matches, None