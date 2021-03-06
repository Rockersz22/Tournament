#The purpose of this program is to give a basic UI to the Swiss Pairings tournament built for
#the Udacity Full Stack program
#WARNING: no safeguards are programmed, if incorrect ids are entered the database will store and
# return wrong information!!!

from tournament import *
latest=latestTournament()
print("\r\nWelcome to the command line for reporting tournament results and generating swiss pairings!\r\n")
input=""
while str(input) != "exit" and str(input) != "Exit":#main input loop
    input=raw_input("Enter command, or type help: ")
    if str(input)=="Archive" or str(input)=="archive":#run if statements against input
        viewArchive()#returns list of players, matches, and tournaments ordered by tournament id

    if str(input)=="new" or str(input)=="New":#run a new tournament
        name=raw_input("What is the name of your tournament? ")
        box=str(name)
        addTournament(box)
        updated=latestTournament()
        players=""
        while players !="exit" and players !="Exit":#loop while inserting new players
            players=raw_input("Enter player names one at a time and type exit when done: ")
            if players !="exit" and players !="Exit":
                registerPlayer(players,updated[0])
        
        running=""
        test=playerStandings()
        while test[0][2]==test[1][2]:#continue pairings as long as there is not a definite winner
            box=swissPairings()
            print("These are your generated matches:")
            for x in box:
                print x
            count=0
            while count<len(box):
                running=raw_input("Enter winner id's one at a time: ")
                winner=""
                loser=""
                for x in box:
                    if x[0]==int(running):#loop through pairings to match against user input
                        winner=x[0]
                        loser=x[2]
                        reportMatch(winner,loser)
                        count=count + 1
                        print("Match Successfully reported")
                    elif x[2]==int(running):
                        winner=x[2]
                        loser=x[0]
                        reportMatch(winner,loser)
                        count=count+1
                        print("Match Successfully reported")
            test=playerStandings()
        print("\r\nThe winner of the tournament is "+test[0][1]+"!")
    if str(input)=="delete"or str(input)=="Delete":#DELETE EVERYTHING
        deleteTournaments()
        deleteMatches()
        deletePlayers()
        print("All players and tournaments successfully deleted!")
    if str(input)=="help" or str(input)=="Help":
        print("\r\n'archive'- will print out a table of previous tournament results")
        print("\r\n'delete' - will delete all previous matches, players, and tournaments from the database")
        print("\r\n'new' - will start the process of running a new tournament, the first round of matchings are randomly generated.  The proceeding rounds are based off swiss pairings.  WARNING: entering winning ids incorrectly/repeatedly will completely destroy the validity of the matching system!!")
   
        
