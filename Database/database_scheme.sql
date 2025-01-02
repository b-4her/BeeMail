CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    email TEXT PRIMARY KEY  NOT NULL,
    hash TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS email ON users(email);

CREATE TABLE IF NOT EXISTS message_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status INTEGER DEFAULT 0 NOT NULL,
    type TEXT NOT NULL
);

-- Notes: 
-- -> The status refers to the message being viewed by the recipient (1 when viewed and 0 -default- when not)
-- -> Message type can be either primary or reply (The message type depends on the sender)


CREATE UNIQUE INDEX IF NOT EXISTS date_time_content_subject on message_details(subject, content, date, time);

-- Note: this unique index is created to get error when two identical emails are sent at the same second. 
-- Using try except we are able to catch it. That is important to do since we don't have any way to 
-- identify who sent which email of these identical emails.


CREATE TABLE IF NOT EXISTS user_messages (
    sender_email TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    message_id INTEGER NOT NULL,
    FOREIGN KEY(sender_email) REFERENCES users(email),
    FOREIGN KEY(recipient_email) REFERENCES users(email),
    FOREIGN KEY(message_id) REFERENCES message_details(id)
);

CREATE TABLE IF NOT EXISTS responses (
    parent_id INTEGER NOT NULL,
    response_id INTEGER NOT NULL,
    FOREIGN KEY(parent_id) REFERENCES message_details(id),
    FOREIGN KEY(response_id) REFERENCES message_details(id)
);


-- Indices to increase queries speed (The most searched data only, to avoid wasting much space):

-- # For login
CREATE INDEX IF NOT EXISTS hash_email on users(hash, email);  
CREATE INDEX IF NOT EXISTS emails on users(email); 

-- # Used each time when viewing an email
CREATE INDEX IF NOT EXISTS mails_relation on responses(parent_id, response_id); 

-- # Used everytime a user sends an email
CREATE INDEX IF NOT EXISTS mails_id on message_details(id, status, type);  
CREATE INDEX IF NOT EXISTS recipient_idx on user_messages(message_id, recipient_email); 