import streamlit as st
import elevenlabs
import json
import os
from elevenlabs import generate, voices

def split_text(text, limit=400):
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

def fetch_voicelist():
    try:
        return voices()
    except:
        st.sidebar.warning("There was an issue loading the voice list. Defaulting to predefined list.")
        return ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"]

def get_audio(text, voice="Bella", model="eleven_monolingual_v1", api_key=None):
    if api_key:  # only set api_key if it's provided
        elevenlabs.api_key = api_key
    return generate(
        text=text,
        voice=voice,
        model=model
    )

def save_api_keys_to_file(api_keys):
    with open("api_keys.json", "w") as f:
        json.dump(api_keys, f)

def load_api_keys_from_file():
    if os.path.exists("api_keys.json"):
        with open("api_keys.json", "r") as f:
            return json.load(f)
    return ["" for _ in range(5)]

st.title('ElevenLabs Audio Generator')

# If not on streamlit's cloud and file exists, load API keys from it
if 'streamlit' not in os.getcwd():
    initial_api_keys = load_api_keys_from_file()
else:
    initial_api_keys = ["" for _ in range(5)]

# Sidebar for API key input
api_key_labels = [f"API Key {i+1}" for i in range(5)]
api_keys = [st.sidebar.text_input(label, value=initial_api_keys[i]) for i, label in enumerate(api_key_labels)]
marked_keys = st.session_state.get("marked_keys", [False]*5)


# Display marked API keys
for idx, marked in enumerate(marked_keys):
    if marked:
        st.sidebar.markdown(f"<span style='color:red'>x</span> API Key {idx+1} is marked as full.", unsafe_allow_html=True)
