import streamlit as st
import utils as utils
import requests
import os
import uuid

music_folder = "./music_files"

def clean_string(string):
    return string.replace('\\', '\\\\')

# function to generate a filename based on the music prompt (using Mistral-7B-Instruct-v0.1)
def generate_filename():
    generation = str(uuid.uuid4()).split('-')[0]
    filename = f"{generation}.mp3"
    return filename

# function that retrieves the MP3 files from given directory
def get_mp3_files(directory):
    mp3_files = []
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            mp3_files.append(file)
    return mp3_files

def save_mp3_to_disk(response_content, filename='output.mp3'):
    try:
        with open(filename, 'wb') as file:
            file.write(response_content)
    except Exception as e:
        print(f"An error occurred while saving the MP3 file: {e}")

def header():
    st.subheader("🎷 Music")
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
    
    music_prompt = st.text_area("Write any inpiration message for a music", st.session_state['settings']['music']['initial_text'])

    if st.button("Generate Music"):
        suggested_filename = generate_filename()
        response = requests.post(
            f"https://api-inference.huggingface.co/models/facebook/musicgen-small",
            headers={
                "Authorization": f"Bearer {os.environ["HFINF_API_KEY"]}"
            },
            data={
                "input": f"{music_prompt}"
            },
        )
        if response.status_code == 200:
            save_mp3_to_disk(response.content, filename=f"{music_folder}/{suggested_filename}")

        #st.audio(response.content, format="audio/mp3")
    previous_mp3_files = get_mp3_files(music_folder)
    st.markdown("#### :blue[Previous MP3 Files]")
    col1, col2, col3 = st.columns(3)
    for i, audio_file in enumerate(previous_mp3_files):
        if i % 3 == 0:
            with col1:
                st.write(audio_file)
                st.audio(f"{music_folder}/{audio_file}", format="audio/mp3")
        elif i % 3 == 1:
            with col2:
                st.write(audio_file)
                st.audio(f"{music_folder}/{audio_file}", format="audio/mp3")
        else:
            with col3:
                st.write(audio_file)
                st.audio(f"{music_folder}/{audio_file}", format="audio/mp3")

if __name__ == "__main__":
    main()


# a catchy beat for a podcast intro
# a funky house with 80s hip hop vibes
# a grand, epic, rhythmic, march-like quality of the music with medieval and fantasy elements

