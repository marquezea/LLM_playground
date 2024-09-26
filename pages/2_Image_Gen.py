import streamlit as st
import utils as utils
import base64
from io import BytesIO
from PIL import Image
import requests
import os

def header():
    st.subheader("🧑‍🎨 Image Generator")
    st.divider()

def main():
    # setup applicaiton
    utils.initialize()

    # display header bar
    header()

    # display side bar
    utils.display_sidebar(
        display_model=False,
        display_image_model=True,
        display_max_tokens=False, 
        display_temperature=False,
        display_resolution=True,
        display_quality=True,
        display_verbose=False,
        display_usage=False,)
    
    image_prompt = st.text_area("Describe the image you want to generate", "Uma sala de aula com alunos animados com a aula de inteligência artificial.")
    if st.session_state['operation_mode'] == 'sync':
        if st.button("Generate Image"):
            img_model_engine = [model_key for model_title,model_key in utils.IMAGE_MODELS.items() if model_title == st.session_state.selected_img_model][0]['model']
            client = utils.getImageClient(st.session_state.selected_img_model, img_model_engine)
            response = utils.generateImage(
                st.session_state.selected_img_model, 
                client, 
                img_model_engine, 
                image_prompt,
                st.session_state.resolution,
                st.session_state.quality)
            image = utils.getImageResponse(st.session_state.selected_img_model, response)

            st.image(image, use_column_width=True)
    if st.session_state['operation_mode'] == 'async':
        col1, col2 = st.columns([1,2])
        if col1.button("Request Image Generation"):
            img_model_engine = [model_key for model_title,model_key in utils.IMAGE_MODELS.items() if model_title == st.session_state.selected_img_model][0]['model']
            client = utils.getImageClient(st.session_state.selected_img_model, img_model_engine)
            response = utils.generateImage(
                st.session_state.selected_img_model, 
                client, 
                img_model_engine, 
                image_prompt,
                st.session_state.resolution,
                st.session_state.quality)
            if response.status_code == 200:
                st.session_state['image_id'] = response.json()['sdGenerationJob']['generationId']
            else:
                st.warning(f"Image request failed: {response.status_code}")
        if st.session_state['image_id'] != '':
            if col2.button(f"Get Image {st.session_state['image_id']}"):
                response = requests.get(
                    f"https://cloud.leonardo.ai/api/rest/v1/generations/{st.session_state['image_id']}",
                    headers={
                        "accept": "application/json",
                        "authorization": f"Bearer {os.environ["LEONARDO_API_KEY"]}"
                    }
                )
                if response.status_code == 200:
                    if response.json()['generations_by_pk']['status'] == 'COMPLETE':
                        image_url = response.json()['generations_by_pk']['generated_images'][0]['url']
                        st.image(image_url, use_column_width=True)
                    else:
                        st.write('Image not ready yet')

if __name__ == "__main__":
    main()