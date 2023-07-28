#Interface.py all visaul elements go here layout, frame etc.
import streamlit as st
from my_pixabay import fetch_image, fetch_video
import player

def sidebar_area():
    st.sidebar.header("Player Details")
    
    # Player name input and update
    player_name = st.sidebar.text_input("Player Name", value=player.get_player_name())
    player.update_player_name(player_name)
    
    # Player image reroll
    keyword = st.sidebar.text_input("Keyword for new image")
    if st.sidebar.button("Reroll Image"):
        player.reroll_player_image(keyword)
    
    # Display player image
    st.sidebar.image(player.get_player_image(), use_column_width=True)

    st.sidebar.header("Test Controls")
    
    # Image search and display
    image_query = st.sidebar.text_input("Search for an Image:")
    if st.sidebar.button("Search Image"):
        image_url = fetch_image(image_query)
        if image_url:
            st.session_state['image_url'] = image_url

    # Video search and display
    video_query = st.sidebar.text_input("Search for a Video:")
    if st.sidebar.button("Search Video"):
        video_url = fetch_video(video_query)
        if video_url:
            st.session_state['video_url'] = video_url

    # Placeholder for audio search
    audio_type = st.sidebar.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
    audio_query = st.sidebar.text_input("Search for Audio:")
    if st.sidebar.button("Search Audio"):
        st.sidebar.write(f"Searching for audio '{audio_query}' of type '{audio_type}'... (feature not supported)")

def main_area():
    # Display chat and media
    chat_col, media_col = st.columns([1, 1])

    # Chat input and display placeholder
    chat_input = chat_col.text_input("Enter your chat message:")
    chat_col.text_area("Chat Display", "Chat messages will appear here.", height=300)

    # Media Display
    if 'image_url' in st.session_state:
        media_col.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)

    if 'video_url' in st.session_state:
        media_col.video(st.session_state['video_url'] + "#autoplay=1")

def main():
    sidebar_area()
    main_area()

if __name__ == "__main__":
    main()
