USE ticketDb;

CREATE TABLE tickets (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    issue_create_dt DATE NOT NULL,
    issue_desc VARCHAR(400) NOT NULL,
    issue_status VARCHAR(2) NOT NULL,
    issue_resolution VARCHAR(400),
    resolution_dt DATE
);

CREATE TABLE llm_response_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    user_message VARCHAR(400) NOT NULL,
    llm_response VARCHAR(1000) NOT NULL,
    llm_response_eval VARCHAR(1000) NOT NULL,
    create_dt DATE NOT NULL
);

commit;