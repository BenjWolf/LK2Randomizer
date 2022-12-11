import sqlite3
import entities
from LK2Randomizer import Constants

class DBConnection:
    def __init__(self):
        connection = sqlite3.connect(Constants.dbPath)
        self.cursor = connection.cursor()

    #region card queries
    """
    0 number
    1 name
    2 hexCode
    3 rarity
    4 isKeyCard
    """
    def getCardByNumber(self, number):
        result = self.cursor.execute(f"SELECT * FROM cards where number = {number}")
        row = result.fetchone()
        card = entities.Card(row[0], row[1], row[2], row[3], row[4])
        return card
    
    def checkKeyCardByNumber(self, number):
        result = self.cursor.execute(f"SELECT * FROM cards where number = {number}")
        row = result.fetchone()
        isKeyCard = row[4]
        return isKeyCard

    def getAllCards(self):
        cardList = list()

        for row in self.cursor.execute("SELECT * FROM cards"):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4])
            cardList.append(card)
        return cardList

    def getAllNonKeyCards(self):
        cardList = list()

        for row in self.cursor.execute("SELECT * FROM cards WHERE isKeyCard = 0"):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4])
            cardList.append(card)
        return cardList
    #endregion

    #region location queries
    """
    0 id
    1 name
    2 level
    3 originalCardNumber
    4 isoAddress
    5 missable
    """
    def getLocationById(self, id):
        result = self.cursor.execute(f"SELECT * FROM location where id = {id}")
        row = result.fetchone()
        location = entities.Location(row[0], row[1], row[2], row[3], row[4], row[5])
        return location
    
    def getAllLocations(self):
        locationList = list()
        
        for row in self.cursor.execute("SELECT * FROM location"):
            location = entities.Location(row[0], row[1], row[2], row[3], row[4], row[5])
            locationList.append(location)
        return locationList
    #endregion

#testing
#connector = DBConnection()
