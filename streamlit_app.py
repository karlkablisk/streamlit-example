import streamlit as st
import pixabay.core
import requests
import random 
import player
import chat
from my_pixabay import fetch_image, fetch_video
from player import generate_player

player = generate_player()

def main():
    # Sidebar
    st.sidebar.image(player["image"], caption="Player", use_column_width=True)

    player["name"] = st.sidebar.text_input("Player Name:", value=player["name"])
    st.sidebar.text(f"Class: {player['class']}")

    st.sidebar.subheader("Player Stats")
    for stat, value in player["stats"].items():
        st.sidebar.text(f"{stat}: {value}")

    tab_selected = st.sidebar.selectbox("Choose tab", ["Items", "Equipment"])
    if tab_selected == "Items":
        for item in player["items"]:
            st.sidebar.text(item)
    elif tab_selected == "Equipment":
        for slot, item in player["equipment"].items():
            st.sidebar.text(f"{slot.capitalize()}: {item or 'None'}")

    with st.sidebar.expander("Testing"):
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

    # Main Area
    character_col, chat_col, media_col = st.columns([1, 2, 1])

    if 'image_url' in st.session_state:
        character_col.image(st.session_state['image_url'], caption="Character Image", use_column_width=True)
        
    chat_input = chat_col.text_input("Enter your chat message:")
    chat_col.text_area("Chat Display", "Chat messages will appear here.", height=300)

    if 'image_url' in st.session_state:
        media_col.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)
    if 'video_url' in st.session_state:
        media_col.video(st.session_state['video_url'] + "#autoplay=1")

if __name__ == "__main__":
    main()
