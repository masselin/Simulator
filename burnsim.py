from operator import attrgetter
import operator
import random
from time import ctime
import copy
import sqlite3
import math

class Simulator(object):
    """Simulator object, contains information on the game"""
    def __init__(self):
        """Simulator constructor.  Contains game specific information"""
        #Number of games to run per deck
        self.simulationLength = 1000
        #Current turn of the game
        self.turn = 0
        #True/false if P1 goes first
        self.goFirst = 1
        #Number of Lavamancer activations in a turn
        self.lavaAct = 0
        #Deck ID default value for database
        self.deckID = 0
        #True/False toggle to print game info to console
        self.debugmsg = 0
        #Turn on hand logging (very slow)
        self.draw = 0
        #Sets who goes first
        if self.goFirst == 1:
            self.curPlayer = P1()
            self.nAP = P2()
            self.activePlayer = self.curPlayer.deckName
        if self.goFirst != 1:
            self.curPlayer = P2()
            self.nAP = P1()
            self.activePlayer = self.curPlayer.deckName

    def switchPlayers(self):
        """Switch active/non active players"""
        temp = self.curPlayer
        self.curPlayer = self.nAP
        self.nAP = temp
        self.activePlayer = self.curPlayer.deckName
        msg = "Active player is " + self.curPlayer.deckName
        self.debug(msg)

    def setParams(self):
        """Main loop"""
        self.buildDB()
        self.playGames()
        #Quick and dirty way to que several decks to be played in a batch
###17 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 17
##        sim.curPlayer.ringCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 4
##        sim.curPlayer.guideCount = 4
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 2
##        sim.curPlayer.riftCount = 7
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 12
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 0
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()
###18 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 18
##        sim.curPlayer.ringCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 4
##        sim.curPlayer.guideCount = 4
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 2
##        sim.curPlayer.riftCount = 7
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 11
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 0
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()
###19 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 19
##        sim.curPlayer.ringCount = 0
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 4
##        sim.curPlayer.guideCount = 4
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 11
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 1
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###20 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 20
##        sim.curPlayer.ringCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 3
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 10
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 3
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###21 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 21
##        sim.curPlayer.ringCount = 0
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 4
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 8
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 3
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###22 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 21
##        sim.curPlayer.ringCount = 1
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 3
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 7
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###23 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 21
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 3
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 6
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 0
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###24 Land
##        sim.curPlayer.fetchCount = 13
##        sim.curPlayer.landCount = 9
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 3
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 1
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
#24 Land
        sim.curPlayer.fetchCount = 11
        sim.curPlayer.landCount = 11
        sim.curPlayer.ringCount = 2
        sim.curPlayer.ForgottenCaveCount = 0
        sim.curPlayer.eidolonCount = 5
        sim.curPlayer.hellsparkCount = 0
        sim.curPlayer.swiftspearCount = 3
        sim.curPlayer.guideCount = 3
        sim.curPlayer.marauderCount = 0
        sim.curPlayer.vexingCount = 0
        sim.curPlayer.riftCount = 6
        sim.curPlayer.fireblastCount = 2
        sim.curPlayer.atarkaCount = 0
        sim.curPlayer.incinerateCount = 0
        sim.curPlayer.boltCount = 5
        sim.curPlayer.chainCount = 4
        sim.curPlayer.firecraftCount = 4
        sim.curPlayer.vortexCount = 1
        sim.curPlayer.lavamancerCount = 0
        sim.curPlayer.serumCount = 0
        sim.curPlayer.searingCount = 4
        self.playGames()
###24 Land
##        sim.curPlayer.fetchCount = 12
##        sim.curPlayer.landCount = 10
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 3
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 6
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 1
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 4
##        self.playGames()
###25 Land
##        sim.curPlayer.fetchCount = 11
##        sim.curPlayer.landCount = 12
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 2
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 3
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 1
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()
###25 Land
##        sim.curPlayer.fetchCount = 12
##        sim.curPlayer.landCount = 11
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 2
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 3
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 1
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()
###25 Land
##        sim.curPlayer.fetchCount = 13
##        sim.curPlayer.landCount = 10
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 0
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 3
##        sim.curPlayer.guideCount = 2
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 3
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 1
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()

###26 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 24
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.eidolonCount = 5
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 2
##        sim.curPlayer.guideCount = 2
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 3
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 3
##        self.playGames()
#27 Land
        sim.curPlayer.fetchCount = 0
        sim.curPlayer.landCount = 21
        sim.curPlayer.ringCount = 2
        sim.curPlayer.ForgottenCaveCount = 4
        sim.curPlayer.eidolonCount = 5
        sim.curPlayer.hellsparkCount = 0
        sim.curPlayer.swiftspearCount = 3
        sim.curPlayer.guideCount = 2
        sim.curPlayer.marauderCount = 0
        sim.curPlayer.vexingCount = 0
        sim.curPlayer.riftCount = 5
        sim.curPlayer.fireblastCount = 2
        sim.curPlayer.atarkaCount = 0
        sim.curPlayer.incinerateCount = 0
        sim.curPlayer.boltCount = 4
        sim.curPlayer.chainCount = 4
        sim.curPlayer.firecraftCount = 4
        sim.curPlayer.vortexCount = 1
        sim.curPlayer.lavamancerCount = 0
        sim.curPlayer.serumCount = 0
        sim.curPlayer.searingCount = 3
        self.playGames()
