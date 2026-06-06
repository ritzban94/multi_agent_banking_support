import streamlit as st
import time

st.header("Banking Customer Support AI Agent")
st.divider()
st.markdown("""
A multi-agent AI banking assistant that classifies customer queries and feedback, delivers personalized responses, and provides real-time ticket updates to improve support efficiency and customer experience.
""")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if 'initialized' not in st.session_state or not st.session_state.initialized:
    user_id = st.chat_input("Enter user id to proceed..")
    if user_id:
        st.session_state.user_id = user_id
        st.session_state.initialized = True
        st.toast(f"User id : {user_id}", icon=":material/thumb_up:")
        time.sleep(0.5)
        st.rerun()
else:
    session_user_id = st.session_state.get("user_id")
    if prompt := st.chat_input("Type your problem here.."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "user_id": session_user_id, "content": prompt})
        with st.spinner("Thinking...", show_time=True):
            time.sleep(0.5)
            response = "User said something"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "user_id": session_user_id, "content": response})
