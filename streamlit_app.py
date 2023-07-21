import streamlit as st
import json
import os
import elevenlabs
from elevenlabs import generate, play, voices

def split_text(text, limit=400):
    """Split the text into chunks of up to 400 characters."""
    words = text.split()
    chunks = []
    current_chunk = ''

    for word in words:
        if len(current_chunk) + len(word) <= limit:
            current_chunk += ' ' + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def save_voicelist(voice_list, filename="11voicelist.json"):
    with open(filename, "w") as f:
        json.dump(voice_list, f)

def load_voicelist(filename="11voicelist.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        voice_list = voices()
        save_voicelist(voice_list)
        return voice_list

st.title('ElevenLabs Audio Generator')

# Load or fetch voices and then display the dropdown
voice_list = load_voicelist()
selected_voice = st.selectbox('Select a voice:', voice_list)

user_input = st.text_area('Enter/Paste your text here:', height=200)

if user_input:
    # Splitting the input into 400 character chunks
    text_chunks = split_text(user_input)

    # Play each chunk in succession
    for chunk in text_chunks:
        audio = generate(text=chunk, voice=selected_voice, model="eleven_monolingual_v1")
        st.audio(audio.content, format='audio/wav')
