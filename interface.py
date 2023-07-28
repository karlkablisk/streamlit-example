#Interface.py all visaul elements go here layout, frame etc.

import streamlit as st
from my_pixabay import fetch_image
import player

def sidebar_area():
    st.sidebar.header("Player Info")
    
    player_image = player.get_player_image()
    st.sidebar.image(player_image, caption=player.get_player_name(), use_column_width=True)
    
    # Player Details
    st.sidebar.text("Class: " + player.get_player_class())
    
    # Player Stats
    st.sidebar.text("Strength: " + str(player.get_stat("Strength")))
    st.sidebar.text("Charisma: " + str(player.get_stat("Charisma")))
    st.sidebar.text("Dexterity: " + str(player.get_stat("Dexterity")))
    st.sidebar.text("Agility: " + str(player.get_stat("Agility")))
    st.sidebar.text("Luck: " + str(player.get_stat("Luck")))
    
    # Tabs for Items and Equipment
    tab = st.sidebar.selectbox("Choose a tab", ["Items", "Equipment"])
    
    if tab == "Items":
        # Display the items
        for item in player.get_items():
            st.sidebar.text(item)
    else:
        # Equipment section
        st.sidebar.text("Head: " + player.get_equipment("Head"))
        st.sidebar.text("Body: " + player.get_equipment("Body"))
        st.sidebar.text("Arms: " + player.get_equipment("Arms"))
        st.sidebar.text("Legs: " + player.get_equipment("Legs"))
        st.sidebar.text("Accessory 1: " + player.get_equipment("Accessory 1"))
        st.sidebar.text("Accessory 2: " + player.get_equipment("Accessory 2"))

    # Testing Dropdown
    with st.sidebar.expander("Testing"):
        # Image search
        image_query = st.sidebar.text_input("Search for an Image:")
        if st.sidebar.button("Search Image"):
            image_url = fetch_image(image_query)
            if image_url:
                st.session_state['image_url'] = image_url

def column1():
    chat_col = st.columns([2,1,1])[0]
    chat_input = chat_col.text_input("Enter your chat message:")
    chat_col.text_area("Chat Display", "Chat messages will appear here.", height=300)

def column2():
    image_col = st.columns([2,1,1])[1]
    if 'image_url' in st.session_state:
        image_col.image(st.session_state['image_url'], caption="Searched Image", use_column_width=True)
    # Add other elements if required

def column3():
    video_col = st.columns([2,1,1])[2]
    if 'video_url' in st.session_state:
        video_col.video(st.session_state['video_url'] + "#autoplay=1")



