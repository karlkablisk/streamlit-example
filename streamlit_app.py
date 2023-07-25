import streamlit as st
import elevenlabs
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
    # Generate audio using the provided parameters.
    if api_key:  # only set api_key if it's provided
        elevenlabs.api_key = api_key
    return generate(
        text=text,
        voice=voice,
        model=model
    )

st.title('ElevenLabs Audio Generator')

# Sidebar for API key input
api_key_labels = [f"API Key {i+1}" for i in range(5)]
api_keys = [st.sidebar.text_input(label) for label in api_key_labels]
marked_keys = st.session_state.get("marked_keys", [False]*5)

# Display marked API keys
for idx, marked in enumerate(marked_keys):
    if marked:
        st.sidebar.markdown(f"<span style='color:red'>x</span> API Key {idx+1} is marked as full.", unsafe_allow_html=True)

# Button to fetch new voice list
if st.sidebar.button('Fetch New Voice List'):
    voice_list = fetch_voicelist()
else:
    voice_list = ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"]

# Manual API key selection
options = ["NONE"] + [f"API Key {i+1}" for i in range(5)]
selected_api_option = st.sidebar.selectbox("Manually select an API Key", options, index=0)

# Model selection dropdown
model_mapping = {
    'monolingual': 'eleven_monolingual_v1',
    'multilingual': 'eleven_multilingual_v1'
}
selected_model_name = st.selectbox("Select a model:", list(model_mapping.keys()))
selected_model = model_mapping[selected_model_name]

# Display the dropdown for voices
selected_voice = st.selectbox('Select a voice:', voice_list)

user_input = st.text_area('Enter/Paste your text here:', height=200)

みなさん、おはようございます
