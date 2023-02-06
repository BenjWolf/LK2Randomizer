import sqlite3
import entities
from LK2Randomizer import Constants

class DBConnection:
    def __init__(self):
        connection = sqlite3.connect(Constants.dbPath)
        self.cursor = connection.cursor()
    
    #card queries
    #region 
    """
    0 number
    1 name
    2 hexCode
    3 rarity
    4 isKeyCard
    5 isShopCard
    """
    def getCardByNumber(self, number):
        result = self.cursor.execute(f"SELECT number, name, hexCode, rarity, isKeyCard, isShopCard FROM cards WHERE number = {number}")
        row = result.fetchone()
        card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5])
        return card

    def getAllCards(self):
        cardList = list()

        for row in self.cursor.execute("SELECT number, name, hexCode, rarity, isKeyCard, isShopCard FROM cards"):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5])
            cardList.append(card)
        return cardList

    #def getAllNonKeyCards(self):
    #    cardList = list()

    #    for row in self.cursor.execute("SELECT number, name, hexCode, rarity, isKeyCard, isShopCard FROM cards WHERE isKeyCard = 0"):
    #        card = entities.Card(row[0], row[1], row[2], row[3])
    #        cardList.append(card)
    #    return cardList
    #endregion
    
    #starting deck
    #region 
    """
    0 id
    1 isoAddress
    2 cardNumber
    """
    def getStartingDeck(self):
        startingDeckList = list()

        for row in self.cursor.execute("SELECT * FROM startingDeck"):
            slot = entities.StartingDeckSlot(row[0], row[1], row[2])
            startingDeckList.append(slot)
        return startingDeckList
    #endregion

    #location queries
    #region 
    """
    0 id
    1 name
    2 level
    3 cardNumber
    4 isoAddress
    """
    def getAllLocations(self):
        locationList = list()
        
        for row in self.cursor.execute("SELECT id, name, level, cardNumber, isoAddress FROM location"):
            location = entities.CardLocation(row[0], row[1], row[2], row[3], row[4])
            locationList.append(location)
        return locationList
    #endregion

    #shop
    #region 
    """
    0 id
    1 isoAddress
    2 cardNumber
    3 level
    """
    def getShopCardSlots(self):
        shopCardsList = list()

        for row in self.cursor.execute("SELECT * FROM shopCards"):
            slot = entities.ShopCardSlot(row[0], row[1], row[2], row[3])
            shopCardsList.append(slot)
        return shopCardsList
    #endregion

    #bonus draw
    #region 
    """
    0 id
    1 isoAddress
    2 cardNumber
    3 level
    """
    def getBonusDrawCards(self):
        bonusCardsList = list()

        for row in self.cursor.execute("SELECT * FROM bonusDrawCards"):
            slot = entities.BonusDrawCardSlot(row[0], row[1], row[2], row[3])
            bonusCardsList.append(slot)
        return bonusCardsList
    #endregion

