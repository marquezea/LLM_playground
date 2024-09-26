import streamlit as st
import utils as utils
from openai import OpenAI

def header():
    st.subheader("📢 Text To Speech")
    st.divider()

def main():
    # setup applicaiton
    utils.initialize()

    # display header bar
    header()

    # display side bar
    utils.display_sidebar(
        display_model=False,
        display_image_model=False,
        display_max_tokens=False, 
        display_temperature=False,
        display_resolution=False,
        display_quality=False,
        display_verbose=False,
        display_usage=False,
        display_voice=True,
        display_voice_speed=True,)
    
    speech_text = st.text_area("Write something that I'll speech for you", st.session_state['settings']['text_to_speech']['initial_text'])
    if st.button("Speak"):
        client = OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            speed=st.session_state['voice_speed'],
            voice=st.session_state['voice'],
            input=speech_text
        )
        st.audio(response.content, format="audio/mp3")
if __name__ == "__main__":
    main()