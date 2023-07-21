import streamlit as st

def main():
    st.title("Web Audio API with Streamlit")

    # Example audio file (replace with your audio file URL)
    audio_url = "https://example.com/audio_file.mp3"

    st.write("Audio Player:")
    st.audio(audio_url, format="audio/mp3", start_time=0)

    st.write("Volume Control:")
    volume = st.slider("Volume", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

    st.write("Instructions:")
    st.write("1. Adjust the volume using the slider above.")
    st.write("2. Press play on the audio player to hear the audio.")

if __name__ == "__main__":
    main()
