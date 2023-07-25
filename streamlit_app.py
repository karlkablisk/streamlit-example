import streamlit as st
import pixabay.core

# Constants
PIXABAY_API_KEY = '13689623-be5edb4373e4b7e250a22e3ce'  # Replace with your Pixabay API key
px = pixabay.core(PIXABAY_API_KEY)

def fetch_image(query):
    result = px.query(query)
    if len(result) > 0:
        # Print all attributes of the result object for inspection
        st.write(dir(result[0]))
        return result[0].webformatURL  # This line may still cause an error, but we'll see the attributes first
    return None


def fetch_video(query):
    result = px.queryVideo(query)
    if len(result) > 0:
        return result[0].videos.medium.url  # Accessing video URL using attributes
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
