-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players 
(
playerID serial, 
name varchar(40), 
PRIMARY KEY (playerID)
); 

CREATE TABLE match_record 
(
playerID integer REFERENCES players(playerID) PRIMARY KEY,
wins integer, 
matches integer
);