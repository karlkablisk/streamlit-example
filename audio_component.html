import streamlit as st
from elevenlabs import voices, generate

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

st.title('ElevenLabs Audio Generator')

user_input = st.text_area('Enter/Paste your text here:', height=200)

if user_input:
    # Splitting the input into 400 character chunks
    text_chunks = split_text(user_input)

    # Display the list of voices
    voice_list = voices()
    selected_voice = st.selectbox('Select a voice:', voice_list)

    # Play each chunk in succession
    for chunk in text_chunks:
        audio = generate(text=chunk, voice=selected_voice)
        st.audio(audio.content, format='audio/wav')
