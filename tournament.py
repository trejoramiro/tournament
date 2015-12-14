#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<connection failed. error found.>")



def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    query = "DELETE FROM player;"
    cursor.execute(query)

    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT COUNT(*) FROM player;"
    cursor.execute(query)
    num_of_players = cursor.fetchone()[0]


    db.commit()
    db.close()

    return num_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    query = "INSERT INTO player (name) VALUES (%s);"
    parameter = (bleach.clean(name),)
    cursor.execute(query, parameter)

    db.commit()
    db.close()


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
    db, cursor = connect()

    query = "SELECT t2.id, t2.name, t2.wins, t1.matches FROM (SELECT player.id, player.name, COUNT(matches.id) AS matches FROM player LEFT JOIN matches ON player.id = matches.winner OR player.id = matches.loser GROUP BY player.id) t1 LEFT JOIN (SELECT player.id, player.name, COUNT(matches.winner) AS wins FROM player LEFT JOIN matches ON player.id = matches.winner GROUP BY player.id) t2 ON t1.id = t2.id ORDER BY t2.wins DESC;"
    cursor.execute(query)
    data = cursor.fetchall()

    db.commit()
    db.close()
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    query = "INSERT INTO matches (winner, loser) VALUES (%s , %s);"
    pair = (winner, loser)
    cursor.execute(query, pair)

    db.commit()
    db.close()


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
    db, cursor = connect()

    query = "SELECT player.id, player.name, COUNT(matches.winner) AS wins FROM player LEFT JOIN matches ON  player.id = matches.winner GROUP BY player.id ORDER BY wins DESC;"
    cursor.execute(query)
    data = cursor.fetchall()

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

    db.commit()
    db.close()

    return list_of_pairings
