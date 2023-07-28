#my_pixabay.py - all pixabay logic goes here

import streamlit as st
import random
import requests
import pixabay.core

# Constants
PIXABAY_API_KEY = '13689623-be5edb4373e4b7e250a22e3ce'  # Replace with your Pixabay API key
px = pixabay.core(PIXABAY_API_KEY)

BASE_IMAGE_URL = "https://pixabay.com/api/"
BASE_VIDEO_URL = "https://pixabay.com/api/videos/"

def fetch_image(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo',
        'pretty': 'true'
    }

    response = requests.get(BASE_IMAGE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['totalHits'] > 0:
            return random.choice(data['hits'])['webformatURL']
        else:
            return None
    else:
        return None

def fetch_video(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'pretty': 'true'
    }

    response = requests.get(BASE_VIDEO_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['totalHits'] > 0:
            return random.choice(data['hits'])['videos']['medium']['url']
        else:
            return None
    else:
        return None