###28 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 22
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.ForgottenCaveCount = 4
##        sim.curPlayer.eidolonCount = 6
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 2
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 5
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 2
##        self.playGames()
###29 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 27
##        sim.curPlayer.ringCount = 2
##        sim.curPlayer.eidolonCount = 6
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 2
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 4
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 2
##        self.playGames()
###30 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 27
##        sim.curPlayer.ringCount = 3
##        sim.curPlayer.eidolonCount = 7
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 3
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 4
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 3
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 1
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 1
##        self.playGames()
###31 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 28
##        sim.curPlayer.ringCount = 3
##        sim.curPlayer.eidolonCount = 6
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 2
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 4
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 3
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 2
##        self.playGames()
###32 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 29
##        sim.curPlayer.ringCount = 3
##        sim.curPlayer.eidolonCount = 7
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 0
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 5
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 3
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 1
##        self.playGames()
###33 Land
##        sim.curPlayer.fetchCount = 0
##        sim.curPlayer.landCount = 30
##        sim.curPlayer.ringCount = 3
##        sim.curPlayer.eidolonCount = 8
##        sim.curPlayer.hellsparkCount = 0
##        sim.curPlayer.swiftspearCount = 0
##        sim.curPlayer.guideCount = 0
##        sim.curPlayer.marauderCount = 1
##        sim.curPlayer.vexingCount = 0
##        sim.curPlayer.riftCount = 4
##        sim.curPlayer.fireblastCount = 2
##        sim.curPlayer.atarkaCount = 0
##        sim.curPlayer.incinerateCount = 0
##        sim.curPlayer.boltCount = 4
##        sim.curPlayer.chainCount = 2
##        sim.curPlayer.firecraftCount = 4
##        sim.curPlayer.vortexCount = 2
##        sim.curPlayer.lavamancerCount = 0
##        sim.curPlayer.serumCount = 0
##        sim.curPlayer.searingCount = 0
##        self.playGames()

    def buildDB(self):
        """Builds the database"""
        self.debug("Begin building Database...")
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        #Build deck table, contains deck id and deck configuration
        self.debug("Building Deck table...")
        #c.execute('''DROP TABLE tableDeck''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableDeck
        (deckID INTEGER PRIMARY KEY AUTOINCREMENT,
        fetch INTEGER NOT NULL,
        land INTEGER NOT NULL,
        cave INTEGER NOT NULL,
        eidolon INTEGER NOT NULL,
        hellspark INTEGER NOT NULL,
        swiftspear INTEGER NOT NULL,
        guide INTEGER NOT NULL,
        marauder INTEGER NOT NULL,
        vexing INTEGER NOT NULL,
        rift INTEGER NOT NULL,
        fireblast INTEGER NOT NULL,
        atarka INTEGER NOT NULL,
        incinerate INTEGER NOT NULL,
        bolt INTEGER NOT NULL,
        jet INTEGER NOT NULL,
        top INTEGER NOT NULL,
        probe INTEGER NOT NULL,
        firecraft INTEGER NOT NULL,
        lavamancer INTEGER NOT NULL,
        ring INTEGER NOT NULL,
        vortex INTEGER NOT NULL,
        serum INTEGER NOT NULL,
        chain INTEGER NOT NULL,
        searingblaze INTEGER NOT NULL)''')
        conn.commit()
        conn.close()
        #Build games table, contains game info, associated deck
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Building Games table...")
        #c.execute('''DROP TABLE tableGames''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableGames
        (gameID INTEGER PRIMARY KEY AUTOINCREMENT,
        deckID INTEGER NOT NULL,
        mulligansTaken INTEGER,
        mulliganNoLand INTEGER,
        mulliganAllLand INTEGER,
        mulliganNoCreatures INTEGER,
        maxTurns INTEGER,
        FOREIGN KEY(deckID) REFERENCES tableDeck(deckID))''')
        conn.commit()
        conn.close()
        #Build turns table, links turn to game, records turn info
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Building Turns table...")
        #c.execute('''DROP TABLE tableTurns''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableTurns
        (turnID INTEGER PRIMARY KEY AUTOINCREMENT,
        gameID INTEGER NOT NULL,
        myLife INTEGER,
        opponentLife INTEGER,
        maxMana INTEGER,
        prowess INTEGER,
        turnNum INTEGER,
        lavaact INTEGER,
        opplife INTEGER,
        FOREIGN KEY(gameID) REFERENCES tableGames(gameID))''')
        conn.commit()
        conn.close()
        #Build hand table, links hand to turnID, contains hand info
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Building hand table...")
        #c.execute('''DROP TABLE tableHand''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableHand
        (handID INTEGER PRIMARY KEY AUTOINCREMENT,
        turnID INTEGER NOT NULL,
        fetch INTEGER NOT NULL,
        land INTEGER NOT NULL,
        cave INTEGER NOT NULL,
        eidolon INTEGER NOT NULL,
        hellspark INTEGER NOT NULL,
        swiftspear INTEGER NOT NULL,
        guide INTEGER NOT NULL,
        marauder INTEGER NOT NULL,
        vexing INTEGER NOT NULL,
        rift INTEGER NOT NULL,
        fireblast INTEGER NOT NULL,
        atarka INTEGER NOT NULL,
        incinerate INTEGER NOT NULL,
        bolt INTEGER NOT NULL,
        jet INTEGER NOT NULL,
        top INTEGER NOT NULL,
        probe INTEGER NOT NULL,
        firecraft INTEGER NOT NULL,
        lavamancer INTEGER NOT NULL,
        ring INTEGER NOT NULL,
        vortex INTEGER NOT NULL,
        serum INTEGER NOT NULL,
        chain INTEGER NOT NULL,
        searingblaze INTEGER NOT NULL,
        FOREIGN KEY(turnID) REFERENCES tableGames(turnID))''')
        conn.commit()
        conn.close()
        #Build board table, links board to turnID, contains board info
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Building board table")
        #c.execute('''DROP TABLE tableBoard''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableBoard
        (boardID INTEGER PRIMARY KEY AUTOINCREMENT,
        turnID INTEGER NOT NULL,
        fetch INTEGER NOT NULL,
        land INTEGER NOT NULL,
        cave INTEGER NOT NULL,
        eidolon INTEGER NOT NULL,
        hellspark INTEGER NOT NULL,
        swiftspear INTEGER NOT NULL,
        guide INTEGER NOT NULL,
        marauder INTEGER NOT NULL,
        vexing INTEGER NOT NULL,
        rift INTEGER NOT NULL,
        fireblast INTEGER NOT NULL,
        atarka INTEGER NOT NULL,
        incinerate INTEGER NOT NULL,
        bolt INTEGER NOT NULL,
        jet INTEGER NOT NULL,
        top INTEGER NOT NULL,
        probe INTEGER NOT NULL,
        firecraft INTEGER NOT NULL,
        lavamancer INTEGER NOT NULL,
        ring INTEGER NOT NULL,
        vortex INTEGER NOT NULL,
        serum INTEGER NOT NULL,
        chain INTEGER NOT NULL,
        searingblaze INTEGER NOT NULL,
        FOREIGN KEY(turnID) REFERENCES tableGames(turnID))''')
        conn.commit()
        conn.close()
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Building draw table...")
        #c.execute('''DROP TABLE tableDraw''')
        c.execute('''CREATE TABLE IF NOT EXISTS tableDraw
        (thingID INTEGER PRIMARY KEY AUTOINCREMENT,
        gameID INTEGER NOT NULL,
        fetch INTEGER NOT NULL,
        land INTEGER NOT NULL,
        cave INTEGER NOT NULL,
        eidolon INTEGER NOT NULL,
        hellspark INTEGER NOT NULL,
        swiftspear INTEGER NOT NULL,
        guide INTEGER NOT NULL,
        marauder INTEGER NOT NULL,
        vexing INTEGER NOT NULL,
        rift INTEGER NOT NULL,
        fireblast INTEGER NOT NULL,
        atarka INTEGER NOT NULL,
        incinerate INTEGER NOT NULL,
        bolt INTEGER NOT NULL,
        jet INTEGER NOT NULL,
        top INTEGER NOT NULL,
        probe INTEGER NOT NULL,
        firecraft INTEGER NOT NULL,
        lavamancer INTEGER NOT NULL,
        ring INTEGER NOT NULL,
        vortex INTEGER NOT NULL,
        serum INTEGER NOT NULL,
        chain INTEGER NOT NULL,
        searingblaze INTEGER NOT NULL,
        FOREIGN KEY(gameID) REFERENCES tableGames(turnID))''')
        self.debug("Database built")

    def recordDeck(self):
        """Records deck information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        #Query for deck config
        self.debug("Recording deck configuration")
        cardcount = [(sim.curPlayer.fetchCount, sim.curPlayer.landCount, sim.curPlayer.ForgottenCaveCount, sim.curPlayer.eidolonCount, sim.curPlayer.hellsparkCount, sim.curPlayer.swiftspearCount, sim.curPlayer.guideCount, sim.curPlayer.marauderCount, sim.curPlayer.vexingCount, sim.curPlayer.riftCount, sim.curPlayer.fireblastCount, sim.curPlayer.atarkaCount, sim.curPlayer.incinerateCount, sim.curPlayer.boltCount, sim.curPlayer.jetCount, sim.curPlayer.topCount, sim.curPlayer.probeCount, sim.curPlayer.firecraftCount, sim.curPlayer.lavamancerCount, sim.curPlayer.ringCount, sim.curPlayer.vortexCount, sim.curPlayer.serumCount, sim.curPlayer.chainCount, sim.curPlayer.searingCount)]
        c.executemany('INSERT INTO tableDeck VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', cardcount)
        cursor = c.execute('SELECT max(deckID) FROM tableDeck')
        self.deckID = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    def recordDraw(self):
        """Records draw information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Recording draw")
        game = self.getGameId()
        self.fetchDraw = self.cardsin(Fetch, sim.curPlayer.myDraw)
        self.landDraw = self.cardsin(Land, sim.curPlayer.myDraw)
        self.eidolonDraw = self.cardsin(Eidolon, sim.curPlayer.myDraw)
        self.hellsparkDraw = self.cardsin(Hellspark, sim.curPlayer.myDraw)
        self.swiftspearDraw = self.cardsin(Swiftspear, sim.curPlayer.myDraw)
        self.guideDraw = self.cardsin(Guide, sim.curPlayer.myDraw)
        self.marauderDraw = self.cardsin(Marauder, sim.curPlayer.myDraw)
        self.vexingDraw = self.cardsin(Vexing, sim.curPlayer.myDraw)
        self.riftDraw = self.cardsin(Rift, sim.curPlayer.myDraw)
        self.fireblastDraw = self.cardsin(Fireblast, sim.curPlayer.myDraw)
        self.atarkaDraw = self.cardsin(Atarka, sim.curPlayer.myDraw)
        self.incinerateDraw = self.cardsin(Incinerate, sim.curPlayer.myDraw)
        self.boltDraw = self.cardsin(Bolt, sim.curPlayer.myDraw)
        self.jetDraw = self.cardsin(Jet, sim.curPlayer.myDraw)
        self.topDraw = self.cardsin(Top, sim.curPlayer.myDraw)
        self.probeDraw = self.cardsin(Probe, sim.curPlayer.myDraw)
        self.firecraftDraw = self.cardsin(Firecraft, sim.curPlayer.myDraw)
        self.vortexDraw = self.cardsin(Vortex, sim.curPlayer.myDraw)
        self.lavamancerDraw = self.cardsin(Lavamancer, sim.curPlayer.myDraw)
        self.ringDraw = self.cardsin(Ring, sim.curPlayer.myDraw)
        self.serumDraw = self.cardsin(Serum, sim.curPlayer.myDraw)
        self.chainDraw = self.cardsin(Chain, sim.curPlayer.myDraw)
        self.searingDraw = self.cardsin(SearingBlaze, sim.curPlayer.myDraw)
        self.caveDraw = self.cardsin(ForgottenCave, sim.curPlayer.myDraw)
        drawinfo = [(self.gameID, self.fetchDraw, self.landDraw, self.caveDraw, self.eidolonDraw, self.hellsparkDraw, self.swiftspearDraw, self.guideDraw, self.marauderDraw, self.vexingDraw, self.riftDraw, self.fireblastDraw, self.atarkaDraw, self.incinerateDraw, self.boltDraw, self.jetDraw, self.topDraw, self.probeDraw, self.firecraftDraw, self.lavamancerDraw, self.ringDraw, self.vortexDraw, self.serumDraw, self.chainDraw, self.searingDraw)]
        c.executemany('INSERT INTO tableDraw VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', drawinfo)
        conn.commit()
        conn.close()

    def recordGame(self):
        """Records game information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Recording game configuration")
        params = [(self.deckID, sim.curPlayer.mulligansTaken, sim.curPlayer.mulliganNoLand, sim.curPlayer.mulliganAllLand, sim.curPlayer.mulliganNoCreatures, math.floor(self.turn))]
        deck = [(self.deckID)]
        c.executemany('INSERT INTO tableGames VALUES (NULL, ?, ?, ?, ?, ?, ?)', params)
        cursor = c.execute('SELECT max(gameID) FROM tableGames WHERE deckID = ?', (deck))
        self.gameID = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    def recordTurn(self):
        """Records turn information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Recording turn configuration")
        game = [(self.gameID)]
        params = [(self.gameID, sim.curPlayer.life, sim.nAP.life, sim.curPlayer.maxMana, sim.curPlayer.prowess, self.turn, sim.curPlayer.lavaAct, sim.nAP.life)]
        c.executemany('INSERT INTO tableTurns VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', params)
        cursor = c.execute('SELECT max(turnID) FROM tableTurns WHERE gameID = ?', (game))
        self.turnID = cursor.fetchone()[0]
        self.debug("Updating max turns")
        c.execute('UPDATE tableGames SET maxTurns = ? WHERE gameID=?', [self.turn, self.gameID])
        conn.commit()
        conn.close()
        if self.curPlayer.deckName == "Burn":
            self.recordBoard()

    def recordHand(self):
        """Records hand information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Recording hand configuration")
        self.fetchHand = self.cardsin(Fetch, sim.curPlayer.myHand)
        self.landHand = self.cardsin(Land, sim.curPlayer.myHand)
        self.eidolonHand = self.cardsin(Eidolon, sim.curPlayer.myHand)
        self.hellsparkHand = self.cardsin(Hellspark, sim.curPlayer.myHand)
        self.swiftspearHand = self.cardsin(Swiftspear, sim.curPlayer.myHand)
        self.guideHand = self.cardsin(Guide, sim.curPlayer.myHand)
        self.marauderHand = self.cardsin(Marauder, sim.curPlayer.myHand)
        self.vexingHand = self.cardsin(Vexing, sim.curPlayer.myHand)
        self.riftHand = self.cardsin(Rift, sim.curPlayer.myHand)
        self.fireblastHand = self.cardsin(Fireblast, sim.curPlayer.myHand)
        self.atarkaHand = self.cardsin(Atarka, sim.curPlayer.myHand)
        self.incinerateHand = self.cardsin(Incinerate, sim.curPlayer.myHand)
        self.boltHand = self.cardsin(Bolt, sim.curPlayer.myHand)
        self.jetHand = self.cardsin(Jet, sim.curPlayer.myHand)
        self.topHand = self.cardsin(Top, sim.curPlayer.myHand)
        self.probeHand = self.cardsin(Probe, sim.curPlayer.myHand)
        self.firecraftHand = self.cardsin(Firecraft, sim.curPlayer.myHand)
        self.vortexHand = self.cardsin(Vortex, sim.curPlayer.myHand)
        self.lavamancerHand = self.cardsin(Lavamancer, sim.curPlayer.myHand)
        self.ringHand = self.cardsin(Ring, sim.curPlayer.myHand)
        self.serumHand = self.cardsin(Serum, sim.curPlayer.myHand)
        self.chainHand = self.cardsin(Chain, sim.curPlayer.myHand)
        self.searingHand = self.cardsin(SearingBlaze, sim.curPlayer.myHand)
        self.caveHand = self.cardsin(ForgottenCave, sim.curPlayer.myHand)
        self.getTurnId()
        handinfo = [(self.turnID, self.fetchHand, self.landHand, self.caveHand, self.eidolonHand, self.hellsparkHand, self.swiftspearHand, self.guideHand, self.marauderHand, self.vexingHand, self.riftHand, self.fireblastHand, self.atarkaHand, self.incinerateHand, self.boltHand, self.jetHand, self.topHand, self.probeHand, self.firecraftHand, self.lavamancerHand, self.ringHand, self.vortexHand, self.serumHand, self.chainHand, self.searingHand)]
        turn = [(self.turnID)]
        c.executemany('INSERT INTO tableHand VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', handinfo)
        cursor = c.execute('SELECT max(handID) FROM tableHand WHERE turnID = ?', (turn))
        self.handID = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    def recordBoard(self):
        """Records board information"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        self.debug("Recording board configuration")
        self.fetchBoard = self.cardsin(Fetch, sim.curPlayer.myBoard)
        self.landBoard = self.cardsin(Land, sim.curPlayer.myBoard)
        self.eidolonBoard = self.cardsin(Eidolon, sim.curPlayer.myBoard)
        self.hellsparkBoard = self.cardsin(Hellspark, sim.curPlayer.myBoard)
        self.swiftspearBoard = self.cardsin(Swiftspear, sim.curPlayer.myBoard)
        self.guideBoard = self.cardsin(Guide, sim.curPlayer.myBoard)
        self.marauderBoard = self.cardsin(Marauder, sim.curPlayer.myBoard)
        self.vexingBoard = self.cardsin(Vexing, sim.curPlayer.myBoard)
        self.riftBoard = self.cardsin(Rift, sim.curPlayer.myBoard)
        self.fireblastBoard = self.cardsin(Fireblast, sim.curPlayer.myBoard)
        self.atarkaBoard = self.cardsin(Atarka, sim.curPlayer.myBoard)
        self.incinerateBoard = self.cardsin(Incinerate, sim.curPlayer.myBoard)
        self.boltBoard = self.cardsin(Bolt, sim.curPlayer.myBoard)
        self.jetBoard = self.cardsin(Jet, sim.curPlayer.myBoard)
        self.topBoard = self.cardsin(Top, sim.curPlayer.myBoard)
        self.probeBoard = self.cardsin(Probe, sim.curPlayer.myBoard)
        self.firecraftBoard = self.cardsin(Firecraft, sim.curPlayer.myBoard)
        self.vortexBoard = self.cardsin(Vortex, sim.curPlayer.myBoard)
        self.lavamancerBoard = self.cardsin(Lavamancer, sim.curPlayer.myBoard)
        self.ringBoard = self.cardsin(Ring, sim.curPlayer.myBoard)
        self.serumBoard = self.cardsin(Serum, sim.curPlayer.myBoard)
        self.chainBoard = self.cardsin(Chain, sim.curPlayer.myBoard)
        self.searingBoard = self.cardsin(SearingBlaze, sim.curPlayer.myBoard)
        self.caveBoard = self.cardsin(ForgottenCave, sim.curPlayer.myBoard)
        boardinfo = [(self.turnID, self.fetchBoard, self.landBoard, self.caveBoard, self.eidolonBoard, self.hellsparkBoard, self.swiftspearBoard, self.guideBoard, self.marauderBoard, self.vexingBoard, self.riftBoard, self.fireblastBoard, self.atarkaBoard, self.incinerateBoard, self.boltBoard, self.jetBoard, self.topBoard, self.probeBoard, self.firecraftBoard, self.lavamancerBoard, self.ringBoard, self.vortexBoard, self.serumBoard, self.chainBoard, self.searingBoard)]
        turn = [(self.turnID)]
        c.executemany('INSERT INTO tableBoard VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', boardinfo)
        cursor = c.execute('SELECT max(boardID) FROM tableBoard WHERE turnID = ?', (turn))
        self.boardID = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    def getTurnId(self):
        """Gets self.turnID"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        cursor = c.execute('SELECT max(turnID) FROM tableTurns')
        self.turnID = cursor.fetchone()[0]
        if self.turnID == None:
            self.turnID = 0
        return

    def getGameId(self):
        """Gets self.gameID"""
        conn = sqlite3.connect('burn.db')
        c = conn.cursor()
        cursor = c.execute('SELECT max(gameID) FROM tableGames')
        self.gameID = cursor.fetchone()[0]
        if self.gameID == None:
            self.gameID = 0
        return

    def cardsin(self, card, zone):
        """Takes card class and zone, returns number of that class instance in zone"""
        count = sum(isinstance(x, card) for x in zone)
        return count

    def getPlayer(self):
        """Gets current player"""
        return self.curPlayer

    def debug(self, message):
        """Prints debug messages to console if enabled"""
        if (self.debugmsg == 1):
            print(message)

    def blast(self):
        """Checks for number of alt cast Fireblast available"""
        self.debug("Evaluating Fireblast")
        castBlast = min(self.cardsin(Fireblast, sim.curPlayer.myHand), (self.cardsin(Land, sim.curPlayer.myBoard)//2))
        castBlast = castBlast * Fireblast().getDamage()
        return castBlast

    def reset(self):
        """Resets game variables"""
##        if self.goFirst == 1:
##            self.curPlayer = P1()
##            self.nAP = P2()
##            self.activePlayer = self.curPlayer.deckName
##        if self.goFirst != 1:
##            self.curPlayer = P2()
##            self.nAP = P1()
##            self.activePlayer = self.curPlayer.deckName
        self.curPlayer.myHand = []
        self.curPlayer.myBoard = []
        self.curPlayer.myGrave = []
        self.curPlayer.myStack = []
        self.nAP.myHand = []
        self.nAP.myBoard = []
        self.nAP.myGrave = []
        self.nAP.myStack = []
        sim.curPlayer.life = 20
        sim.nAP.life = 20
        self.turn = 0
        self.curPlayer.openingHand = 7
        self.nAP.openingHand = 7

    def untapPhase(self):
        """Untap phase"""
        self.debug("Turn " + str(math.floor(self.turn)) + " begins for " + str(self.curPlayer.deckName))
        self.debug("Untap Phase")
        for card in self.curPlayer.myBoard:
            if card.sick > 0:
                card.sick -= 1
            card.untap()
        self.curPlayer.prowess = 0
        self.nAP.prowess = 0
        self.lavaAct = 0
        self.topUsed = 0

    def upkeepPhase(self):
        """Upkeep phase"""
        self.debug("Upkeep Phase")
        for card in self.curPlayer.myHand:
            card.upkeepTrigger()
        self.curPlayer.resolveStack()

    def drawPhase(self):
        """Draw phase"""
        if self.turn > 1 or self.goFirst == 0:
            self.curPlayer.drawCard()
            self.debug("New hand is" + str(self.curPlayer.myHand))
        self.curPlayer.resolveStack()
        if self.curPlayer.deckName == "Burn":
            self.recordHand()

    def mainOnePhase(self):
        """Main one phase"""
        #Play land and crack fetch
        self.curPlayer.playLand()
        self.curPlayer.useFetch()
        #Determine available mana for the turn
        self.curPlayer.availableMana = 0
        for card in self.curPlayer.myBoard:
            if card.type == "Land" and card.name != "Fetch" and card.tapped == 0:
                self.curPlayer.availableMana += 1
        message = "Mana is " + str(self.curPlayer.getMana())
        self.debug(message)
        self.curPlayer.maxMana = self.curPlayer.availableMana
        self.debug("New board is")
        #Find burn in hand
        self.debug(self.curPlayer.myBoard)
        burn = self.curPlayer.getBurn()
        #Loop until there are no plays to make
        noPlay = False
        while(noPlay == False):
            noPlay = True
            #Create list of most to least favorable plays
            self.curPlayer.getPlays()
            for card in self.curPlayer.myHand:
                #Cycle cards
                if card.mana <= self.curPlayer.availableMana and card.cycling == 1:
                    self.debug("Cycling cards")
                    card.cycle()
                    self.noPlay = False
                #Play cards in order
                if card.mana <= self.curPlayer.availableMana and card.type != "Land":
                    self.debug("Attempting to play cards")
                    card.play()
                    self.noPlay = False
        self.curPlayer.resolveStack()

    def combatPhase(self):
        """Combat phase"""
        sim.debug("Beginning combat...")
        self.curPlayer.declareAttacks()
        self.nAP.declareBlocks()
        self.dealDamage()
        #Lavamancer extra damage
        temp = min(len(sim.curPlayer.myGrave)//2, sim.cardsin(Lavamancer, sim.curPlayer.myBoard), sim.curPlayer.availableMana)
        for x in range(0, temp):
            sim.curPlayer.myGrave.pop()
            sim.curPlayer.myGrave.pop()
            sim.curPlayer.availableMana -= 1
            sim.nAP.life -= 1
            sim.curPlayer.lavaAct += 1
        sim.debug("Combat finished, opponent at " + str(sim.nAP.life))
        self.curPlayer.resolveStack()

    def dealDamage(self):
        """Exchange damage in combat"""
        sim.debug("Exchanging Damage")
    #Deal Damage
        for card in sim.curPlayer.blockedAttackers:
            card.damageTaken += card.blockedBy.damage
        for card in sim.nAP.blockers:
            card.damageTaken += card.blocking.damage
        for card in sim.curPlayer.unblockedAttackers:
            msg = str(card) + " was unblocked for " + str(card.damage) + " damage"
            sim.debug(msg)
            sim.nAP.life -= card.damage
    #Consolidate combat zones to myBoard
        for card in sim.nAP.potentialBlockers:
            sim.nAP.myBoard.append(card)
        sim.curPlayer.myBoard = []
        for card in sim.curPlayer.unblockedAttackers:
            sim.curPlayer.myBoard.append(card)
        for card in sim.curPlayer.blockedAttackers:
            sim.curPlayer.myBoard.append(card)
        for card in sim.curPlayer.otherPermanents:
            sim.curPlayer.myBoard.append(card)
    #Kill things
        for card in sim.curPlayer.myBoard:
            if card.type == "Creature" and card.damageTaken > card.toughness:
                card.damageTaken = 0
                card.die()
        for card in sim.nAP.myBoard:
            if card.type == "Creature" and card.damageTaken > card.toughness:
                card.damageTaken = 0
                card.die()

    def mainTwoPhase(self):
        """Main two phase"""
        x = self.blast()
        if (x >= sim.nAP.life and sim.curPlayer.life > 0):
            y = x//4
            for z in range(0, y + 1):
                noPlay = False
                Fireblast.play(self)
        self.curPlayer.resolveStack()

    def endPhase(self):
        """End of turn phase"""
        sim.nAP.life -= self.cardsin(Eidolon, self.curPlayer.myBoard) * 2
        sim.debug(str(self.curPlayer) + " turn ends at " + str(sim.curPlayer.life) + ".  " + str(sim.nAP) + " at " + str(sim.nAP.life))
        self.curPlayer.resolveStack()
        for card in sim.curPlayer.myBoard:
            if card.type == "Creature":
                card.damageTaken = 0
                card.damage -= sim.curPlayer.prowess * card.prowess
                card.toughness -= sim.curPlayer.prowess * card.prowess
        for card in sim.nAP.myBoard:
            if card.type == "Creature":
                card.damageTaken = 0
                card.damage -= sim.nAP.prowess * card.prowess
                card.toughness -= sim.nAP.prowess * card.prowess
        if self.curPlayer.deckName == "Burn":
            self.recordTurn()
        sim.curPlayer.prowess = 0
        sim.nAP.prowess = 0


    def preGame(self):
        """Pregame, shuffle, reset deck, mulligan"""
        self.reset()
        sim.curPlayer.buildDeck()
        sim.nAP.buildDeck()
        self.curPlayer.resolveMulligans()
        self.nAP.resolveMulligans()
        if (len(self.curPlayer.myHand) < 7):
            self.debug("Taking mulligan scry")
            self.curPlayer.scry(1)
        if (len(self.nAP.myHand) < 7):
            self.debug("Taking mulligan scry")
            self.nAP.scry(1)

    def playGames(self):
        """Main games loop"""
        if self.curPlayer.deckName == "Burn":
            self.recordDeck()
        self.debug("Playing games")
        games = 0
        for games in range(0, self.simulationLength):

            self.debug("Game " + str(games) + " begins")
            self.preGame()
            if self.curPlayer.deckName == "Burn":
                self.recordGame()
            self.debug("Reseting deck variables")
#Keep decision made, begin playing
            while sim.nAP.life > 0 and sim.curPlayer.life > 0:
                self.turn += 1
                self.untapPhase()
                self.upkeepPhase()
                self.drawPhase()
                self.mainOnePhase()
                self.combatPhase()
                self.mainTwoPhase()
                self.endPhase()
                self.switchPlayers()
#Repeat because turns are dumb
                self.untapPhase()
                self.upkeepPhase()
                self.drawPhase()
                self.mainOnePhase()
                self.combatPhase()
                self.mainTwoPhase()
                self.endPhase()
                self.switchPlayers()

class Card:
    """Card class, constains generalized card functions and lots of card variables"""
    def __init__(self):
        self.type = "Land"
        self.damage = 0
        self.toughness = 0
        self.mana = 0
        self.sick = 1
        self.name = "Wastes"
        self.targets = 0
        self.cardsDrawn = 0
        self.tapped = 0
        self.vanishing = 0
        self.shouldAttack = 0
        self.shouldBlock = 0
        self.blocking = None
        self.blockedBy = None
        self.owner = sim.curPlayer
        self.damageTaken = 0
        self.prowess = 0
        self.counter = 0
        self.tgtcreature = 0
        self.tgtplayer = 0
        self.target = None
        self.cycling = 0

    def __str__(self):
        return str(self.name)

    def getType(self):
        return self.type

    def setType(self, newtype):
        self.type = str(newtype)

    def getDamage(self):
        return self.damage

    def setDamage(self, newdamage):
        self.damage = int(newdamage)

    def getMana(self):
        return self.mana

    def setMana(self, newmana):
        self.mana = int(newmana)

    def getName(self):
        return self.name

    def setName(self, newname):
        self.name = str(newname)

    def cycle(self):
        """Cycle cards"""
        sim.curPlayer.drawCard()
        for i, o in enumerate(sim.curPlayer.myHand):
            if o.name == self.getName():
                self.owner.myGrave.append(o)
                del sim.curPlayer.myHand[i]
                break

    def getTargets(self):
#Get clocks
        tgt = sim.curPlayer
        if self.tgtcreature == 0 and self.tgtplayer == 0:
            tgt = sim.curPlayer

        if self.tgtcreature > 0 or self.tgtplayer > 0:
            myPower = 0
            for card in sim.curPlayer.myBoard:
                if card.type == "Creature":
                    myPower += card.damage
            if myPower == 0:
                myPower = .001
            myClock = math.ceil((sim.nAP.life - sim.curPlayer.getBurn()) / myPower)
            oppPower = 0
            for card in sim.nAP.myBoard:
                if card.type == "Creature":
                    oppPower += card.damage
            if oppPower == 0:
                oppPower = .001
            oppClock= math.ceil(sim.curPlayer.life / oppPower)

            if self.tgtcreature == 1 and self.tgtplayer == 1 and self.damage > 0 and self.counter == 0:

    #Burn face if myclock > oppclock
                if myClock > oppClock:
                    target = sim.nAP
                if myClock <= oppClock:
                    pot = []
                    for card in sim.nAP.myBoard:
                        if card.type == "Creature" and card.toughness <= self.damage:
                            pot.append(card)
                    if len(pot) > 0:
                        pot.sort(key=operator.attrgetter('damage'))
                        tgt = pot[-1]
                    else:
                        tgt = sim.nAP
            if self.tgtcreature == 1 and self.tgtplayer == 0 and self.damage > 0 and self.counter == 0:
    #Burn highest power creature
                pot = []
                for card in sim.nAP.myBoard:
                    if card.type == "Creature" and card.toughness <= self.damage:
                        pot.append(card)
                if len(pot) > 0:
                    pot.sort(key=operator.attrgetter('damage'))
                    tgt = pot[-1]
    #Target player
            if self.tgtcreature == 0 and self.tgtplayer == 1:
                tgt = sim.nAP

    #Target biggest creature
            if self.tgtcreature == 1 and self.tgtplayer == 0 and self.damage == 0 and self.counter == 0:
                pot = []
                for card in sim.nAP.myBoard:
                    if card.type == "Creature" and card.toughness <= self.damage:
                        pot.append(card)
                if len(pot) > 0:
                    pot.sort(key=operator.attrgetter('damage'))
                    tgt = pot[-1]
        self.target = tgt
        if self.target == None:
            self.target = sim.curPlayer

    def setTargets(self, newtargets):
        self.targets = int(self.tgtcreature) + int(self.tgtplayer)

    def getCardsDrawn(self):
        return self.cardsDrawn

    def setCardsDrawn(self, newcards):
        self.cardsDrawn = int(newcards)

    def getTapped(self):
        return self.tapped

    def tap(self):
        self.tapped = 1

    def untap(self):
        self.tapped = 0

    def setVanishing(self, val):
        self.vanishing = int(val)

    def getVanishing(self):
        return self.vanishing

    def die(self):
        """How a creature dies"""
        for i, o in enumerate(self.owner.myBoard):
            if o.name == self.getName():
                o.diesTrigger()
                self.owner.myGrave.append(o)
                del self.owner.myBoard[i]
                break

    def additionalPlay(self):
        pass

    def play(self):
        """Plays a card from hand to the stack"""
        x = self.__class__
        if self.counter == 1:
            if sim.cardsin(x, sim.nAP.myHand) > 0 and sim.nAP.availableMana >= self.getMana():
                for i, o in enumerate(sim.nAP.myHand):
                    if o.name == self.getName():
                        del sim.nAP.myHand[i]
                        break
                sim.nAP.myGrave.append(self)
                sim.nAP.availableMana -= self.getMana()
                sim.curPlayer.myStack.sort(key=operator.attrgetter('damage'))
                card = sim.curPlayer.myStack.pop()
                sim.curPlayer.myGrave.append(card)
                self.owner = sim.curPlayer
                message = "Using " + str(x) + " to counter " + str(card)
                sim.debug(message)
        if self.counter == 0:
            if sim.cardsin(x, sim.curPlayer.myHand) > 0 and sim.curPlayer.availableMana >= self.getMana():
                for i, o in enumerate(sim.curPlayer.myHand):
                    if o.name == self.getName():
                        del sim.curPlayer.myHand[i]
                        break
                sim.curPlayer.myStack.append(self)
                sim.curPlayer.availableMana -= self.getMana()
                self.owner = sim.curPlayer
                message = "Appending " + str(self.getName()) + " to stack"
                sim.debug(message)
        self.additionalPlay()

    def upkeepTrigger(self):
        pass

    def drawTrigger(self):
        pass

    def endTrigger(self):
        pass

    def etbTrigger(self):
        pass

    def diesTrigger(self):
        pass

class SearingBlaze(Card):
    """Searing Blaze"""
    def __init__(self):
        super(SearingBlaze, self).__init__()
        self.type = "Instant"
        self.damage = 3
        self.mana = 2
        self.sick = 0
        self.name = "SearingBlaze"
        self.tgtcreature = 1
        self.tgtplayer = 0

    def additionalPlay(self):
        self.owner.life -= 3

class Eidolon(Card):
    """Eidolon of the Great Revel"""
    def __init__(self):
        super(Eidolon, self).__init__()
        self.type = "Creature"
        self.damage = 2
        self.mana = 2
        self.sick = 1
        self.name = "Eidolon"
        self.toughness = 2

class Land(Card):
    """Generic rainbow land"""
    def __init__(self):
        super(Land, self).__init__()
        self.type = "Land"
        self.name = "Land"

class Fireblast(Card):
    """Fireblast"""
    def __init__(self):
        super(Fireblast, self).__init__()
        self.type = "Instant"
        self.damage = 4
        self.mana = 6
        self.sick = 0
        self.name = "Fireblast"
        self.tgtcreature = 1
        self.tgtplayer = 1

    def play(self):
        x = self.__class__
        if sim.cardsin(x, sim.curPlayer.myHand) > 0 and sim.cardsin(Land, sim.curPlayer.myBoard) >= 2:
            for i, o in enumerate(sim.curPlayer.myHand):
                if o.name == self.getName():
                    del sim.curPlayer.myHand[i]
                    break
            sim.curPlayer.myBoard.append(self)
            sim.curPlayer.maxMana -= 2
            for i, o in enumerate(sim.curPlayer.myBoard):
                if o.name == "Land":
                    del sim.curPlayer.myBoard[i]
                    break
            for i, o in enumerate(sim.curPlayer.myBoard):
                if o.name == "Land":
                    del sim.curPlayer.myBoard[i]
                    break
            message = "Playing " + str(self.getName())
            sim.debug(message)

class Fetch(Card):
    """Generic Onslaught/Zendikar fetchland"""
    def __init__(self):
        super(Fetch, self).__init__()
        self.type = "Land"
        self.name = "Fetch"

class ForgottenCave(Card):
    """Forgotten Cave"""
    def __init__(self):
        super(ForgottenCave, self).__init__()
        self.type = "Land"
        self.name = "ForgottenCave"
        self.tapped = 1
        self.mana = 1
        self.cycling = 1

class Ring(Card):
    """Barbarian Ring"""
    def __init__(self):
        super(Ring, self).__init__()
        self.type = "Land"
        self.name = "Ring"
        self.damage = 2
        self.tgtcreature = 1
        self.tgtplayer = 1

    def useRing(self):
        if (len(sim.myGrave) >= 7 and sim.availableMana >= 2):
            for i, o in enumerate(sim.curPlayer.myBoard):
                if o.name == "Ring":
                    del sim.myBoard[i]
                    sim.curPlayer.myGrave.append(Ring())
                    sim.nAP.life -= 2
                    sim.maxMana -= 1
                    break

class Hellspark(Card):
    """Hellspark Elemental"""
    def __init__(self):
        super(Hellspark, self).__init__()
        self.type = "Creature"
        self.damage = 3
        self.mana = 2
        self.sick = 0
        self.name = "Hellspark"
        self.toughness = 1

    def endTrigger(self):
        self.die()
        sim.curPlayer.myHand.append(HellsparkUnearth())

class HellsparkUnearth(Card):
    """Hellspark Elemental, unearthed"""
    def __init__(self):
        super(Hellspark, self).__init__()
        self.type = "Creature"
        self.damage = 3
        self.mana = 2
        self.sick = 0
        self.name = "Hellspark Unearth"
        self.toughness = 1

    def endTrigger(self):
        self.die()
        if sim.cardsin(HellsparkUnearth, sim.curPlayer.myGrave) > 0:
            for i, o in enumerate(sim.curPlayer.myGrave):
                if o.name == "Hellspark Unearth":
                    del sim.myBoard[i]
                    break

class Swiftspear(Card):
    """Monastery Swiftspear"""
    def __init__(self):
        super(Swiftspear, self).__init__()
        self.type = "Creature"
        self.damage = 1
        self.mana = 1
        self.sick = 0
        self.name = "Swiftspear"
        self.toughness = 2
        self.prowess = 1

class Guide(Card):
    """Goblin Guide"""
    def __init__(self):
        super(Guide, self).__init__()
        self.type = "Creature"
        self.damage = 2
        self.mana = 1
        self.sick = 0
        self.name = "Guide"
        self.toughness = 2

class Lavamancer(Card):
    """Grim Lavamancer"""
    def __init__(self):
        super(Lavamancer, self).__init__()
        self.type = "Creature"
        self.damage = 1
        self.mana = 1
        self.sick = 1
        self.name = "Lavamancer"
        self.targets = 1
        self.toughness = 1

class Marauder(Card):
    """Keldon Marauder"""
    def __init__(self):
        super(Marauder, self).__init__()
        self.type = "Creature"
        self.damage = 3
        self.mana = 2
        self.sick = 1
        self.name = "Marauder"
        self.targets = 1
        self.vanishing = 2
        self.toughness = 3

    def upkeepTrigger(self):
        x = self.getVanishing()
        x -= 1
        self.setVanishing(x)
        if self.getVanishing() <= 0:
            self.die()

    def etbTrigger(self):
        sim.nAP.life -= 1

    def diesTrigger(self):
        sim.nAP.life -= 1

class Vexing(Card):
    """Vexing Devil"""
    def __init__(self):
        super(Vexing, self).__init__()
        self.type = "Creature"
        self.damage = 4
        self.mana = 1
        self.sick = 1
        self.name = "Vexing"
        self.toughness = 3

    def etbTrigger(self):
        if sim.turn <= 2:
            sim.nAP.life -= 4
            self.die()

class Rift(Card):
    """Flame Rift"""
    def __init__(self):
        super(Rift, self).__init__()
        self.type = "Sorcery"
        self.damage = 4
        self.mana = 2
        self.sick = 0
        self.name = "Rift"

    def additionalPlay(self):
        sim.curPlayer.life -= 4

class Atarka(Card):
    """Atarka's Command, 3 damage, +1/+1 modes only"""
    def __init__(self):
        super(Atarka, self).__init__()
        self.type = "Instant"
        self.damage = 3
        self.mana = 2
        self.sick = 0
        self.name = "Atarka"
        self.tgtplayer = 1

    def play(self):
        x = self.__class__
        if sim.cardsin(x, sim.myHand) > 0 and sim.availableMana >= self.getMana():
            for i, o in enumerate(sim.myHand):
                if o.name == self.getName():
                    del sim.myHand[i]
                    break
            sim.myBoard.append(self)
            sim.availableMana -= self.getMana()
            sim.prowess += 1
            creatures = 0
            for o in sim.myBoard:
                if o.type == "Creature":
                    creatures += 1
            sim.nAP.life -= creatures
            message = "Playing " + str(self.getName())
            sim.debug(message)


class Incinerate(Card):
    """Incinerate"""
    def __init__(self):
        super(Incinerate, self).__init__()
        self.type = "Instant"
        self.damage = 3
        self.mana = 2
        self.sick = 0
        self.name = "Incinerate"
        self.tgtcreature = 1
        self.tgtplayer = 1

class Bolt(Card):
    """Lightning Bolt"""
    def __init__(self):
        super(Bolt, self).__init__()
        self.type = "Instant"
        self.damage = 3
        self.mana = 1
        self.sick = 0
        self.name = "Bolt"
        self.tgtcreature = 1
        self.tgtplayer = 1

class Chain(Card):
    """Chain Lightning"""
    def __init__(self):
        super(Chain, self).__init__()
        self.type = "Sorcery"
        self.damage = 3
        self.mana = 1
        self.sick = 0
        self.name = "Chain"
        self.tgtcreature = 1
        self.tgtplayer = 1

class Probe(Card):
    """Gitaxian Probe"""
    def __init__(self):
        super(Probe, self).__init__()
        self.type = "Sorcery"
        self.damage = 0
        self.mana = 0
        self.sick = 0
        self.name = "Probe"

    def additionalPlay(self):
        sim.curPlayer.drawCard()
        sim.curPlayer.life -= 2

class Serum(Card):
    """Serum Visions"""
    def __init__(self):
        super(Serum, self).__init__()
        self.type = "Sorcery"
        self.damage = 0
        self.mana = 1
        self.sick = 0
        self.name = "Serum"
        self.targets = 0
        self.cardsDrawn = 1

    def additionalPlay(self):
        sim.curPlayer.drawCard()
        sim.curPlayer.scry(2)

class Jet(Card):
    """Magma Jet"""
    def __init__(self):
        super(Jet, self).__init__()
        self.type = "Instant"
        self.damage = 2
        self.mana = 2
        self.sick = 0
        self.name = "Jet"
        self.tgtcreature = 1
        self.tgtplayer = 1

    def additionalPlay(self):
        sim.scry(2)

class Firecraft(Card):
    """Exquisite Firecraft"""
    def __init__(self):
        super(Firecraft, self).__init__()
        self.type = "Sorcery"
        self.damage = 4
        self.mana = 3
        self.sick = 0
        self.name = "Firecraft"
        self.tgtcreature = 1
        self.tgtplayer = 1

class Vortex(Card):
    """Sulfuric Vortex"""
    def __init__(self):
        super(Vortex, self).__init__()
        self.type = "Enchantment"
        self.damage = 0
        self.mana = 3
        self.sick= 0
        self.name = "Vortex"
        self.tgtplayer = 1

    def upkeepTrigger(self):
        sim.curPlayer.life -= 2

class DelverOfSecrets(Card):
    """Delver of Secrets"""
    def __init__(self):
        super(DelverOfSecrets, self).__init__()
        self.damage = 1
        self.toughness = 1
        self.type = "Creature"
        self.sick = 1
        self.name = "Delver"
        self.mana = 1

    def upkeepTrigger(self):
        temp = sim.curPlayer.myDeck.pop()
        if temp.type == "Instant" or temp.type == "Sorcery":
            self.damage = 3
            self.toughness = 2
        sim.curPlayer.myBoard.append(temp)

class StormchaserMage(Card):
    """Stormchaser Mage"""
    def __init__(self):
        super(StormchaserMage, self).__init__()
        self.damage = 1
        self.toughness = 2
        self.type = "Creature"
        self.sick = 0
        self.name = "Stormchaser"
        self.prowess = 1
        self.mana = 2

class Preordain(Card):
    """Preordain"""
    def __init__(self):
        super(Preordain, self).__init__()
        self.type = "Sorcery"
        self.damage = 0
        self.mana = 1
        self.sick = 0
        self.name = "Preordain"
        self.targets = 0
        self.cardsDrawn = 1

    def additionalPlay(self):
        sim.curPlayer.scry(2)
        sim.curPlayer.drawCard()

class Counterspell(Card):
    """Counterspell"""
    def __init__(self):
        super(Counterspell, self).__init__()
        self.type = "Instant"
        self.damage = 0
        self.mana = 2
        self.sick = 0
        self.name = "Force Spike"
        self.targets = 1
        self.counter = 1

class ForceSpike(Card):
    """Force Spike, actually hard counters stuff"""
    def __init__(self):
        super(ForceSpike, self).__init__()
        self.type = "Instant"
        self.damage = 0
        self.mana = 1
        self.sick = 0
        self.name = "Force Spike"
        self.targets = 1
        self.counter = 1

class Cryptic(Card):
    """Cryptic Command, counter/draw only"""
    def __init__(self):
        super(Cryptic, self).__init__()
        self.type = "Instant"
        self.damage = 0
        self.mana = 4
        self.sick = 0
        self.name = "Cryptic"
        self.targets = 1
        self.counter = 1
        self.cardsDrawn = 1

    def additionalPlay(self):
        sim.curPlayer.drawCard()


class Top(object):
    """Sensei's Divining Top"""
    #This card does not work.
    def __init__(self):
        self.type = "Top"
        self.damage = 0
        self.mana = 1
        self.sick = 0
        self.name = "Top"
        self.targets = 0
        self.cardsDrawn = 0

    def useTop(self):
        mode = self.topMode
        topList = []
        wanted = []
        unwanted = []
        for x in range(0, 3):
            sim.debug(sim.myHand)
            topList.append(sim.myDeck.pop())
        if (mode == "mana"):
            self.debug("Using Top for mana")
            sim.myHand.sort(key=lambda x: x.type)
            for card in topList:
                if (card.type != "Land"):
                    unwanted.append(card)
                if(card.type == "Land"):
                    wanted.append(card)
            for card in unwanted:
                sim.knownCards.append(card)
                sim.myDeck.append(card)
            topList = wanted
            wanted = []
            unwanted = []
            for card in topList:
                if card == Land:
                    unwanted.append(card)
                if card == Fetch:
                    wanted.append(card)
            for card in unwanted:
                sim.knownCards.append(card)
                sim.myDeck.append(card)
            for card in wanted:
                sim.knownCards.append(card)
                sim.myDeck.append(card)

        if (mode == "damage"):
            self.debug("Using Top for damage")
            sim.myHand.sort(key=lambda x: x.type)
            for card in topList:
                if (card.type == "Land"):
                    unwanted.append(card)
                if(card.type != "Land"):
                    wanted.append(card)
            for card in unwanted:
                sim.knownCards.append(card)
                sim.myDeck.append(card)
            topList = wanted
            sim.myHand.sort(key=lambda x: x.damage, reverse = True)
            while (len(topList) > 0):
                card = topList.pop()
                sim.knownCards.append(card)
                sim.myDeck.append(card)

    def tapTop(self):
        if self.cardsin(Top, self.myBoard) > 0:
            sim.drawCard()
            for i, o in enumerate(self.myBoard):
                if o.name == "Top":
                    del self.myBoard[i]
                    break
            sim.myDeck.append(Top())
            sim.knownCards.append(Top())

    def play(self):
        if (any(isinstance(x, Top) for x in sim.myHand) and sim.availableMana >= Top().mana):
            for i, o in enumerate(self.myHand):
                if o.name == "Top":
                    del self.myHand[i]
                    break
            self.myBoard.append(Top())
            self.availableMana -= Top().mana
            sim.curPlayer.prowess += 1
            self.debug("Playing Top")

    def getDamage(self):
        return self.damage


class Player(object):
    """Player class, contains data common to both players or to inherit from"""
    def __init__(self):
        self.life = 20
        self.myDeck = []
        self.myHand = []
        self.myGrave = []
        self.myBoard = []
        self.myStack = []
        self.mulligansTaken = 0
        self.mulliganNoLand = 0
        self.mulliganAllLand = 0
        self.mulliganNoCreatures = 0
        self.expensiveHand = 0
        self.maxMana = 0
        self.availableMana = 0
        self.openingHand = 7
        self.knownCards = []
        self.prowess = 0
        self.powerOnBoard = 0
        self.lavaAct = 0
        self.blockers = []
        self.unblockedAttackers = []
        self.otherPermanents = []
        self.potentialBlockers = []
        self.blockedAttackers = []
        self.fetchCount = 0
        self.landCount = 0
        self.ringCount = 0
        self.eidolonCount = 0
        self.ForgottenCaveCount = 0
        self.hellsparkCount = 0
        self.swiftspearCount = 0
        self.guideCount = 0
        self.marauderCount = 0
        self.vexingCount = 0
        self.riftCount = 0
        self.fireblastCount = 0
        self.atarkaCount = 0
        self.incinerateCount = 0
        self.boltCount = 0
        self.chainCount = 0
        self.jetCount = 0
        self.topCount = 0
        self.probeCount = 0
        self.firecraftCount = 0
        self.vortexCount = 0
        self.lavamancerCount = 0
        self.serumCount = 0
        self.crypticCount = 0
        self.forcespikeCount = 0
        self.counterspellCount = 0
        self.preordainCount = 0
        self.stormchaserCount = 0
        self.searingCount = 0
        self.delverCount = 0
        self.type = "Player"

    def sethellsparkCount(self, new):
        self.hellsparkCount = new

    def gethellsparkCount(self):
        return self.hellsparkCount

    def getMana(self):
        return self.availableMana

    def shuffle(self):
        sim.debug("Beginning shuffle...")
        random.shuffle(self.myDeck)
        self.knownCards = []
        sim.debug("Shuffle finished, known cards emptied")

    def deckList(self):
        pass

    def resolveStack(self):
#Get opponent counters
        counters = 0
        for card in sim.nAP.myHand:
            if card.counter == 1:
                counters += 1
        plays = True
        while counters > 0 and plays == True:
            plays = False
            for card in sim.nAP.myHand:
                if card.mana <= sim.nAP.availableMana and len(self.myStack) > 0 and card.counter > 0:
                    card.play()
                    counters -= 1
                    plays = True
                    del sim.curPlayer.myStack[::-1]
        for card in sim.curPlayer.myStack:
            message = "Resolving " + str(card.getName())
            sim.debug(message)
            if card.type == "Creature":
                sim.curPlayer.myBoard.append(card)
                card.etbTrigger()
            if card.type == "Sorcery" or card.type == "Instant":
                sim.curPlayer.prowess += 1
                card.getTargets()
                if card.target.type == "Player":
                    sim.nAP.life -= card.damage
                else:
                    card.damageTaken += card.damage
                sim.curPlayer.myGrave.append(card)
            if card.type == "Enchantment":
                sim.curPlayer.prowess += 1
                sim.curPlayer.myBoard.append(card)
        sim.curPlayer.myStack = []

    def mulligan(self):
        sim.debug("Starting mulligan...")
        self.mulligansTaken += 1
        sim.debug("Returning cards")
        for x in range(0, len(self.myHand)):
            self.myDeck.append(self.myHand.pop())
        self.shuffle()
        sim.debug("Shuffling cards")
        sim.debug("Mulligan finished")

    def getBurn(self):
        sim.debug("Calculating burn in hand")
        burnInHand = 0
        for card in self.myHand:
            if card.type == "Sorcery" or card.type == "Instant":
                burnInHand += card.damage
        sim.debug("Burn in hand is " + str(burnInHand))
        return burnInHand

    def playLand(self):
        sim.debug("Evaluating land drop")
        landDrop = 0
        if sim.cardsin(Fetch, sim.curPlayer.myHand) > 0 and sim.cardsin(Land, sim.curPlayer.myDeck) > 0 and landDrop == 0:
            landDrop += 1
            sim.debug("Playing fetch")
            for i, o in enumerate(sim.curPlayer.myHand):
                if o.name == "Fetch":
                    del sim.curPlayer.myHand[i]
                    break
            sim.curPlayer.myBoard.append(Fetch())
        if sim.cardsin(Land, sim.curPlayer.myHand) > 0 and landDrop == 0:
            landDrop += 1
            sim.debug("Playing land")
            for i, o in enumerate(sim.curPlayer.myHand):
                if o.name == "Land":
                    del sim.curPlayer.myHand[i]
                    break
            sim.curPlayer.myBoard.append(Land())
        if sim.cardsin(Ring, sim.curPlayer.myHand) > 0 and landDrop == 0:
            landDrop += 1
            sim.debug("Playing ring")
            for i, o in enumerate(sim.curPlayer.myHand):
                if o.name == "Ring":
                    del sim.curPlayer.myHand[i]
                    break
            sim.curPlayer.myBoard.append(Ring())
        if sim.cardsin(ForgottenCave, sim.curPlayer.myHand) > 0 and landDrop == 0:
            landDrop += 1
            sim.debug("Playing Forgotten Cave")
            for i, o in enumerate(sim.curPlayer.myHand):
                if o.name == "ForgottenCave":
                    del sim.curPlayer.myHand[i]
                    break
            sim.curPlayer.myBoard.append(ForgottenCave())

    def useFetch(self):
        if (any(isinstance(x, Fetch) for x in sim.curPlayer.myBoard) and any(isinstance(y, Land) for y in sim.curPlayer.myDeck)):
            sim.debug("Using Fetch for mana")
            for i, o in enumerate(sim.curPlayer.myBoard):
                if o.name == "Fetch":
                    del sim.curPlayer.myBoard[i]
                    break
            for i, o in enumerate(sim.curPlayer.myDeck):
                if o.name == "Land":
                    del sim.curPlayer.myDeck[i]
                    break
            sim.curPlayer.myBoard.append(Land())
            sim.curPlayer.myGrave.append(Fetch())
            sim.curPlayer.availableMana += 1
            sim.curPlayer.shuffle()

    def drawCard(self):
        self.myDraw = []
        if(len(self.myDeck) > 0):
            self.myDraw.append(self.myDeck.pop())
            if sim.curPlayer.deckName == "Burn" and sim.draw == 1:
                sim.recordDraw()
            if len(self.knownCards) > 0:
                thing = self.knownCards.pop()
            sim.debug("Drawing card (" + str(self.myDraw[0]) + ")")
            sim.debug("Cards remaining: " + str(len(self.myDeck)))
            self.myHand.append(self.myDraw[0])

    def buildDeck(self):
        sim.debug("Beginning deck building")
        self.myDeck = []
        self.myBoard = []
        self.myHand = []
        self.myGrave = []
        self.myStack = []
        for x in range(0, sim.curPlayer.topCount):
            self.myDeck.append(Top())
        for x in range(0, self.fetchCount):
            self.myDeck.append(Fetch())
        for x in range(0, self.landCount):
            self.myDeck.append(Land())
        for x in range(0, self.eidolonCount):
            self.myDeck.append(Eidolon())
        for x in range(0, self.hellsparkCount):
            self.myDeck.append(Hellspark())
        for x in range(0, self.swiftspearCount):
            self.myDeck.append(Swiftspear())
        for x in range(0, self.guideCount):
            self.myDeck.append(Guide())
        for x in range(0, self.marauderCount):
            self.myDeck.append(Marauder())
        for x in range(0, self.vexingCount):
            self.myDeck.append(Vexing())
        for x in range(0, self.riftCount):
            self.myDeck.append(Rift())
        for x in range(0, self.fireblastCount):
            self.myDeck.append(Fireblast())
        for x in range(0, self.atarkaCount):
            self.myDeck.append(Atarka())
        for x in range(0, self.incinerateCount):
            self.myDeck.append(Incinerate())
        for x in range(0, self.boltCount):
            self.myDeck.append(Bolt())
        for x in range(0, self.chainCount):
            self.myDeck.append(Chain())
        for x in range(0, self.jetCount):
            self.myDeck.append(Jet())
        for x in range(0, self.probeCount):
            self.myDeck.append(Probe())
        for x in range(0, self.ForgottenCaveCount):
            self.myDeck.append(ForgottenCave())
        for x in range(0, self.firecraftCount):
            self.myDeck.append(Firecraft())
        for x in range(0, self.vortexCount):
            self.myDeck.append(Vortex())
        for x in range(0, self.lavamancerCount):
            self.myDeck.append(Lavamancer())
        for x in range(0, self.ringCount):
            self.myDeck.append(Ring())
        for x in range(0, self.serumCount):
            self.myDeck.append(Serum())
        for x in range(0, self.crypticCount):
            self.myDeck.append(Cryptic())
        for x in range(0, self.forcespikeCount):
            self.myDeck.append(ForceSpike())
        for x in range(0, self.counterspellCount):
            self.myDeck.append(Counterspell())
        for x in range(0, self.preordainCount):
            self.myDeck.append(Preordain())
        for x in range(0, self.stormchaserCount):
            self.myDeck.append(StormchaserMage())
        for x in range(0, self.delverCount):
            self.myDeck.append(DelverOfSecrets())
        for x in range(0, self.searingCount):
            self.myDeck.append(SearingBlaze())
        random.shuffle(self.myDeck)
        sim.debug("Deck built")

    def resolveMulligans(self):
        pass

    def declareBlocks(self):
        """Blocking, I'm sorry"""
        #Set up variables
        sim.nAP.potentialBlockers = []
        sim.curPlayer.blockedAttackers = []
        sim.curPlayer.unblockedAttackers = []
        blkPwr = []
        blkTough = []
        defClock = 0
        atkPwr = []
        atkTough = []
        #Find my clock
        for card in sim.nAP.myBoard:
            if card.type == "Creature":
                defClock += card.damage
        atkClock = 0
        #Find known attacker clock
        for card in sim.curPlayer.myBoard:
            if card.type == "Creature":
                atkClock += card.damage
        #Block if opponent will win first
        if atkClock > defClock and len(sim.nAP.potentialBlockers) > 0:
            sim.nAP.myBoardCpy = sim.nAP.myBoard
            #Make list of potential blockers
            for card in sim.nAP.myBoardCpy:
                if card.type == "Creature" and card.tapped == 0:
                    sim.nAP.potentialBlockers.append(card)
                    blkPwr.append(card.damage)
                    blkTough.append(card.toughness)
                    sim.nAP.myBoard.remove(card)
            for card in sim.curPlayer.attackers:
                atkPwr.append(card.power)
                atkTough.append(card.toughness)
            toblock = []
#Highest power blocker on highest toughness attacker it can kill
            bigBlockIdx = blkPwr.index(max(blkPwr))
            bigBlock = max(blkPwr)
            atkIdx = None
            #find highest toughness I can trade with, I should use a do/while
            highest = 0
            for val in range(len(sim.curPlayer.atkTough)):
                if sim.curPlayer.atkTough[val] >= highest and highest <= bigBlock:
                    highest = sim.curPlayer.atkTough[val]
                    atkIdx = val
            while atkIdx != None:
                sim.nAP.potentialBlockers[bigBlockIdx].blocking = sim.curPlayer.attackers[atkIdx]
                sim.curPlayer.attackers[atkIdx].blockedBy = sim.nAP.potentialBlockers[bigBlockIdx]
                sim.nAP.myBoard.append(sim.nAP.potentialBlockers[bigBlockIdx])
                del sim.nAP.potentialBlockers[bigBlockIdx]
                sim.curPlayer.blockedAttackers.append(sim.curPlayer.attackers[atkIdx])
                del sim.curPlayer.attackers[atkIdx]
                del sim.curPlayer.atkPwr[atkIdx]
                del sim.curPlayer.atkTough[atkIdx]
                atkIdx = None
                bigBlockIdx = blkPwr.index(max(blkPwr))
                bigBlock = max(blkPwr)
                highest = 0
                #find highest toughness I can trade with
                for val in range(len(sim.curPlayer.atkTough)):
                    if sim.curPlayer.atkTough[val] >= highest and highest <= bigBlock:
                        highest = sim.curPlayer.atkTough[val]
                        atkIdx = val

#Blockers with toughness > opposing power on remaining attackers, so they bounce vs die
            bigBlockIdx = blkTough.index(max(blkTough))
            bigBlock = max(blkTough)
            atkIdx = None
            highest = 0
            for val in range(len(sim.curPlayer.atkPwr)):
                if sim.curPlayer.atkPwr[val] < highest and highest < bigBlock:
                    highest = sim.curPlayer.atkPwr[val]
                    atkIdx = val
            while atkIdx != None:
                sim.nAP.potentialBlockers[bigBlockIdx].blocking = sim.curPlayer.attackers[atkIdx]
                sim.curPlayer.attackers[atkIdx].blockedBy = sim.nAP.potentialBlockers[bigBlockIdx]
                sim.nAP.myBoard.append(sim.nAP.potentialBlockers[bigBlockIdx])
                del sim.nAP.potentialBlockers[bigBlockIdx]
                sim.curPlayer.blockedAttackers.append(sim.curPlayer.attackers[atkIdx])
                del sim.curPlayer.attackers[atkIdx]
                bigBlockIdx = blkTough.index(max(blkTough))
                bigBlock = max(blkTough)
                atkIdx = None
                highest = 0
                for val in range(len(sim.curPlayer.atkPwr)):
                    if sim.curPlayer.atkPwr[val] < highest and highest < bigBlock:
                        highest = sim.curPlayer.atkPwr[val]
                        atkIdx = val
#Chump blocks to change clock speed
            defDmg = 0
            for card in sim.nAP.myBoard:
                if card.type == "Creature":
                    defDmg += card.damage
            for card in sim.nAP.potentialBlockers:
                defDmg += card.damage
            atkDmg = 0
            for card in sim.curPlayer.attackers:
                atkDmg += card.damage
            defClock = math.ceil((sim.curPlayer.life - getBurn()) / defDmg)
            atkClock = math.ceil((sim.nAP.life / atkDmg))
            lifegain = 0
            while atkClock >= defClock and len(sim.curPlayer.attackers) > 0 and len(sim.nAP.potentialBlockers) > 0 and len(atkClock)< 5:
                smallBlockIdx = blkPwr.index(min(blkPwr))
                smallBlock = min(blkPwr)
                atkIdx = None
                #find highest power I can chump
                atkIdx = sim.curPlayer.atkPwr.index(max(sim.curPlayer.atkPwr))
                lifegain += max(sim.curPlayer.atkPwr)
                sim.nAP.potentialBlockers[smallBlockIdx].blocking = sim.curPlayer.attackers[atkIdx]
                sim.curPlayer.attackers[atkIdx].blockedBy = sim.nAP.potentialBlockers[smallBlockIdx]
                sim.nAP.myBoard.append(sim.nAP.potentialBlockers[smallBlockIdx])
                del sim.nAP.potentialBlockers[smallBlockIdx]
                sim.curPlayer.blockedAttackers.append(sim.curPlayer.attackers[atkIdx])
                del sim.curPlayer.attackers[atkIdx]
                del sim.curPlayer.atkPwr[atkIdx]
                del sim.curPlayer.atkTough[atkIdx]
                defDmg = 0
                for card in sim.nAP.myBoard:
                    if card.type == "Creature":
                        defDmg += card.damage
                for card in sim.nAP.potentialBlockers:
                    defDmg += card.damage
                atkDmg = 0
                for card in sim.curPlayer.attackers:
                    atkDmg += card.damage
                defClock = math.ceil((sim.curPlayer.life - getBurn()) / defDmg)
                atkClock = math.ceil((sim.nAP.life + lifegain)/ atkDmg)
        #Move everything not blocked to unblocked attackers
        for card in sim.curPlayer.attackers:
            sim.curPlayer.unblockedAttackers.append(card)


    def declareAttacks(self):
        """Declare attacks.  I'm so, so, so sorry for this code"""
        sim.debug("Declaring Attacks")
        sim.debug("Adding Prowess")
        #Add prowess
        for card in sim.curPlayer.myBoard:
            if card.type == "Creature" and card.prowess == 1:
                card.damage += sim.curPlayer.prowess
                card.toughness += sim.curPlayer.prowess
        for card in sim.nAP.myBoard:
            if card.type == "Creature" and card.prowess == 1:
                card.damage += sim.nAP.prowess
                card.toughness += sim.nAP.prowess
        #Set up lists
        sim.curPlayer.atkPwr = []
        sim.curPlayer.potentialAttacks = []
        sim.curPlayer.attackers = []
        sim.curPlayer.otherPermanents = []

    #Get potential attackers/blockers
        sim.curPlayer.potentialBlocks = []
        for card in sim.nAP.myBoard:
            if card.type == "Creature" and card.tapped == 0:
                sim.curPlayer.potentialBlocks.append(card)

        for card in sim.curPlayer.myBoard:
            if card.type == "Creature" and card.tapped == 0 and card.sick < 1:
                sim.curPlayer.potentialAttacks.append(card)
                msg = card.name + " is potentially attacking"
                sim.debug(msg)
                sim.curPlayer.atkPwr.append(card.damage)
            else:
                sim.curPlayer.otherPermanents.append(card)

        #Look at impact of all attacking
        if sum(sim.curPlayer.atkPwr) > 0:
            sim.debug("Attacks are possible")
            myClock = math.ceil((sim.nAP.life - sim.curPlayer.getBurn())/sum(sim.curPlayer.atkPwr))
            oppPwr = []
            for card in sim.nAP.myBoard:
                if card.type == "Creature":
                    oppPwr.append(card.damage)
            if sum(oppPwr) == 0:
                oppPwr.append(0.001)
            oppClock = math.ceil(sim.curPlayer.life/sum(oppPwr))
            lifegained = 0
#Remove attackers to slow opp clock
            while oppClock < myClock and len(sim.curPlayer.atkPwr) > 0:
                idx = sim.curPlayer.atkPwr.index(min(sim.curPlayer.atkPwr))
                card = sim.curPlayer.potentialAttacks[idx]
                msg = card.name + " is not attacking"
                sim.debug(msg)
                sim.curPlayer.otherPermanents.append(sim.curPlayer.potentialAttacks[idx])
                del sim.curPlayer.potentialAttacks[idx]
                del sim.curPlayer.atkPwr[idx]
                blkIdx = oppPwr.index(max(oppPwr))
                lifegained += max(oppPwr)
                del oppPwr[blkIdx]
                x = sum(sim.curPlayer.atkPwr)
                if x == 0:
                    x = .001
                if sum(oppPwr) == 0:
                    oppPwr.append(0.001)
                myClock = math.ceil((sim.nAP.life - sim.curPlayer.getBurn())/x)
                oppClock = math.ceil((sim.curPlayer.life + lifegained)/ sum(oppPwr))
#Remove attackers if nothing gets through
            if len(sim.curPlayer.potentialAttacks) < len(sim.curPlayer.potentialBlockers):
                sim.debug("No profitable attacks")
                for card in sim.curPlayer.potentialAttacks:
                    sim.curPlayer.otherPermanents.append(card)
                sim.curPlayer.potentialAttacks = []
#Finalize attacks
            sim.curPlayer.attackers = sim.curPlayer.potentialAttacks
            msg = "Attackers are " + str(sim.curPlayer.attackers)
            sim.debug(msg)
            msg = "Everything else is " + str(sim.curPlayer.otherPermanents)
            sim.debug(msg)

class P1(Player):
    """Player 1"""
    def __init__(self):
        """P1 variables, basically decklist and life"""
        super(P1, self).__init__()
        self.life = 20
        self.fetchCount = 0
        self.landCount = 22
        self.ForgottenCaveCount = 0
        self.ringCount = 1
        self.eidolonCount = 5
        self.hellsparkCount = 0
        self.swiftspearCount = 3
        self.guideCount = 3
        self.marauderCount = 0
        self.vexingCount = 0
        self.riftCount = 6
        self.fireblastCount = 2
        self.atarkaCount = 0
        self.incinerateCount = 0
        self.boltCount = 6
        self.chainCount = 4
        self.firecraftCount = 4
        self.vortexCount = 0
        self.lavamancerCount = 0
        self.serumCount = 0
        self.searingCount = 4
        self.deckName = "Burn"

    def getBlockers(self):
        """Finds number of blockers opponent has"""
        blockers = 0
        if len(sim.nAP.myBoard) > 0:
            for card in sim.nAP.myBoard:
                if card.type == "Creature" and card.tapped == 0:
                    blockers + 1
        return blockers

    def negs(self):
        """Reasons to not play a spell"""
#Overextension
        blockers = self.getBlockers()
        attackers = 0
        for x in range(len(sim.curPlayer.myBoard)):
            if (sim.curPlayer.myBoard[x].type == "Creature"):
                attackers += 1
        for x in range(len(self.myHand)):
            if attackers - blockers > 2:
                if self.myHand[x].type == "Creature":
                    self.cardScore[x] -= 3

    def getClock(self):
        """Get my clock"""
        clock = 9999
        for card in self.myBoard:
            if card.type == "Creature":
                self.powerOnBoard += card.damage
        if self.powerOnBoard != 0:
            clock = math.ceil(sim.nAP.life/self.powerOnBoard)
        return clock

    def getNewClock(self, newcard):
        """Get clock if new card played"""
        clock = 9999
        if newcard.damage > 0:
            self.powerOnBoard = 0
            for card in self.myBoard:
                if card.type == "Creature":
                    self.powerOnBoard += card.damage * (card.sick + 1)
            if newcard.type == "Instant" or newcard.type == "Sorcery":
                if self.powerOnBoard != 0:
                    clock = math.ceil((sim.nAP.life - newcard.damage)/self.powerOnBoard)
            if newcard.type == "Creature":
                if newcard.sick == 0:
                    clock = math.ceil(sim.nAP.life/(self.powerOnBoard + newcard.damage))
                if newcard.sick == 1:
                    clock = math.ceil((sim.nAP.life + newcard.damage)/(self.powerOnBoard + newcard.damage))
        return clock

    def plusses(self):
        """Reasons to play a spell"""
        #Bonus for number of targets, makes higher value for 2 for 1's
        for x in range(len(self.myHand)):
            self.cardScore[x] += self.myHand[x].targets
        #Bonus for drawing cards, makes cantrips and 2 for 1's better
        for x in range(len(self.myHand)):
            self.cardScore[x] += self.myHand[x].cardsDrawn
        #Bonus for speeding clock
        for x in range(len(self.myHand)):
            if self.getNewClock(self.myHand[x]) < self.getClock():
                self.cardScore[x] += 3
        #Bonus for highest impact
        highDamage = 0
        for card in self.myHand:
            if card.damage >= highDamage:
                highDamage = card.damage
        for x in range(len(self.myHand)):
            if self.myHand[x].damage >= highDamage:
                self.cardScore[x] += 1
        #Bonus for dodging interaction
        for x in range(len(self.myHand)):
            if self.myHand[x].type != "Creature":
                self.cardScore[x] += 1
        #Bonus for burning opponent out
        burn = sim.curPlayer.getBurn()
        for x in range(len(self.myHand)):
            if burn >= sim.nAP.life and self.myHand[x].type == "Instant" or burn >= sim.nAP.life and self.myHand[x].type == "Sorcery":
                self.cardScore[x] += 5
        #Bonus for early creature
        if sim.turn <= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].type == "Creature":
                    self.cardScore[x] += 1
        #Bonus for cycling land
        if sim.curPlayer.availableMana >= 3:
            for x in range(len(self.myHand)):
                if self.myHand[x].cycling == 1:
                    self.cardScore[x] += 1

    def findCurve(self):
        """Builds mana curve, creates bonus for positive tempo"""
        #Uses all mana
        for x in range(len(self.myHand)):
            if self.myHand[x].mana == self.availableMana:
                self.cardScore[x] += 1
        #Cast 2 2's
        if self.availableMana == 4 and self.manaList[2] >= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].mana == 2:
                    self.cardScore[x] += 3
        #Cast 2 1's
        if self.availableMana == 2 and self.manaList[1] >= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].mana == 1:
                    self.cardScore[x] += 3
        #Cast 0's
        for x in range(len(self.myHand)):
            if self.myHand[x].mana == 0:
                self.cardScore[x] += 10

    def buildManaList(self):
        """2d array of cards in hand by cost"""
        self.manaList = [0] * 15
        for card in self.myHand:
            self.manaList[card.mana] += 1

    def join(self, hand):
        """Joins cards with card score to sort by rank"""
        joins = []
        for x in range(len(hand)):
            tup = self.myHand[x], self.cardScore[x]
            joins.append(tup)
        joins = sorted(joins, key=lambda x: x[1], reverse = True)
        self.myHand = []
        self.cardScore = []
        for x in range(len(joins)):
            self.myHand.append(joins[x][0])
            self.cardScore.append(joins[x][1])

    def getPlays(self):
        """Create play list and score list"""
        self.cardScore = None
        self.cardScore = [0] * len(self.myHand)
        self.buildManaList()
        self.findCurve()
        self.plusses()
        self.negs()
        self.join(self.myHand)
        sim.debug(self.myHand)
        sim.debug(self.cardScore)

    def scry(self, value):
        """Scry"""
        sim.debug("Scry " + str(value))
        mana = 0
        scryList = []
        self.myHand.sort(key=operator.attrgetter('type'))
        for card in self.myHand:
            if(card.type == "Land"):
                mana += 1
        mana += self.maxMana
        for x in range(0, value):
            scryList.append(self.myDeck.pop())
        scryList.sort(key=operator.attrgetter('damage'))
        for x in range(0, value):
            card = scryList.pop(0)
            if (card.damage == 0 and mana > 3):
                sim.debug(card.name)
                sim.debug("Scry to bottom")
                self.myDeck.insert(0, card)
            if (card.damage > 0):
                sim.debug(card.name)
                sim.debug("Scry to top")
                self.knownCards.append(card)
                self.myDeck.append(card)
            if (card.damage == 0 and self.maxMana <= 3):
                sim.debug(card.name)
                sim.debug("Scry to top")
                self.knownCards.append(card)
                self.myDeck.append(card)

    def resolveMulligans(self):
        """Mulligan logic"""
        mulliganReasons = 1
        while(mulliganReasons > 0):
            mulliganReasons = 0
            sim.debug("P1: Determining mulligan")
            for x in range(self.openingHand):
                self.drawCard()
            recurring = 0
            land = 0
            spells = 0
            top = 0
            mana = 0
            for card in self.myHand:
                if card.type == "Creature":
                    recurring += 1
                if card.type == "Land":
                    land += 1
                if card.type == "Instant" or card.type == "Sorcery":
                    spells += 1
                if card.type == "Top":
                    top += 1
                mana += card.mana
#7 card decision
            if (len(self.myHand) == 7):
                sim.debug("P1: Evaluating 7 card keep")
                if (land < 2):
                    sim.debug("P1: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 4):
                    sim.debug("P1: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if (recurring < 1):
                    sim.debug("P1: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if(top > 2):
                    sim.debug("P1: Mulligan top flood")
                    mulliganReasons += 1
                    self.topFlood += 1
                x = 10 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P1: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

#6 card decision
            if (len(self.myHand) == 6):
                sim.debug("P1: Evaluating 6 card keep")
                if (land < 2):
                    sim.debug("P1: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 3):
                    sim.debug("P1: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if (recurring < 1):
                    sim.debug("P1: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if(top > 2):
                    sim.debug("P1: Mulligan top flood")
                    mulliganReasons += 1
                    self.topFlood += 1
                x = 9 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P1: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

#5 card decision
            if (len(self.myHand) == 5):
                sim.debug("P1: Evaluating 5 card keep")
                if (land < 1):
                    sim.debug("P1: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 2):
                    sim.debug("P1: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if (recurring < 1):
                    sim.debug("P1: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if(top > 1):
                    sim.debug("P1: Mulligan top flood")
                    mulliganReasons += 1
                    self.topFlood += 1

#4 card decision
            if (len(self.myHand) == 4):
                sim.debug("P1: Evaluating 4 card keep")
                if (land < 1):
                    sim.debug("P1: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land >= 4):
                    sim.debug("P1: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if (recurring < 1):
                    sim.debug("P1: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if(top > 2):
                    sim.debug("P1: Mulligan top flood")
                    mulliganReasons += 1
                    self.topFlood += 1

#3 card decision
            if (len(self.myHand) == 3):
                sim.debug("P1: Evaluating 3 card keep")
                if (land < 1):
                    sim.debug("P1: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land >= 3):
                    sim.debug("P1: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if (recurring < 1):
                    sim.debug("P1: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1

            if (len(self.myHand) < 3):
                sim.debug("P1: Forced to keep 2 card hand")

            if (mulliganReasons > 0):
                self.mulligan()
                self.openingHand -= 1

class P2(Player):
    """See P1"""
    def __init__(self):
        super(P2, self).__init__()
        self.fetchCount = 8
        self.landCount = 10
        self.swiftspearCount = 4
        self.stormchaserCount = 4
        self.delverCount = 4
        self.riftCount = 4
        self.fireblastCount = 2
        self.boltCount = 4
        self.chainCount = 2
        self.probeCount = 4
        self.preordainCount = 4
        self.serumCount = 4
        self.firecraftCount = 1
        self.crypticCount = 1
        self.counterspellCount = 3
        self.forcespikeCount = 2
        self.deckName = "Delver"

    def resolveMulligans(self):
        mulliganReasons = 1
        while(mulliganReasons != 0):
            mulliganReasons = 0
            sim.debug("P2: Determining mulligan")
            for x in range(self.openingHand):
                self.drawCard()
            recurring = 0
            land = 0
            removal = 0
            cantrip = 0
            counter = 0
            mana = 0

            for card in self.myHand:
                if card.type == "Creature":
                    recurring += 1
                if card.type == "Land":
                    land += 1
                if card.type == "Instant" or card.type == "Sorcery":
                    if card.damage > 0:
                        removal += 1
                    if card.cardsDrawn > 0:
                        cantrip += 1
                    if card.targets > 0 and card.damage <= 0:
                        counter += 1
                mana += card.mana

#7 card decision
            if (len(self.myHand) == 7):
                sim.debug("P2: Evaluating 7 card keep")
                if (recurring < 1):
                    sim.debug("P2: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if (counter <1):
                    sim.debug("P2: Mulligan no counters")
                    mulliganReasons += 1
                if (land < 1):
                    sim.debug("P2: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 3):
                    sim.debug("P2: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if(cantrip < 1):
                    sim.debug("P2: Mulligan no cantrips")
                    mulliganReasons += 1
                if (removal < 1):
                    sim.debug("P2: Mulligan no removal")
                    mulliganReasons += 1
                x = 9 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P2: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

    #6 card decision
            if (len(self.myHand) == 6):
                sim.debug("P2: Evaluating 6 card keep")
                if (recurring < 1):
                    sim.debug("P2: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if (counter <1):
                    sim.debug("P2: Mulligan no counters")
                    mulliganReasons += 1
                if (land < 1):
                    sim.debug("P2: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 3):
                    sim.debug("P2: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                if(cantrip < 1):
                    sim.debug("P2: Mulligan no cantrips")
                    mulliganReasons += 1
                if (removal < 1):
                    sim.debug("P2: Mulligan no removal")
                    mulliganReasons += 1
                x = 8 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P2: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

    #5 card decision
            if (len(self.myHand) == 5):
                sim.debug("P2: Evaluating 5 card keep")
                if (recurring < 1):
                    sim.debug("P2: Mulligan no creatures")
                    mulliganReasons += 1
                    self.mulliganNoCreatures += 1
                if (land < 1):
                    sim.debug("P2: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                if(land > 3):
                    sim.debug("P2: Mulligan mana flood")
                    mulliganReasons += 1
                    self.mulliganAllLand += 1
                x = 7 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P2: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

    #4 card decision
            if (len(self.myHand) == 4):
                sim.debug("P2: Evaluating 4 card keep")
                if (land < 1):
                    sim.debug("P2: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1
                x = 6 + (sim.cardsin(Fireblast, self.myHand) * 6)
                if(mana > x):
                    sim.debug("P2: Mulligan expensive hand")
                    mulliganReasons += 1
                    self.expensiveHand += 1

    #3 card decision
            if (len(self.myHand) == 3):
                sim.debug("P2: Evaluating 3 card keep")
                if (land < 1 and cantrip < 1):
                    sim.debug("P2: Mulligan no land")
                    mulliganReasons += 1
                    self.mulliganNoLand += 1

            if (len(self.myHand) < 3):
                sim.debug("P2: Forced to keep 2 card hand")

            if (mulliganReasons > 0):
                self.mulligan()
                self.openingHand -= 1

    def scry(self, value):
        sim.debug("Scry " + str(value))
        mana = 0
        scryList = []
        self.myHand.sort(key=operator.attrgetter('type'))
        for card in self.myHand:
            if(card.type == "Land"):
                mana += 1
        mana += self.maxMana
        for x in range(0, value):
            scryList.append(self.myDeck.pop())
        for x in range(0, value):
            card = scryList.pop(0)
            if (card.type != "Land"):
                self.knownCards.append(card)
                self.myDeck.append(card)
                sim.debug(card.name)
                sim.debug("Scry to top")
            else:
                sim.debug(card.name)
                sim.debug("Scry to bottom")
                self.myDeck.insert(0, card)


    def getBlockers(self):
    	blockers = 0
    	if len(sim.nAP.myBoard) > 0:
    		for card in sim.nAP.myBoard:
    			if card.type == "Creature" and card.tapped == 0:
    				blockers + 1
    	return blockers

    def negs(self):
#Overextension
        blockers = self.getBlockers()
        attackers = 0
        for x in range(len(self.myBoard)):
            if (self.myBoard[x].type == "Creature"):
                attackers += 1
        for x in range(len(self.myHand)):
            if attackers - blockers > 2:
                if self.myHand[x].type == "Creature":
                    self.cardScore[x] -= 3

    def getClock(self):
        clock = 9999
        for card in self.myBoard:
            if card.type == "Creature":
                self.powerOnBoard += card.damage
        if self.powerOnBoard != 0:
            clock = math.ceil(sim.nAP.life/self.powerOnBoard)
        return clock

    def getNewClock(self, newcard):
        clock = 9999
        self.powerOnBoard = 0
        for card in self.myBoard:
            if card.type == "Creature":
                self.powerOnBoard += card.damage * (card.sick + 1)
        if newcard.type == "Instant" or newcard.type == "Sorcery":
            if self.powerOnBoard != 0:
                clock = math.ceil((sim.nAP.life - newcard.damage)/self.powerOnBoard)
        if newcard.type == "Creature":
            if newcard.sick == 0:
                clock = math.ceil(sim.nAP.life/(self.powerOnBoard + newcard.damage))
            if newcard.sick == 1:
                clock = math.ceil((sim.nAP.life + newcard.damage)/(self.powerOnBoard + newcard.damage))
        return clock

    def plusses(self):
        #Bonus for number of targets, makes higher value for 2 for 1's
        for x in range(len(self.myHand)):
            self.cardScore[x] += self.myHand[x].targets
        #Bonus for drawing cards, makes cantrips and 2 for 1's better
        for x in range(len(self.myHand)):
            self.cardScore[x] += self.myHand[x].cardsDrawn
        #Bonus for speeding clock
        for x in range(len(self.myHand)):
            if self.getNewClock(self.myHand[x]) < self.getClock():
                self.cardScore[x] += 3
        #Bonus for highest impact
        highDamage = 0
        for card in self.myHand:
            if card.damage >= highDamage:
                highDamage = card.damage
        for x in range(len(self.myHand)):
            if self.myHand[x].damage >= highDamage:
                self.cardScore[x] += 1
        #Bonus for dodging interaction
        for x in range(len(self.myHand)):
            if self.myHand[x].type != "Creature":
                self.cardScore[x] += 1
        #Bonus for burning opponent out
        burn = sim.curPlayer.getBurn()
        for x in range(len(self.myHand)):
            if burn >= sim.nAP.life and self.myHand[x].type == "Instant" or burn >= sim.nAP.life and self.myHand[x].type == "Sorcery":
                self.cardScore[x] += 5
        #Bonus for early creature
        if sim.turn <= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].type == "Creature":
                    self.cardScore[x] += 1
        #Bonus for cycling land
        if sim.curPlayer.availableMana >= 3:
            for x in range(len(self.myHand)):
                if self.myHand[x].cycling == 1:
                    self.cardScore[x] += 1

    def findCurve(self):
        #Uses all mana
        for x in range(len(self.myHand)):
            if self.myHand[x].mana == self.availableMana:
                self.cardScore[x] += 1
        #Cast 2 2's
        if self.availableMana == 4 and self.manaList[2] >= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].mana == 2:
                    self.cardScore[x] += 3
        #Cast 2 1's
        if self.availableMana == 2 and self.manaList[1] >= 2:
            for x in range(len(self.myHand)):
                if self.myHand[x].mana == 1:
                    self.cardScore[x] += 3
        #Cast 0's
        for x in range(len(self.myHand)):
            if self.myHand[x].mana == 0:
                self.cardScore[x] += 10

    def buildManaList(self):
        self.manaList = [0] * 15
        for card in self.myHand:
            self.manaList[card.mana] += 1

    def join(self, hand):
        joins = []
        for x in range(len(hand)):
            tup = self.myHand[x], self.cardScore[x]
            joins.append(tup)
        joins = sorted(joins, key=lambda x: x[1], reverse = True)
        self.myHand = []
        self.cardScore = []
        for x in range(len(joins)):
            self.myHand.append(joins[x][0])
            self.cardScore.append(joins[x][1])

    def getPlays(self):
        #Create play list and score list
        self.cardScore = None
        self.cardScore = [0] * len(self.myHand)
        self.buildManaList()
        self.findCurve()
        self.plusses()
        self.negs()
        self.join(self.myHand)
        sim.debug(self.myHand)
        sim.debug(self.cardScore)


#Main program
print(ctime())
print("Running simulation, check back later")
sim = Simulator()
sim.setParams()
print("Simulation finished")
print(ctime())