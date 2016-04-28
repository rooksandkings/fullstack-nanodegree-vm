#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys

def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM match_record")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM match_record")
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players;")    
    DB.close()
    return c.fetchone()[0]


def registerPlayer(input_name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      players(playerID serial, name varchar(40), primary key(playerID))
    """

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (input_name,))
    c.execute("INSERT INTO match_record (name, wins, matches) VALUES (%s, %s, %s)", (input_name, 0, 0))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT playerID, name, wins, matches FROM match_record ORDER BY wins DESC")
    DB.close()
    return c.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("UPDATE match_record SET (wins, matches) = (wins + 1, matches + 1) WHERE playerID = (%s)", (winner,))
    c.execute("UPDATE match_record SET matches = (matches + 1) WHERE playerID = (%s)", (loser,))
    DB.commit()
    DB.close()
 
 
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
    pairing_index = 0
    pairs = []
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
   
    c.execute("SELECT playerID from match_record")
    number_of_pairings = len(c.fetchall())/2

    while pairing_index < number_of_pairings:
        c.execute("SELECT playerID, name from match_record ORDER BY wins DESC LIMIT 2 OFFSET %s", (pairing_index * 2,))
        current_list = c.fetchall()
        new_tuple = current_list[0] + current_list[1]
        pairs.append(new_tuple)
        pairing_index = pairing_index + 1
    DB.close()
    return pairs
    