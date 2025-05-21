INSERT INTO users (email, fullname, is_active, salt, hashed_password)
VALUES ('master@user.com', 'MasterUser', true, 'qwerty', 'password')
RETURNING id;
