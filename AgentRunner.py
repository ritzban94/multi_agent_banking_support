from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from Constants import *

class AgentRunner:
    _agent: Agent
    _content: types.Content

    def __init__(self, agent: Agent, content: types.Content):
        self._agent = agent
        self._content = content

    async def execute_agent(self, initial_state: Optional[Dict[str, Any]] = {}) -> str:
        """Create session and runner for given agent and start agent execution."""
        app_name = self._agent.name + APP_CD
        user_id = self._agent.name + USER_CD
        session_id = self._agent.name + SESSION_CD

        session_service = InMemorySessionService()

        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )

        runner = Runner(
            agent=self._agent,
            app_name=app_name,
            session_service=session_service,
        )

        response_text = "Agent did not produce a final response"

        verbose= False

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=self._content):
            if verbose:
                print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text ## # Assuming text response in the first part

                elif event.actions and event.actions.escalate:
                    response_text = f"Agent escalated: {event.error_message or 'No specific message provided.'}"
    
        return response_text