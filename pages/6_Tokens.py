import streamlit as st
import utils as utils
from pathlib import Path
from openai import OpenAI
import json
import tiktoken
import torch
from transformers import BertTokenizer, BertModel

# Load pre-trained model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Function to create embeddings
def create_embeddings(sentence):
    # Tokenize the input sentence
    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)

    # Get the embeddings from the model
    with torch.no_grad():
        outputs = model(**inputs)

    # The last hidden state is the first element of the output tuple
    last_hidden_state = outputs.last_hidden_state

    # We can take the mean of the last hidden state to get a single vector for the sentence
    sentence_embedding = last_hidden_state.mean(dim=1)

    return sentence_embedding

def tokenize_and_print(text, encoding_name="cl100k_base"):
    try:
        # Get the encoding
        encoding = tiktoken.get_encoding(encoding_name)

        # Tokenize the text
        tokens_int = encoding.encode(text)
        tokens_txt = [encoding.decode([token]) for token in tokens_int]

        return tokens_int, tokens_txt

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def header():
    st.subheader("🪙 Tokens")
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
    
    sentence = st.text_area("Write anything to convert into tokens", st.session_state['settings']['tokens']['initial_text'])
    if st.button("Convert to Tokens"):
        tokens_int, tokens_txt = tokenize_and_print(sentence)
        st.markdown(f"### Qtde de Tokens: {len(tokens_int)}")
        st.dataframe(
            {"tokenid": tokens_int, "tokenstr": tokens_txt}, 
            use_container_width=True,
            column_config={
                "tokenid": st.column_config.TextColumn("Token #"),
                "tokenstr": st.column_config.TextColumn("Token"),
            })
    if st.button("Convert to Embeddings"):
        embeddings = create_embeddings(sentence)

        st.write(embeddings)

if __name__ == "__main__":
    main()