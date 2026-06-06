from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import agent_tool

from LlmClient import llm_client
from AgentRunner import AgentRunner
from Prompts import *
from Constants import *
from Tools import create_ticket, search_ticket_with_id, search_ticket_with_message, check_ticket_id

import sys
import logging
import asyncio
import streamlit as st
import time


def global_exception_handler(exctype, value, traceback):
    """Catches any unhandled runtime exception globally."""
    logging.error("Unhandled exception occurred:", exc_info=(exctype, value, traceback))
    print(f"A critical error occurred: {value}. The system has logged this event.")


def create_all_agents():

    llm = llm_client.get_llm_client()
    intent_agent = Agent(
        name= INTENT_AGENT_NAME+VERSION_CODE,
        model=llm,
        description=INTENT_AGENT_DESC,
        instruction=INTENT_AGENT_PROMPT,
        output_key="user_message_intent"
    )

    positive_feedback_agent = Agent(
        name= "positive_feedback_agent_v1",
        model=llm,
        description=FEEDBACK_AGENT_DESC,
        instruction=POSITIVE_FEEDBACK_AGENT_PROMPT
    )

    create_ticket_agent = Agent(
        name= "create_ticket_agent_v1",
        model=llm,
        description=FEEDBACK_AGENT_DESC,
        instruction=CREATE_TICKET_AGENT_PROMPT,
        tools=[create_ticket, check_ticket_id]
    )

    search_ticket_agent = Agent(
        name= "search_ticket_agent_v1",
        model=llm,
        description=FEEDBACK_AGENT_DESC,
        instruction=SEARCH_TICKET_AGENT_PROMPT,
        tools=[search_ticket_with_message],
        sub_agents=[create_ticket_agent]
    )

    ticket_agent = SequentialAgent(
        name= "ticket_agent_v1",
        description="Entry agent for tickets",
        sub_agents=[search_ticket_agent]
    )

    query_agent = Agent(
        name= QUERY_AGENT_NAME+VERSION_CODE,
        model=llm,
        description=QUERY_AGENT_DESC,
        instruction=QUERY_AGENT_PROMPT,
        tools=[search_ticket_with_id]
    )

    intent_agent_as_tool = agent_tool.AgentTool(agent=intent_agent)

    coordinator_agent = Agent(
        name= COORDINATOR_AGENT_NAME+VERSION_CODE,
        model=llm,
        description=COORDINATOR_AGENT_DESC,
        instruction=COORDINATOR_AGENT_PROMPT,
        tools=[intent_agent_as_tool],
        sub_agents=[positive_feedback_agent, ticket_agent, query_agent]
    )

    return coordinator_agent

async def call_agents(chat_username, message):
    load_dotenv()
    sys.excepthook = global_exception_handler
    coordinator_agent = create_all_agents()
    agent_content = types.Content(role='user', parts=[types.Part(text=f"Username: {chat_username}"),
                                                  types.Part(text=f"User message: {message}")])
    agent_runner = AgentRunner(coordinator_agent, agent_content)
    agent_response = await agent_runner.execute_agent()
    return agent_response

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
            response = asyncio.run(call_agents(session_user_id, prompt))
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "user_id": session_user_id, "content": response})