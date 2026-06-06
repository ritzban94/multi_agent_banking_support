from google.adk.agents import Agent
from LlmClient import llm_client

from Prompts import *
from Constants import *
from Tools import create_ticket, check_ticket_id

llm = llm_client.get_llm_client()

create_ticket_agent = Agent(
    name= "create_ticket_agent_v1",
    model=llm,
    description=FEEDBACK_AGENT_DESC,
    instruction=CREATE_TICKET_AGENT_PROMPT,
    tools=[create_ticket, check_ticket_id]
)