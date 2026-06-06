from google.adk.agents import Agent
from google.adk.tools import agent_tool
from LlmClient import llm_client

from Prompts import *
from Constants import *
from agent_test.intent_agent.agent import intent_agent
from agent_test.positive_feedback_agent.agent import positive_feedback_agent
from agent_test.ticket_agent.agent import ticket_agent
from agent_test.query_agent.agent import query_agent

llm = llm_client.get_llm_client()
intent_agent_as_tool = agent_tool.AgentTool(agent=intent_agent)

root_agent = Agent(
    name= COORDINATOR_AGENT_NAME+VERSION_CODE,
    model=llm,
    description=COORDINATOR_AGENT_DESC,
    instruction=COORDINATOR_AGENT_PROMPT,
    tools=[intent_agent_as_tool],
    sub_agents=[positive_feedback_agent, ticket_agent, query_agent]
)