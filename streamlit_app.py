import streamlit as st
import pixabay.core
import requests
import random 
import interface
import player
import chat
from my_pixabay import fetch_image, fetch_video
from player import generate_player
from interface import sidebar_area, column1, column2, column3

def main():
    st.title('Pixabay Media Search and Display')
    
    sidebar_area()
    column1()
    column2()
    column3()

if __name__ == "__main__":
    main()
