-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- To run tournament.sql in terminal, use the command >>\i tournament.sql

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

DROP TABLE IF EXISTS player, matches;

CREATE TABLE player (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
  );

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES player(id) ON DELETE CASCADE,
    loser INTEGER REFERENCES player(id) ON DELETE CASCADE
  );
