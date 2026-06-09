from typing import Any, Dict
from MySqlConnector import MySqlConnector
from sentence_transformers import SentenceTransformer, util

from Constants import *


def tool_success(key:str, result: Any) -> Dict[str, Any]:
    """Convenience function to return a success result."""
    return {
        'status': 'success',
        key: result
    }

def tool_error(message: str) -> Dict[str, Any]:
    """Convenience function to return an error result."""
    return {
        'status': 'error',
        'error_message': message
    }


def create_ticket(username: str, ticketId: int, user_message: str) -> dict:
    returnDict = {}
    db_connector = MySqlConnector()
    db_connector.connect_to_db()
    values = (ticketId, username, user_message)
    result = db_connector.execute_insert_query(INSERT_QUERY, values)
    if result == INSERT_SUCCESS_MSG:
        returnDict = tool_success(QUERY_RESULTS_STR, result)
    else:
        returnDict = tool_error(DB_CONNECTION_ERROR_MSG)
    db_connector.close_connector()
    return returnDict


def get_ticket_status(status_code: str) -> str:
    status_str = ""
    match status_code:
        case 'OP':
            status_str = 'Open'
        case 'IP':
            status_str = 'In Progress'
        case 'RS':
            status_str = 'Resolved'
        case 'BL':
            status_str = 'Blocked'
        case _:
            status_str = 'Not available'
    return status_str


def search_ticket_with_id(username: str, ticketId: int) -> dict:
    returnDict = {}
    db_connector = MySqlConnector()
    db_connector.connect_to_db()
    values = (ticketId, username)
    results = db_connector.execute_select_query(TICKET_STATUS_QUERY, values)
    if DB_CONNECTION_ERROR_MSG in results:
        returnDict = tool_error(DB_CONNECTION_ERROR_MSG)
    else:
        if not results:
            returnDict = tool_success(QUERY_RESULTS_STR, NOT_FOUND_STR)
        else:
            ticket_details = results[0]
            ticket_status = get_ticket_status(ticket_details[4])
            returnDict = tool_success(QUERY_RESULTS_STR, f'Found. Status is {ticket_status}')
    db_connector.close_connector()
    return returnDict


def check_ticket_id(ticketId: int) -> dict:
    returnDict = {}
    db_connector = MySqlConnector()
    db_connector.connect_to_db()
    values = (ticketId,)
    results = db_connector.execute_select_query(SEARCH_EXISTING_ID_QUERY, values)
    if DB_CONNECTION_ERROR_MSG in results:
        returnDict = tool_error(DB_CONNECTION_ERROR_MSG)
    else:
        if not results:
            returnDict = tool_success(QUERY_RESULTS_STR, NOT_FOUND_STR)
        else:
            returnDict = tool_success(QUERY_RESULTS_STR, FOUND_EXISTING_STR)
    db_connector.close_connector()
    return returnDict


def search_ticket_with_message(username: str, user_message: str) -> dict:
    returnDict = {}
    similarity_model = SentenceTransformer(MODEL_TXT_SIMILARITY)
    db_connector = MySqlConnector()
    db_connector.connect_to_db()
    values = (username,)
    results = db_connector.execute_select_query(OPEN_TICKETS_WITH_USER_QUERY, values)
    if DB_CONNECTION_ERROR_MSG in results:
        returnDict = tool_error(DB_CONNECTION_ERROR_MSG)
    else:
        if results != []:
            issue_desc_list = [data[3] for data in results]
            target_embedding = similarity_model.encode(user_message, convert_to_tensor=True)
            list_embeddings = similarity_model.encode(issue_desc_list, convert_to_tensor=True)
            cosine_scores = [score.item() for score in util.cos_sim(target_embedding, list_embeddings)[0]]
            highest_cosine_score = max(cosine_scores)
            target_issue = None
            if highest_cosine_score > 0.8:
                target_issue_desc = issue_desc_list[cosine_scores.index(highest_cosine_score)]
                target_idx = next((i for i, item in enumerate(results) if item[3] == target_issue_desc), -1)
                if target_idx != -1:
                    target_issue = results[target_idx]
            if target_issue != None:
                returnDict = tool_success(QUERY_RESULTS_STR, f'Found. Ticket Id is {target_issue[0]} and status is open.')
            else:
                returnDict = tool_success(QUERY_RESULTS_STR, NOT_FOUND_STR)
        else:
            returnDict = tool_success(QUERY_RESULTS_STR, NOT_FOUND_STR)
    db_connector.close_connector()
    return returnDict


def log_llm_response_and_eval(username: str, user_message: str, llm_response: str, llm_response_eval: str) -> dict:
    returnDict = {}
    db_connector = MySqlConnector()
    db_connector.connect_to_db()
    values = (username, user_message, llm_response, llm_response_eval)
    result = db_connector.execute_insert_query(LOG_INSERT_QUERY, values)
    if result == INSERT_SUCCESS_MSG:
        returnDict = tool_success(QUERY_RESULTS_STR, result)
    else:
        returnDict = tool_error(DB_CONNECTION_ERROR_MSG)
    db_connector.close_connector()
    return returnDict

