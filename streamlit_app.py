import streamlit as st
import json
import os
import elevenlabs
from elevenlabs import generate, play, voices

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

def save_voicelist(voice_list, filename="11voicelist.json"):
    with open(filename, "w") as f:
        json.dump(voice_list, f)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_voicelist(filename="11voicelist.json"):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        else:
            voice_list = voices()
            save_voicelist(voice_list)
            return voice_list
    except (json.JSONDecodeError, FileNotFoundError):
        st.warning("There was an issue loading the voice list. Defaulting to 'Bella'.")
        return ["Bella"]

def get_audio_with_key(api_key, text, voice="Bella"):
    elevenlabs.api_key = api_key
    return generate(
        text=text,
        voice=voice,
        model="eleven_monolingual_v1"
    )

st.title('ElevenLabs Audio Generator')

# Sidebar for API key input
api_keys = [st.sidebar.text_input(f"API Key {i+1}") for i in range(5)]
marked_keys = st.session_state.get("marked_keys", [False]*5)

# Load or fetch voices and then display the dropdown
voice_list = load_voicelist()
selected_voice = st.selectbox('Select a voice:', voice_list)

user_input = st.text_area('Enter/Paste your text here:', height=200)

if user_input:
    generated = False
    for idx, api_key in enumerate(api_keys):
        if api_key and not marked_keys[idx]:
            try:
                audio = get_audio_with_key(api_key, user_input, selected_voice)
                st.audio(audio, format='audio/wav')
                generated = True
                break
            except:
                marked_keys[idx] = True
                st.sidebar.markdown(f"API Key {idx+1} is marked as full.")
    
    # If no valid API keys, or they all failed
    if not generated:
        # Splitting the input into 400 character chunks
        text_chunks = split_text(user_input)

        for chunk in text_chunks:
            audio = get_audio(chunk, selected_voice)
            st.audio(audio, format='audio/wav')

st.session_state.marked_keys = marked_keys
