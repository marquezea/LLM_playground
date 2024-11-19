import streamlit as st
import utils as utils
import base64
from openai import OpenAI

def header():
    st.subheader("🕵️ Vision")
    st.divider()

# Function to encode the image
def encode_image(file_image):
  #with open(image_path, "rb") as image_file:
  return base64.b64encode(file_image.getvalue()).decode('utf-8')

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
    display_skills=False,
    display_vision_model=True)

vision_options = [opt['title'] for opt in st.session_state['settings']['vision_prompts']]
action = st.selectbox("Select an option", vision_options)
prompt_index = vision_options.index(action)
vision_prompt = st.text_area("Prompt", height=100, value=st.session_state['settings']['vision_prompts'][prompt_index]['prompt'])

filename = st.file_uploader('Select a file', type=['jpg','jpeg','png','bmp','gif','tiff'])

if filename is not None:
    extension = filename.name.split('.')[-1]
    if extension in ['jpg','jpeg','png']:
        st.image(filename)
        base64_image = encode_image(filename)
        vision_model_engine = [vision_model_key for vision_model_title,vision_model_key in utils.VISION_MODELS.items() if vision_model_title == st.session_state.selected_vision_model][0]['model']
        client = utils.getVisionClient(st.session_state.selected_vision_model, vision_model_engine)
        utils.verbose('vision model engine',vision_model_engine)
    
        try:
            response = utils.vision(client, st.session_state.selected_vision_model, vision_model_engine, base64_image, vision_prompt)
            msg = utils.getVisionResponse(st.session_state.selected_vision_model, response)
            st.markdown("### Image description")
            st.markdown(msg)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            pass
    

        

