from google.adk.agents import Agent
from LlmClient import llm_client

from Prompts import *
from Constants import *
from Tools import search_ticket_with_id

llm = llm_client.get_llm_client()

query_agent = Agent(
    name= QUERY_AGENT_NAME+VERSION_CODE,
    model=llm,
    description=QUERY_AGENT_DESC,
    instruction=QUERY_AGENT_PROMPT,
    tools=[search_ticket_with_id]
)