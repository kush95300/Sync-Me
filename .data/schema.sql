-- Create Table and db
CREATE TABLE if not EXISTS users (username, password, default_access_key, default_secret_key);

-- Create User
INSERT INTO users (username, password) VALUES ("admin","user");

-- List users
SELECT * FROM users;

-- Delete Row
DELETE FROM users WHERE username = "admin";