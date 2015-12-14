#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM player;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM player;")
    data_from_query = c.fetchall()
    num_of_players = int(data_from_query[0][0])
    conn.commit()
    conn.close()

    return num_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO player (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT t2.id, t2.name, t2.wins, t1.matches FROM (SELECT player.id, player.name, COUNT(matches.id) AS matches FROM player LEFT JOIN matches ON player.id = matches.winner OR player.id = matches.loser GROUP BY player.id) t1 LEFT JOIN (SELECT player.id, player.name, COUNT(matches.winner) AS wins FROM player LEFT JOIN matches ON player.id = matches.winner GROUP BY player.id) t2 ON t1.id = t2.id ORDER BY t2.wins DESC;")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s , %s);", (winner, loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT player.id, player.name, COUNT(matches.winner) AS wins FROM player LEFT JOIN matches ON  player.id = matches.winner GROUP BY player.id ORDER BY wins DESC;")
    data = c.fetchall()

    list_of_pairings = []
    counter = 0

    while counter < len(data):
        id1 = data[counter][0]
        name1 = data[counter][1]
        id2 = data[counter+1][0]
        name2 = data[counter+1][1]
        pair = (id1, name1, id2, name2)
        list_of_pairings.append(pair)
        counter = counter + 2

    conn.commit()
    conn.close()

    return list_of_pairings
