# Author : Charlie Newell
# Date   : 08/03/2017
""" This file contains the functions for scrapping one page of data from sports-reference.com """

# urllib2 is used to fetch the url
import urllib2

# BeautifulSoup is the module used to scrape the data from the html
from bs4 import BeautifulSoup

def getPage(url, teams):

    # concat sports-reference.com with game url
    gameUrl = "https://www.sports-reference.com" + url
    
    # open gameUrl
    gamePage = urllib2.urlopen(gameUrl)
    
    # Parse html store in gameHtml variable
    gameHtml = BeautifulSoup(gamePage, "html.parser")

    # get strings that will be used to access data tables
    winner, loser = convertStrings(teams)

    # Get data for each team
    winnerData = getData(gameHtml, winner)
    loserData  = getData(gameHtml, loser)
 
    if winnerData["Success"] == True and loserData["Success"] == True:
        print winnerData, loserData
        return winnerData, loserData

    else:
    	print "One of the team's data could not be accessed!"
    	return winnerData, loserData


def convertStrings(teams):
    """ This function converts the strings passed to the getPage function into strings that
	    sports-reference.com uses to store data tables
	"""

    # unpack tuple
    winner = teams[0]
    loser  = teams[1]

    # turn all strings to lower case
    winner = winner.lower().replace(' ', '-').replace('.','').replace('(','').replace(')','').replace(' & ', '-')
    loser  = loser.lower().replace(' ', '-').replace('.','').replace('(','').replace(')','').replace(' & ', '-')

    # Some Schools don't have links; hack there box-score names below
    if winner == "thomas-university":
        winner = "thomas-ga"
    elif loser == "thomas-university":
        loser = "thomas-ga"

    if winner == "bristol-university":
        winner = "bristol"
    elif loser == "bristol-university":
    	loser = "bristol"

    #print winner
    return winner, loser

def getData(gameHtml, team):
    """ This function returns a dictionary of data for the team passed to it """

    # Parse html for teams basic data box
    try:

        #Get team names
        scoreBox      = gameHtml.find("div", {"class" : "scorebox"})
        
        # Get both team names
        teamNames      = scoreBox.findAll("strong")

        # Scrape team names
        firstTeamName = teamNames[0].find("a").text
        secondTeamName = teamNames[1].find("a").text

        # Get both team scores
        teamScores = scoreBox.findAll("div", {"class" : "score"})
        
        # Scrape team scores
        firstTeamScore = teamScores[0].text
        secondTeamScore = teamScores[1].text
        
        # Get box score data for specefic team
        teamBox = gameHtml.find("table", {"id" : "box-score-basic-" + team})

        # Use tfoot to access summary row of data table
        summaryRow = teamBox.findAll("tfoot")

        # Get data in the tfoot row
        data = summaryRow[0].findAll("td")

        # Gather data
        FG     = data[1].find(text=True)
        FGA    = data[2].find(text=True)
        FGPer  = data[3].find(text=True)
        TP     = data[7].find(text=True)
        TPA    = data[8].find(text=True)
        TPPer  = data[9].find(text=True)
        FT     = data[10].find(text=True)
        FTA    = data[11].find(text=True)
        FTPer  = data[12].find(text=True)
        ORB    = data[13].find(text=True)
        TRB    = data[15].find(text=True)
        AST    = data[16].find(text=True)
        STL    = data[17].find(text=True)
        BLK    = data[18].find(text=True)
        TOV    = data[19].find(text=True)
        PF     = data[20].find(text=True)
        PTS    = data[21].find(text=True)

        # Turn data into dictionary
        teamData = { "FG"    : FG,
                     "FGA"   : FGA,
                      "FGPer" : FGPer,
                      "TP"    : TP,
                      "TPA"   : TPA,
                      "TPPer" : TPPer,
                      "FT"    : FT,
                      "FTA"   : FTA,
                      "FTPer" : FTPer,
                      "ORB"   : ORB,
                      "TRB"   : TRB,
                      "AST"   : AST,
                      "STL"   : STL,
                      "BLK"   : BLK,
                      "TOV"   : TOV,
                      "PF"    : PF,
                      "PTS"   : PTS,
                      "Success" : True }

        if firstTeamScore == PTS:
            teamData["Team"] = firstTeamName
        elif secondTeamScore == PTS:
            teamData["Team"] = secondTeamName

        return teamData

    # If box score is not accessed print team name that failed and set success to false
    except:
        teamData = { "Success" : False }  
        print team
        return teamData               
