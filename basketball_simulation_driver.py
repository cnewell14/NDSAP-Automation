# Author : Charlie Newell
# Date   : 08/02/2017
""" The purpose of this file is to drive the data scrapping process for the NDSAP college
    basketball simulation. 
"""

import sys

# urllib2 used to fetch URL
import urllib2

# BeautifulSoup used to scrap data from html
from bs4 import BeautifulSoup

# Import game scraping functions
from scrape_one_page_class import getPage

# Import excel placing functions
from place_game_data_class import placeData
from place_game_data_class import openBook

# Import openpyxl to find max row of excel doc
import openpyxl

# Import writing to spreadsheet functions
from write_to_excel import writeSheet


class Driver:
    """This class will initiate the data scrape and placement process"""

    def __init__(self):
        self.url      = "https://www.sports-reference.com/cbb/boxscores/index.cgi?month=11&day=11&year=2016"
        self.mainPage = urllib2.urlopen(self.url)
        self.soup     = BeautifulSoup(self.mainPage, "html.parser")

    def Go(self):
        """ Driver function that gathers list of games, sends them to data scraping class
            then calls the class that stores the data in excel document 
        """

        # Open workbooks and get maxRow
        wb, ws, maxRow = openBook('test.xlsx', 'Sheet1')

        # Call function that returns list of tuples, one for each game
        gameTuplesList, gameLinksList = self.getGames(self.soup)

        # Save data into a list first
        gameDataList = []

        if len(gameLinksList) == len(gameTuplesList):
            for i in range(0, len(gameLinksList)):

                # Add winner&loser data to list
                winnerData, loserData = getPage(gameLinksList[i], gameTuplesList[i])

                # Update from Andy
                # gameDataList.append((winnerData, loserData))
                
                if winnerData["Success"] == False or loserData["Success"] == False:
                    sys.exit("Team data could not be accessed! Exiting!")
                else:
                    placeData(wb, ws, winnerData, loserData, maxRow+1)
                    maxRow += 1
                
                # maybe add to list then go through list placing data
                # put function call to place data into excel document here
            # Call function to write results to excel document

            #Update from Andy
            # writeSheet(gameDataList)

        else:
            print "Lists are not the same size!"


    def getGames(self, html):
        """ Parse html page and return a list of tuples (winner, loser) """

        gameTuplesList = []
        gameLinksList  = []

        # store html of table of games in gameList
        gameList  = html.findAll("div", {"class" : "game_summary nohover"})
        
        # loop through each game and parse winner and loser
        for game in gameList:

            # Get game link
            linkRow = game.find("td", {"class" : "right gamelink"})
            link    = linkRow.find("a")["href"]

        	# Get the losing team name
            loserRow  = game.findAll("tr", {"class" : "loser"})
            loserLink = loserRow[0].find("td")
            
            # Find link to team page, split to get team name used by sports-reference.com
            try:
                loser = loserLink.find("a")["href"]
                loser = loser.split("/")[3]

            # If team does not have link to team page take text    
            except:
                loser = loserLink.find(text=True)
            

            # Get the winning team name
            winnerRow  = game.findAll("tr", {"class" : "winner"})
            winnerLink = winnerRow[0].find("td")

            # Find link to team page, split to get team name used by sports-reference.com
            try:
                winner = winnerLink.find("a")["href"]
                winner = winner.split("/")[3]

            # If team does not have link to team page take text
            except:
            	winner = winnerLink.find(text=True)
            

            # Append data to lists
            gameTuplesList.append((winner, loser))
            gameLinksList.append(link)

        # return gameListTuples
        return gameTuplesList, gameLinksList   

if __name__ == "__main__":
    drive = Driver()
    drive.Go()