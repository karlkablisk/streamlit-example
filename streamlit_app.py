import streamlit as st
import elevenlabs
import json
import os
from elevenlabs import generate, voices
from IPython.display import Audio

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
    if api_key:
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

api_key_labels = [f"API Key {i+1}" for i in range(5)]
api_keys = [st.sidebar.text_input(label, value=initial_api_keys[i]) for i, label in enumerate(api_key_labels)]
marked_keys = st.session_state.get("marked_keys", [False]*5)

voice_list = fetch_voicelist()

# Manual API key selection
options = ["NONE"] + [f"API Key {i+1}" for i in range(5)]
selected_api_option = st.sidebar.selectbox("Manually select an API Key", options, index=0)

model_mapping = {
    'monolingual': 'eleven_monolingual_v1',
    'multilingual': 'eleven_multilingual_v1'
}
selected_model_name = st.selectbox("Select a model:", list(model_mapping.keys()))
selected_model = model_mapping[selected_model_name]
selected_voice = st.selectbox('Select a voice:', voice_list)
user_input = st.text_area('Enter/Paste your text here:', height=200)

if st.button('SPEAK') and user_input:
    generated = False
    used_api_key = "NONE"

    if selected_api_option != "NONE":
        api_idx = options.index(selected_api_option) - 1
        if api_keys[api_idx] and not marked_keys[api_idx]:
            try:
                audio = get_audio(user_input, selected_voice, selected_model, api_keys[api_idx])
                Audio(audio, autoplay=True)
                st.audio(audio, format='audio/wav')
                generated = True
                used_api_key = selected_api_option
            except:
                marked_keys[api_idx] = True

    if not generated:
        for idx, api_key in enumerate(api_keys):
            if api_key and not marked_keys[idx]:
                try:
                    audio = get_audio(user_input, selected_voice, selected_model, api_key)
                    Audio(audio, autoplay=True)
                    st.audio(audio, format='audio/wav')
                    generated = True
                    used_api_key = f"API Key {idx+1}"
                    break
                except:
                    marked_keys[idx] = True

    if not generated:
        try:
            audio = get_audio(user_input, selected_voice, selected_model)
            Audio(audio, autoplay=True)
            st.audio(audio, format='audio/wav')
            generated = True
        except:
            st.warning("Unable to generate audio, even without an API key.")

    if generated:
        st.write(f"Generated using: {used_api_key}")

    if 'streamlit' not in os.getcwd():
        save_api_keys_to_file(api_keys)

st.session_state.marked_keys = marked_keys
