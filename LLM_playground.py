import streamlit as st
import utils as utils

def main():

    # setup applicaiton
    utils.initialize()

    st.title('LLM Playground')
    st.markdown('##### An educational playground for exploring and demonstrating various use cases and concepts of Large Language Models (LLMs).')
    st.divider()
    st.markdown('##### :blue[by Adriano Marqueze - Sep-2024]')

    # if st.button("Test Hugging Face API"):
    #     import requests

    #     API_URL = "https://api-inference.huggingface.co/models/cross-encoder/ms-marco-MiniLM-L-12-v2"
    #     headers = {"Authorization": "Bearer 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"}

    #     def query(payload):
    #         response = requests.post(API_URL, headers=headers, json=payload)
    #         return response.json()
            
    #     output = query({
    #         "inputs": "I like you. I love you",
    #     })
    #     st.json(output)   

if __name__ == "__main__":
    main()


# from huggingface_hub import InferenceClient

# client = InferenceClient(
#     "google/gemma-7b-it",
#     token="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
# )

# for message in client.chat_completion(
# 	messages=[{"role": "user", "content": "What is the capital of France?"}],
# 	max_tokens=500,
# 	stream=True,
# ):
#     print(message.choices[0].delta.content, end="")