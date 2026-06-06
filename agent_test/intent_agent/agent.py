from google.adk.agents import Agent
from LlmClient import llm_client

from Prompts import *
from Constants import *

llm = llm_client.get_llm_client()

intent_agent = Agent(
    name= INTENT_AGENT_NAME+VERSION_CODE,
    model=llm,
    description=INTENT_AGENT_DESC,
    instruction=INTENT_AGENT_PROMPT,
    output_key="user_message_intent"
)