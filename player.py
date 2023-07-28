#player.py - all player related details go here


import streamlit as st
from my_pixabay import fetch_image

# Player attributes
player_image = fetch_image("person")
player_name = "PLAYER"
player_class = "Warrior"  # Example class for now

player_stats = {
    "Strength": 10,
    "Charisma": 10,
    "Dexterity": 10,
    "Agility": 10,
    "Luck": 10
}

player_items = ["Item1", "Item2"]  # Example items for now

player_equipment = {
    "Head": "None",
    "Body": "None",
    "Arms": "None",
    "Legs": "None",
    "Accessory 1": "None",
    "Accessory 2": "None"
}

# Generate player method removed as we're directly using global variables

# Functions to retrieve player attributes
def get_player_image():
    return player_image

def reroll_player_image(keyword):
    global player_image
    new_image_url = fetch_image(keyword)
    if new_image_url:
        player_image = new_image_url

def get_player_name():
    return player_name

def set_player_name(name):
    global player_name
    player_name = name

def get_player_class():
    return player_class

def get_stat(stat_name):
    return player_stats.get(stat_name, "N/A")

def get_items():
    return player_items

def get_equipment(slot):
    return player_equipment.get(slot, "None")

def set_equipment(slot, item):
    global player_equipment
    if slot in player_equipment:
        player_equipment[slot] = item
