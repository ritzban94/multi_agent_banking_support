import os
from mysql import connector

from Constants import INSERT_SUCCESS_MSG, INSERT_FAILURE_MSG, DB_CONNECTION_ERROR_MSG

class MySqlConnector:
    """
    A wrapper for querying MySql which returns query results.
    """
    _db_connector = None
    _db_host = None
    _db_port = None
    _db_user = None
    _db_password = None
    _db_database = None

    def __init__(self):
        self._db_host = os.getenv("MYSQL_HOST")
        self._db_port = os.getenv("MYSQL_PORT")
        self._db_user = os.getenv("MYSQL_USER")
        self._db_password = os.getenv("MYSQL_PASSWORD")
        self._db_database = os.getenv("MYSQL_DATABASE")

    def connect_to_db(self):
        self._db_connector = connector.connect(
            host=self._db_host,
            port=self._db_port,
            user=self._db_user,
            password=self._db_password,
            database=self._db_database
        )
    
    def close_connector(self):
        self._db_connector.close()
    
    def execute_insert_query(self, query: str, parameters: tuple) -> str:
        return_message = ""
        if self._db_connector.is_connected():
            cursor = self._db_connector.cursor()
            cursor.execute(query, parameters)
            self._db_connector.commit()
            cursor.close()
            return_message = INSERT_SUCCESS_MSG
        else:
            return_message = INSERT_FAILURE_MSG
        return return_message
    
    def execute_select_query(self, query: str, parameters: tuple) -> list:
        query_results = []
        if self._db_connector.is_connected():
            cursor = self._db_connector.cursor()
            cursor.execute(query, parameters)
            query_results = cursor.fetchall()
        else:
            query_results.append(DB_CONNECTION_ERROR_MSG)
        return query_results

