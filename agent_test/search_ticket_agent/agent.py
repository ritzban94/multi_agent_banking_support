from google.adk.agents import Agent
from LlmClient import llm_client

from Prompts import *
from Constants import *
from Tools import search_ticket_with_message
from agent_test.create_ticket_agent.agent import create_ticket_agent

llm = llm_client.get_llm_client()

search_ticket_agent = Agent(
    name= "search_ticket_agent_v1",
    model=llm,
    description=FEEDBACK_AGENT_DESC,
    instruction=SEARCH_TICKET_AGENT_PROMPT,
    tools=[search_ticket_with_message],
    sub_agents=[create_ticket_agent]
)