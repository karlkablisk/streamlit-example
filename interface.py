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
    image_keyword = st.sidebar.text_input("Keyword for new image:")
    if st.sidebar.button("Reroll Player Image"):
        player.reroll_player_image(image_keyword)
    
    # Player Details
    st.sidebar.text("Class: " + player.get_player_class())
    
    # Player Stats
    st.sidebar.text("Strength: " + str(player.get_stat("Strength")))
    st.sidebar.text("Charisma: " + str(player.get_stat("Charisma")))
    st.sidebar.text("Dexterity: " + str(player.get_stat("Dexterity")))
    st.sidebar.text("Agility: " + str(player.get_stat("Agility")))
    st.sidebar.text("Luck: " + str(player.get_stat("Luck")))
    
    # Tabs for Items, Equipment, and Testing
    tab = st.sidebar.radio("Choose a tab", ["Items", "Equipment", "Testing"])
    
    if tab == "Items":
        for item in player.get_items():
            st.sidebar.text(item)
    elif tab == "Equipment":
        st.sidebar.text("Head: " + player.get_equipment("Head"))
        st.sidebar.text("Body: " + player.get_equipment("Body"))
        st.sidebar.text("Arms: " + player.get_equipment("Arms"))
        st.sidebar.text("Legs: " + player.get_equipment("Legs"))
        st.sidebar.text("Accessory 1: " + player.get_equipment("Accessory 1"))
        st.sidebar.text("Accessory 2: " + player.get_equipment("Accessory 2"))
    else:
        # Testing Tab
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
        # Audio search
        audio_type = st.sidebar.selectbox("Choose audio type", ["music", "voice", "sound_effect"])
        audio_query = st.sidebar.text_input("Search for Audio:")
        if st.sidebar.button("Search Audio"):
            st.sidebar.write(f"Searching for audio '{audio_query}' of type '{audio_type}'... (feature not supported)")

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

def main():
    sidebar_area()
    column1()
    column2()
    column3()

if __name__ == "__main__":
    main()
