from google.adk.agents import Agent
from google.adk.tools import agent_tool
from LlmClient import llm_client

from Prompts import *
from Constants import *

llm = llm_client.get_llm_client()

positive_feedback_agent = Agent(
    name= "positive_feedback_agent_v1",
    model=llm,
    description=FEEDBACK_AGENT_DESC,
    instruction=POSITIVE_FEEDBACK_AGENT_PROMPT
)