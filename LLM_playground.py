import streamlit as st
import utils as utils

def main():

    # setup applicaiton
    utils.initialize()

    st.title('LLM Playground')
    st.markdown('##### An educational playground for exploring and demonstrating various use cases and concepts of Large Language Models (LLMs).')
    st.divider()
    st.markdown('##### :blue[by Adriano Marqueze - release 13-Nov-2024]')

if __name__ == "__main__":
    main()

