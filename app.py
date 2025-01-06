import streamlit as st
from chatbot import ChatBot
from config import TASK_SPECIFIC_INSTRUCTIONS
from zetalogger import logger
 
def main():
    st.title("Chat with ZetaBot, a statistics assistant")

    # add a file uploader so user can upload their own data
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        logger.debug(f"Uploaded file: {uploaded_file.name}")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "content": TASK_SPECIFIC_INSTRUCTIONS},
            {"role": "assistant", "content": "Understood"}
        ]
    chatbot = ChatBot(st.session_state, uploaded_file)

    # Display user and assistant messages skipping the first two
    for message in st.session_state.messages[2:]:
        # ignore tool use blocks
        if isinstance(message["content"], str):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    if user_msg := st.chat_input("Type your message here..."):
        st.chat_message("user").markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("ZetaBot is thinking..."):
                response_placeholder = st.empty()
                full_response = chatbot.process_user_input(user_msg)
                response_placeholder.markdown(full_response)

if __name__ == "__main__":
    main()
