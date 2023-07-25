import streamlit as st
import elevenlabs
from elevenlabs import generate, voices, Models
from typing import Optional, List

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

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_voicelist():
    try:
        voice_list = voices()
        return voice_list
    except:
        st.warning("There was an issue loading the voice list. Defaulting to 'Bella'.")
        return ["Bella"]

def get_audio_with_key(api_key, text, voice="Bella", model="eleven_monolingual_v1"):
    elevenlabs.api_key = api_key
    return generate(
        text=text,
        voice=voice,
        model=model
    )

st.title('ElevenLabs Audio Generator')

# Sidebar for API key input
api_keys = [st.sidebar.text_input(f"API Key {i+1}") for i in range(5)]
marked_keys = st.session_state.get("marked_keys", [False]*5)

# Manual API key selection
selected_api_index = st.sidebar.selectbox("Manually select an API Key", list(range(1, 6)), index=0)

# Model selection dropdown
models = Models.from_api()
selected_model = st.selectbox("Select a model:", [model.id for model in models])

# Load or fetch voices and then display the dropdown
voice_list = load_voicelist()
selected_voice = st.selectbox('Select a voice:', voice_list)

user_input = st.text_area('Enter/Paste your text here:', height=200)

if user_input:
    generated = False

    # Use manually selected API key if it's valid
    if api_keys[selected_api_index - 1] and not marked_keys[selected_api_index - 1]:
        try:
            audio = get_audio_with_key(api_keys[selected_api_index - 1], user_input, selected_voice, selected_model)
            st.audio(audio, format='audio/wav')
            generated = True
        except:
            marked_keys[selected_api_index - 1] = True
            st.sidebar.markdown(f"API Key {selected_api_index} is marked as full.")

    # If manually selected API key failed or wasn't valid, try the rest
    if not generated:
        for idx, api_key in enumerate(api_keys):
            if api_key and not marked_keys[idx]:
                try:
                    audio = get_audio_with_key(api_key, user_input, selected_voice, selected_model)
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
