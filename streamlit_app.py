import streamlit as st
import requests

# Constants
PIXABAY_SECRET = st.secrets["PIXABAY_API_SECRET"]
#PIXABAY_API_KEY = PIXABAY_SECRET 
PIXABAY_API_KEY = '13689623-be5edb4373e4b7e250a22e3ce'  # Replace with your Pixabay API key


# Pixabay API base URL
PIXABAY_API_URL = 'https://pixabay.com/api/'

# Fetch media from Pixabay
def fetch_media(query, media_type, audio_type=None):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo' if media_type == 'image' else None,
        'video_type': 'film' if media_type == 'video' else None,
        'type': audio_type if media_type == 'audio' else None,
        'per_page': 1  # We're only interested in the first result
    }
    
    response = requests.get(PIXABAY_API_URL, params=params)
    
    # Check if the request was successful
    if response.ok:
        try:
            return response.json()
        except ValueError:
            st.write("Error decoding the JSON from Pixabay API.")
            return {}
    else:
        st.write(f"Error fetching data from Pixabay API. Status code: {response.status_code}")
        return {}

# Main function
def main():
    st.title('Pixabay Media Search and Display')

    # Sidebar
    with st.sidebar:
        st.header("Controls")
        
        # Image search
        image_query = st.text_input("Search for an Image:")
        if st.button("Search Image"):
            image_data = fetch_media(image_query, 'image')
            if image_data['hits']:
                st.session_state['image_url'] = image_data['hits'][0]['webformatURL']

        # Video search
        video_query = st.text_input("Search for a Video:")
        if st.button("Search Video"):
            video_data = fetch_media(video_query, 'video')
            if video_data['hits']:
                st.session_state['video_url'] = video_data['hits'][0]['videos']['medium']['url']

        # Audio search with type
        audio_type = st.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
        audio_query = st.text_input("Search for Audio:")
        if st.button("Search Audio"):
            audio_data = fetch_media(audio_query, 'audio', audio_type)
            if audio_data['hits']:
                st.session_state['audio_url'] = audio_data['hits'][0]['webformatURL']

    # Main Area
    # Display Image
    if 'image_url' in st.session_state:
        st.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)

    # Display Video
    if 'video_url' in st.session_state:
        st.video(st.session_state['video_url'])

    # Display Audio
    if 'audio_url' in st.session_state:
        st.audio(st.session_state['audio_url'])

if __name__ == "__main__":
    main()
