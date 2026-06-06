USE ticketDb;

CREATE TABLE tickets (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    issue_create_dt DATE NOT NULL,
    issue_desc VARCHAR(50) NOT NULL,
    issue_status VARCHAR(2) NOT NULL,
    issue_resolution VARCHAR(50),
    resolution_dt DATE
);

INSERT INTO tickets (id, username, issue_create_dt, issue_desc, issue_status)
VALUES (111, 'test', sysdate(), 'test', 'OP');

commit;