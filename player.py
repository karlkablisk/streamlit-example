#player.py - all player related details go here

import streamlit as st
from my_pixabay import fetch_image

PIXABAY_API_KEY = st.secrets["PIXABAY_API_SECRET"]

def generate_player():
    player = {}
    player_image = fetch_image('person', PIXABAY_API_KEY)
    player["image"] = player_image
    player["name"] = "PLAYER"
    player["class"] = "CLASS_NAME" # Placeholder
    player["stats"] = {
        "Strength": 0,
        "Charisma": 0,
        "Dexterity": 0,
        "Agility": 0,
        "Luck": 0
    }
    player["items"] = []
    player["equipment"] = {
        "head": None,
        "body": None,
        "arms": None,
        "legs": None,
        "accessory1": None,
        "accessory2": None
    }
    return player
