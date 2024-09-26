import streamlit as st
import utils as utils
import json
import pdfplumber
import os
import tiktoken

def header():
    st.subheader("↗🦥 RAG")
    st.divider()

def extractPDFText_pdfplumber(file):
    raw_text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            raw_text += text
    return raw_text

def extractText_text(file):
    return file.read().decode('utf-8')

# setup applicaiton
utils.initialize()

# display header bar
header()

# display side bar
utils.display_sidebar(
    display_model=True,
    display_image_model=False,
    display_max_tokens=True, 
    display_temperature=True,
    display_resolution=False,
    display_quality=False,
    display_verbose=False,
    display_usage=True,
    display_voice=False,
    display_voice_speed=False,
    display_skills=False)

options = ["Sumarizar documento", "Traduzir documento"]
options_buttons = ["Sumarizar", "Traduzir"]
extracted_text = ""
initial_prompts = ["""Você vai atuar como um assistente para entender este DOCUMENTO. Preciso que você analise, fornecendo as seguintes informações:
a) Qual é o resumo deste documento em um parágrafo?
b) Quem é o público-alvo deste documento?
c) Quais são os requisitos de conhecimento para entender este documento?
d) Que tipo de documento é este?
e) Quais são os pontos mais importantes em bullets?
f) Quais conclusões este documento fornece?""",
"""Você vai traduzir este documento para o português."""]
action = st.selectbox("Selecione uma ação", options)
st.markdown(f"### {action} com RAG")
prompt_index = options.index(action)
summarize_prompt = st.text_area("Instruções", height=200, value=initial_prompts[prompt_index])
uploadForm = st.form('Upload PDF', clear_on_submit=True)
filename = uploadForm.file_uploader('Selecione um documento', type=['pdf','txt','doc'])


if filename is not None:
    extension = filename.name.split('.')[-1]
    if extension == 'pdf':
        extracted_text = extractPDFText_pdfplumber(filename)
    if extension == 'txt':
        extracted_text = extractText_text(filename)
    if extracted_text != '':
        model_engine = [model_key for model_title,model_key in utils.MODELS.items() if model_title == st.session_state.selected_model][0]['model']
        prompt = summarize_prompt + "\n\n DOCUMENTO:\n\n" + extracted_text
        count_tokens = utils.countTokens(prompt)
        max_tokens = utils.MODELS[st.session_state.selected_model]['max_tokens']
        if utils.countTokens(prompt) > max_tokens:
            st.error(f"O modelo {st.session_state.selected_model} suporta ate {max_tokens}, e seu prompt tem {count_tokens} tokens. Selecione um documento menor.")
        else:
            st.write(f"O prompt tem {count_tokens} tokens e o modelo suporta ate {max_tokens}.")
            client = utils.getLLMClient(st.session_state.selected_model, model_engine)
            response = utils.simplePrompt(st.session_state.selected_model, client, model_engine, prompt)
            utils.updateUsage(st.session_state.selected_model, response)
            msg = utils.getResponse(st.session_state.selected_model, response)
            st.markdown(f'#### :orange[{filename.name}]')
            st.write(msg)
        
submit = uploadForm.form_submit_button(f'{options_buttons[prompt_index]}')

