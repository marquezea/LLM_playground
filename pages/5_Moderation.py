import streamlit as st
import utils as utils
from pathlib import Path
from openai import OpenAI
import json

def header():
    st.subheader("🧐 Text Moderation")
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
        display_voice=False,
        display_voice_speed=False,)
    
    moderation_text = st.text_area("Write something bad", "I want to kill you.")
    if st.button("Moderate"):
        client = OpenAI()
        response = client.moderations.create(input=moderation_text)
        if response.results[0].flagged:
            categories = json.loads(response.results[0].categories.json())
            reds = ', '.join([f":red[{k.upper()}]" for k,v in categories.items() if v])
            greens = ', '.join([f":green[{k.upper()}]" for k,v in categories.items() if not v])
            st.markdown('#### WARNINGS')
            st.markdown(f'##### {reds}')
            st.markdown('#### SAFE')
            st.markdown(f'##### {greens}')
        else:
            st.markdown('#### THIS IS SAFE')
if __name__ == "__main__":
    main()