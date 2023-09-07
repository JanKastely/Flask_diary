DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL);

CREATE TABLE post(
id INTEGER PRIMARY KEY AUTOINCREMENT,
author_id INTEGER NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
title TEXT NOT NULL,
body TEXT NOT NULL,
likes INTEGER DEFAULT 0,
FOREIGN KEY (author_id) REFERENCES user(id));

CREATE TABLE likes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
post_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (post_id) REFERENCES post(id),
FOREIGN KEY (user_id) REFERENCES user(id));

CREATE TABLE user_likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    UNIQUE (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (post_id) REFERENCES post(id)
);
