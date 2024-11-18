import streamlit as st
import utils as utils
import pdfplumber

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

options = [opt['title'] for opt in st.session_state['settings']['summarize_prompts']]
options_buttons = [opt['button_label'] for opt in st.session_state['settings']['summarize_prompts']]
extracted_text = ""
action = st.selectbox("Select an action", options)
st.markdown(f"### {action} com RAG")
prompt_index = options.index(action)
summarize_prompt = st.text_area("Instructions", height=200, value=st.session_state['settings']['summarize_prompts'][prompt_index]['prompt'])
uploadForm = st.form('Upload PDF', clear_on_submit=True)
filename = uploadForm.file_uploader('Select a document', type=['pdf','txt'])


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
            st.error(f"This model  {st.session_state.selected_model} supports up to {max_tokens} tokens. Your prompt has {count_tokens} tokens. Select a smaller document or change to another model.")
        else:
            st.write(f"This prompt will use {count_tokens} tokens and the model supports up to {max_tokens} tokens.")
            client = utils.getLLMClient(st.session_state.selected_model, model_engine)
            response = utils.simplePrompt(st.session_state.selected_model, client, model_engine, prompt)
            utils.updateUsage(st.session_state.selected_model, response)
            msg = utils.getResponse(st.session_state.selected_model, response)
            st.markdown(f'#### :orange[{filename.name}]')
            st.write(msg)
        
submit = uploadForm.form_submit_button(f'{options_buttons[prompt_index]}')

