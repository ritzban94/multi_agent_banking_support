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
        response_logs = { "agents" : ['coordinator_agent', 'intent_agent'], "action": "", "status": "" }
        verbose= True

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=self._content):
            if verbose:
                print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")
            
            if event.content and event.content.parts:
                event_part = event.content.parts[0]
                if event_part.function_response and event_part.function_response.name == 'intent_agent_v1':
                    response_logs["action"] = event_part.function_response.response.get("result")
                if event_part.function_call and event_part.function_call.name == 'transfer_to_agent':
                    response_logs["agents"].append(event_part.function_call.args.get('agent_name')[:-3])

            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text ## # Assuming text response in the first part
                    response_logs["status"] = "Success"

                elif event.actions and event.actions.escalate:
                    response_text = f"Agent escalated: {event.error_message or 'No specific message provided.'}"
                    response_logs["status"] = "Fail"


        await session_service.delete_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
    
        return response_text, response_logs