JUDGE_MODEL_GPT = "openai/gpt-4o"
MODEL_GPT = "openai/gpt-4o-mini"
MODEL_TXT_SIMILARITY = "all-MiniLM-L6-v2"
MODEL_GPT_USER_INIT_MESSAGE = "Are you ready?"
MODEL_GPT_SYS_INIT_MESSAGE = "You are a helpful Banking Customer Support agent, chatting with a user to come up with an appropriate response."
JUDGE_MODEL_GPT_SYS_INIT_MESSAGE = "You are an expert evaluator."

VERSION_CODE="_v1"

INTENT_AGENT_NAME="intent_agent"
INTENT_AGENT_DESC="Classifies the user query based on intent"

FEEDBACK_AGENT_NAME="feedback_agent"
FEEDBACK_AGENT_DESC="Generates appropriate response to the user feedback"

QUERY_AGENT_NAME="query_agent"
QUERY_AGENT_DESC="Generates appropriate response to the user query"

COORDINATOR_AGENT_NAME="coordinator_agent"
COORDINATOR_AGENT_DESC="Main coordinator."

APP_CD="_app_1"
USER_CD="_user_1"
SESSION_CD="_session_01"

QUERY_RESULTS_STR = "query_results"
NOT_FOUND_STR = "Not found."
FOUND_EXISTING_STR = "Found existing ticket."

DB_CONNECTION_ERROR_MSG = "Database connection error - Database is not connected."

INSERT_FAILURE_MSG = "Row insert failure."

INSERT_SUCCESS_MSG = "Row insert successful."

INSERT_QUERY = "INSERT INTO tickets (id, username, issue_create_dt, issue_desc, issue_status) VALUES (%s, %s, sysdate(), %s, 'OP')"

LOG_INSERT_QUERY = "INSERT INTO llm_response_log (username, user_message, llm_response, llm_response_eval, create_dt) VALUES (%s, %s,  %s, %s, sysdate())"

SEARCH_EXISTING_ID_QUERY = "SELECT * FROM tickets WHERE id = %s"

TICKET_STATUS_QUERY = "SELECT * FROM tickets WHERE id = %s AND username = %s"

OPEN_TICKETS_WITH_USER_QUERY = "SELECT * FROM tickets WHERE username = %s and issue_status = 'OP'"