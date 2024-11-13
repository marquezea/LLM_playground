import streamlit as st
import utils as utils
import json

def header():
    st.subheader("🔧 Configuration")
    st.divider()

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
    display_voice_speed=False,
    display_skills=False)

tab1, tab2, tab3 = st.tabs(["Perfis", "RAG", "Prompts"])

with tab1:
    st.header("Perfis")
    perfis = st.session_state['settings']['skills']
    edited_skills = st.data_editor(perfis)

    btnSave = st.button("Salvar alterações", key='btnSaveSkills')
    if btnSave:
        st.session_state['settings']['skills'] = edited_skills
        with open("settings.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(st.session_state['settings'], indent=4))

with tab2:
    st.header("RAG")
    summarize = st.session_state['settings']['summarize_prompts']
    edited_summarize = st.data_editor(summarize)

    btnSave = st.button("Salvar alterações", key='btnSaveSummarize')
    if btnSave:
        st.session_state['settings']['summarize_prompts'] = edited_summarize
        with open("settings.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(st.session_state['settings'], indent=4))

with tab3:
    st.header("Default prompts")
    image_gen      = st.session_state['settings']['image_gen']['initial_text']
    text_to_speech = st.session_state['settings']['text_to_speech']['initial_text']
    music          = st.session_state['settings']['music']['initial_text']
    moderation     = st.session_state['settings']['moderation']['initial_text']
    tokens         = st.session_state['settings']['tokens']['initial_text']

    c1, c2 = st.columns(2)
    image_gen = c1.text_area("Image generation", image_gen)
    text_to_speech = c2.text_area("Text to speech", text_to_speech)
    c3, c4 = st.columns(2)
    music = c3.text_area("Music", music)
    moderation = c4.text_area("Moderation", moderation)
    c5, c6 = st.columns(2)
    tokens = c5.text_area("Tokens", tokens)

    btnSave = st.button("Salvar alterações", key='btnSavePrompts')
    if btnSave:
        st.session_state['settings']['image_gen']['initial_text'] = image_gen
        st.session_state['settings']['text_to_speech']['initial_text'] = text_to_speech
        st.session_state['settings']['music']['initial_text'] = music
        st.session_state['settings']['moderation']['initial_text'] = moderation
        st.session_state['settings']['tokens']['initial_text'] = tokens
        with open("settings.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(st.session_state['settings'], indent=4))