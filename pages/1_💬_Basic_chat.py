import streamlit as st
import utils as utils

def header():
    st.subheader("💬 Basic Chat")
    st.divider()
    clear_button = st.button("Clear Chat")
    if clear_button:
        utils.clear_messages()

def chatInteraction():
    # ask for a chat prompt input
    prompt = st.chat_input()
    if prompt:
        model_engine = [model_key for model_title,model_key in utils.MODELS.items() if model_title == st.session_state.selected_model][0]['model']
        client = utils.getLLMClient(st.session_state.selected_model, model_engine)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        utils.verbose('model engine',model_engine)
        try:
            response = utils.chatCompletion(st.session_state.selected_model, client, model_engine)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
        try:
            utils.verbose('response',response.json())
        except:
            utils.verbose('response', response)
        utils.updateUsage(st.session_state.selected_model, response)
        utils.verbose('usage acum',st.session_state.usage)
        msg = utils.getResponse(st.session_state.selected_model, response)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
            
def main():
    # setup applicaiton
    utils.initialize()

    # display header bar
    header()

    # display side bar
    utils.display_sidebar()

    # display all the messages in the session (history of all chat messages)
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    chatInteraction()

if __name__ == "__main__":
    main()