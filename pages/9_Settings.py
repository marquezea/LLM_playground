import streamlit as st
import utils as utils
import requests

def get_OpenAI_billing_credit_grants():
    print('Calling api')
    url = "https://api.openai.com/dashboard/billing/credit_grants"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://platform.openai.com/",
        "Authorization": "Bearer sess-girJhYldDVMMtEwCJRQUUliPqggLBwtAcEGdUZse"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def header():
    st.subheader("🕸️ Settings")
    st.divider()

def main():
    # setup applicaiton
    utils.initialize()

    # display header bar
    header()

    # display tabs
    tabSkills, tabCosts = st.tabs(["Skills", "Costs"])
    with tabSkills:
        st.write("List of Skills")
    
    with tabCosts:
        openAI_result = get_OpenAI_billing_credit_grants()
        st.json(openAI_result)
if __name__ == "__main__":
    main()