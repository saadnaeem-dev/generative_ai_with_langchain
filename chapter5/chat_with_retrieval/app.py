"""Document loading functionality.

Run like this:
> PYTHONPATH=. streamlit run chapter5/chat_with_retrieval/app.py
"""

import streamlit as st

from chapter5.chat_with_retrieval.chat_with_documents import add_uploaded_docs, answer_question
from chapter5.chat_with_retrieval.utils import LOGGER, MEMORY, DocumentLoader

LOGGER.info("Show title")
st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("🦜 LangChain: Chat with Documents")


LOGGER.info("Upload files")
uploaded_files = st.sidebar.file_uploader(
    label="Upload files",
    type=list(DocumentLoader.supported_extensions.keys()),
    accept_multiple_files=True,
)
if not uploaded_files:
    st.info("Please upload documents to continue.")
    st.stop()

LOGGER.info("Configure chain")
add_uploaded_docs(uploaded_files=uploaded_files)

avatars = {"human": "user", "ai": "assistant"}

if len(MEMORY.chat_memory.messages) == 0:
    st.chat_message("assistant").markdown("Ask me anything!")

for msg in MEMORY.chat_memory.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

LOGGER.info("Chat interface")
container = st.container()
assistant = st.chat_message("assistant")
if user_query := st.chat_input(placeholder="Give me 3 keywords for what you have right now"):
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        response = answer_question(user_query)
        # Display the response from the chatbot
        if response:
            container.markdown(response)
