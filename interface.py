import streamlit as st
from my_pixabay import fetch_image, fetch_video
import player

def sidebar_area():
    st.sidebar.header("Player Info")

    # Editable Player Name
    new_player_name = st.sidebar.text_input("Player Name", player.get_player_name())
    player.set_player_name(new_player_name)

    player_image = player.get_player_image()
    st.sidebar.image(player_image, caption=player.get_player_name(), use_column_width=True)

    # Reroll image
    image_keyword = st.sidebar.text_input("Keyword for new image:", key="image_keyword")

    if st.sidebar.button("Reroll Player Image") or image_keyword != st.session_state.get("previous_image_keyword", ""):
        player.reroll_player_image(image_keyword)
        st.session_state["previous_image_keyword"] = image_keyword

    # Tabs for Stats, Items, Equipment, and Testing
    stats_tab, items_tab, equipment_tab, testing_tab = st.sidebar.tabs(["Stats", "Items", "Equipment", "Testing"])

    with stats_tab:
        # Player Details
        st.text("Class: " + player.get_player_class())

        # Player Stats
        st.text("Strength: " + str(player.get_stat("Strength")))
        st.text("Charisma: " + str(player.get_stat("Charisma")))
        st.text("Dexterity: " + str(player.get_stat("Dexterity")))
        st.text("Agility: " + str(player.get_stat("Agility")))
        st.text("Luck: " + str(player.get_stat("Luck")))

    with items_tab:
        for item in player.get_items():
            st.text(item)

    with equipment_tab:
        st.text("Head: " + player.get_equipment("Head"))
        st.text("Body: " + player.get_equipment("Body"))
        st.text("Arms: " + player.get_equipment("Arms"))
        st.text("Legs: " + player.get_equipment("Legs"))
        st.text("Accessory 1: " + player.get_equipment("Accessory 1"))
        st.text("Accessory 2: " + player.get_equipment("Accessory 2"))

    with testing_tab:
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

        # Audio search
        audio_type = st.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
        audio_query = st.text_input("Search for Audio:")
        if st.button("Search Audio"):
            st.write(f"Searching for audio '{audio_query}' of type '{audio_type}'... (feature not supported)")

def column1():
    chat_col = st.columns([2,1,1])[0]
    chat_input = chat_col.text_input("Enter your chat message:")
    chat_col.text_area("Chat Display", "Chat messages will appear here.", height=300)

def column2():
    image_col = st.columns([2,1,1])[1]
    if 'image_url' in st.session_state:
        image_col.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)

def column3():
    video_col = st.columns([2,1,1])[2]
    if 'video_url' in st.session_state:
        video_col.video(st.session_state['video_url'] + "#autoplay=1")
