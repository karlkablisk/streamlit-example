import streamlit as st
import pixabay.core
import requests
import random 
import player
import chat

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
            # Choose a random image from the results
            return random.choice(data['hits'])['webformatURL']
        else:
            st.write("API call did not return any hits.")
            return None
    else:
        st.write(f"API call failed with status code: {response.status_code}")
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
            # Choose a random video from the results
            return random.choice(data['hits'])['videos']['medium']['url']
        else:
            st.write("API call did not return any hits.")
            return None
    else:
        st.write(f"API call failed with status code: {response.status_code}")
        return None

def submenu_area():
    st.sidebar.header("Controls")
    # Image search
    image_query = st.sidebar.text_input("Search for an Image:")
    if st.sidebar.button("Search Image"):
        image_url = fetch_image(image_query)
        if image_url:
            st.session_state['image_url'] = image_url

    # Video search
    video_query = st.sidebar.text_input("Search for a Video:")
    if st.sidebar.button("Search Video"):
        video_url = fetch_video(video_query)
        if video_url:
            st.session_state['video_url'] = video_url

    audio_type = st.sidebar.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
    audio_query = st.sidebar.text_input("Search for Audio:")
    if st.sidebar.button("Search Audio"):
        st.sidebar.write(f"Searching for audio '{audio_query}' of type '{audio_type}'... (feature not supported)")

def main_area():
    chat_col, media_col = st.columns([1, 1])

    # Chat input and display placeholder
    chat_input = chat_col.text_input("Enter your chat message:")
    chat_col.text_area("Chat Display", "Chat messages will appear here.", height=300)

    # Media Display
    if 'image_url' in st.session_state:
        media_col.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)

    if 'video_url' in st.session_state:
        # Streamlit does not currently support video controls or autoplay customization. Using autoplay in the URL.
        media_col.video(st.session_state['video_url'] + "#autoplay=1")

def main():
    st.title('Pixabay Media Search and Display')
    submenu_area()
    main_area()

if __name__ == "__main__":
    main()
