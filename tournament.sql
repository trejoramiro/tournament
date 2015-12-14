-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- To run tournament.sql in terminal, use the command >>\i tournament.sql


CREATEDB tournament;
\c tournament

DROP TABLE IF EXISTS player, matches;

CREATE TABLE player (
    id serial primary key,
    name text,
  );

CREATE TABLE matches (
    id serial primary key,
    winner integer references player(id),
    loser integer references player(id)
  );
