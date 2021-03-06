#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    
    return psycopg2.connect("dbname=tournament")

def latestTournament():    
    conn=connect()
    cur=conn.cursor()
    cur.execute('SELECT id FROM tournaments ORDER BY created DESC limit 1')
    results=cur.fetchone()
    if results is None:
        d="default"
        cur.execute('INSERT INTO tournaments("name") values(%s)',(d,))
        conn.commit()
        cur.execute('SELECT id FROM tournaments ORDER BY created DESC limit 1')
        results=cur.fetchone()
        conn.close()        
    return results

def addTournament(name):
    conn=connect()
    cur=conn.cursor()
    cur.execute('INSERT INTO tournaments("name") values(%s);',(name,))
    conn.commit()
    conn.close()  

def deleteTournaments():
    """Remove all the match records from the database."""
    conn=connect()
    cur=conn.cursor()
    cur.execute('DELETE FROM tournaments')
    conn.commit()
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    conn=connect()
    cur=conn.cursor()
    cur.execute('DELETE FROM matches')
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn=connect()
    cur=conn.cursor()
    cur.execute('DELETE FROM players')
    conn.commit()
    conn.close()

def countPlayers(t_id=-1):
    """Returns the number of players currently registered."""
    box=latestTournament()
    tourn_id=t_id
    if int(t_id)==-1:
        tourn_id=int(box[0])
    conn=connect()
    cur=conn.cursor()
    cur.execute('SELECT COUNT(id) FROM players WHERE t_id=%s',(tourn_id,))
    result=cur.fetchone()
    return result[0]
    

def registerPlayer(name,t_id=-1):#t_id is the tournament # the player is registered in
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    box=latestTournament()
    tourn_id=t_id
    if int(t_id)==-1:
        tourn_id=int(box[0])  
    conn=connect()
    cur=conn.cursor()
    cur.execute('INSERT INTO players("name","t_id") VALUES(%s,%s)',(name,tourn_id))
    conn.commit()

def playerStandings(t_id=-1,first=-1):#specify tournamend id if needed
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
    box=latestTournament()
    tourn_id=t_id
    if int(t_id)==-1:
        tourn_id=int(box[0])  
    conn=connect()
    cur=conn.cursor()
    """ This is a super complicated query so I'll make it a little more legible here:
       SELECT id, name,                                                          
      (SELECT COUNT(*) FROM matches WHERE matches.winner_id=players.id) AS wins, #count wins 
      (SELECT COUNT(*) FROM matches WHERE matches.winner_id=players.id 
      OR matches.loser_id=players.id) AS matches,                                #count total matches
      FROM players WHERE t_id=%s ORDER by wins DESC;
    """
    cur.execute('SELECT id, name, (SELECT COUNT(*) FROM matches WHERE matches.winner_id=players.id) AS wins, (SELECT COUNT(*) FROM matches WHERE matches.winner_id=players.id OR matches.loser_id=players.id) AS matches FROM players WHERE t_id=%s ORDER by wins DESC;',(tourn_id,) )
    if first != -1:
        cur.execute('SELECT id, name FROM players WHERE t_id=%s ORDER BY random()',(tourn_id,))
    results=cur.fetchall()
    return results
        

def reportMatch(winner, loser,t_id=-1):#t_id is the tournament match is reported to
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn=connect()
    cur=conn.cursor()
    if winner==0: #don't let a bye match be reported backwards
        box=winner
        winner=loser
        loser=box
    box=latestTournament()
    tourn_id=t_id
    if int(t_id)==-1:
        tourn_id=int(box[0])
    cur.execute('INSERT INTO matches("winner_id","loser_id","t_id") VALUES(%s,%s,%s)',(winner,loser,tourn_id))
    conn.commit()
 
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
    conn=connect()
    cur=conn.cursor()
    latest=latestTournament()
    cur.execute('SELECT count(*) FROM matches WHERE t_id=%s',(latest[0],))#checks if first round of tourn
    check=cur.fetchone()
    
    
    if check[0]==0:
        standings = playerStandings(-1,0) # if first round players are randomly selected
    else:
        standings = playerStandings(-1,-1)#else run "swiss pairings" query
      

    if len(standings)%2: #if there are an odd number of players, "0,Bye Match" will be added as a player
        box=0,'Bye Match'
        standings.append(box)
    ids=[(x[0]) for x in standings]
    names=[(x[1]) for x in standings]
    results=zip(ids[::2],names[::2],ids[1::2],names[1::2])
    conn.close()
    return results
    


def viewArchive():
    conn=connect()
    cur=conn.cursor()
    cur.execute('SELECT * FROM (SELECT DISTINCT ON (players.id) tournaments.id as "Tournament#", players.name, players.id as "Players id", (SELECT COUNT(*) FROM matches WHERE matches.winner_id=players.id) as wins from  tournaments left join players on tournaments.id=players.t_id left join matches on players.t_id=matches.t_id ORDER BY players.id) as tourney ORDER BY "Tournament#", wins DESC;')  #for every player in each tournament select id, name, and wins
    print("\r\nTournament records: \r\ntour#, name, p_id, wins\r\n")
    for x in cur:
        print(x)
    conn.close()
    
  








