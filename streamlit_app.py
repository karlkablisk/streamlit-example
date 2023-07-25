import streamlit as st
import pixabay.core
import requests

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
            return data['hits'][0]['webformatURL']
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
            return data['hits'][0]['videos']['medium']['url']
        else:
            st.write("API call did not return any hits.")
            return None
    else:
        st.write(f"API call failed with status code: {response.status_code}")
        return None




def main():
    st.title('Pixabay Media Search and Display')

    with st.sidebar:
        st.header("Controls")

        # Image search
        image_query = st.text_input("Search for an Image:")
        if st.button("Search Image"):
            image_url = fetch_image(image_query)
            if image_url:
                st.session_state['image_url'] = image_url

        # Video search
        video_query = st.text_input("Search for a Video:")
        if st.button("Search Video"):
            video_url = fetch_video(video_query)
            if video_url:
                st.session_state['video_url'] = video_url

        # Audio search with type (Note: Pixabay API does not provide direct support for audio)
        # This is kept as is since you had this in your previous app version.
        audio_type = st.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
        audio_query = st.text_input("Search for Audio:")
        if st.button("Search Audio"):
            # Sample code, as the library and Pixabay API do not provide direct audio support.
            st.write(f"Searching for audio '{audio_query}' of type '{audio_type}'... (feature not supported)")

    # Main Area
    if 'image_url' in st.session_state:
        st.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)

    if 'video_url' in st.session_state:
        st.video(st.session_state['video_url'])

if __name__ == "__main__":
    main()
