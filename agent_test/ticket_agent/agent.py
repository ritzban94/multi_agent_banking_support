from google.adk.agents import SequentialAgent
from agent_test.search_ticket_agent.agent import search_ticket_agent

ticket_agent = SequentialAgent(
    name= "ticket_agent_v1",
    description="Entry agent for tickets",
    sub_agents=[search_ticket_agent]
)