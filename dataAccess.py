import sqlite3
import entities
from LK2Randomizer import Constants

class DBConnection:
    def __init__(self):
        self.connection = sqlite3.connect(Constants.dbPath)
        self.cursor = self.connection.cursor()
    
    #card queries
    #region 
    """
    0 number
    1 name
    2 hexCode
    3 rarity
    4 isKeyCard
    5 isShopCard
    6 element
    7 type
    """
    def getCardByNumber(self, number):
        result = self.cursor.execute(f"SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type FROM cards WHERE number = {number}")
        row = result.fetchone()
        card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return card

    def getAllCards(self):
        cardList = list()

        for row in self.cursor.execute("SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type FROM cards"):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cardList.append(card)
        return cardList

    #def getAllNonKeyCards(self):
    #    cardList = list()

    #    for row in self.cursor.execute("SELECT number, name, hexCode, rarity, isKeyCard, isShopCard FROM cards WHERE isKeyCard = 0"):
    #        card = entities.Card(row[0], row[1], row[2], row[3])
    #        cardList.append(card)
    #    return cardList
    #endregion
    
    #cardPool
    #region
    '''
    0 cardNumber
    '''
    def setAllCardsInPool(self):
        self.clearCardPool()
        self.cursor.execute("""
        INSERT INTO cardPool (cardNumber)
        SELECT number FROM cards
        """)
        self.connection.commit()

    def setCardPool(self, cardNumbers):
        self.clearCardPool()
        for num in cardNumbers:
            self.cursor.execute(f"INSERT INTO cardPool (cardNumber) VALUES ({num})")
        self.connection.commit()


    def clearCardPool(self):
        self.cursor.execute("DELETE FROM cardPool")
        self.connection.commit()

    def getCardsFromPool(self):
        cardList = list()
        for row in self.cursor.execute("""
        SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type 
        FROM cards c
        JOIN cardPool cp on cp.cardNumber = c.number
        """):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cardList.append(card)
        return cardList

    def getShopCardsFromPool(self):
        cardList = list()

        for row in self.cursor.execute("""
        SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type 
        FROM cards c
        JOIN cardPool cp on cp.cardNumber = c.number
        WHERE c.isShopCard = 1
        """):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cardList.append(card)
        return cardList
    
    def getCardsFromPoolByRarity(self, rarity):
        cardList = list()
                
        for row in self.cursor.execute(f"""
        SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type 
        FROM cards c
        JOIN cardPool cp on cp.cardNumber = c.number
        WHERE c.rarity = {rarity}
        """):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cardList.append(card)
        return cardList

    def getShopCardsFromPoolByRarity(self, rarity):
        cardList = list()
                
        for row in self.cursor.execute(f"""
        SELECT number, name, hexCode, rarity, isKeyCard, isShopCard, element, type 
        FROM cards c
        JOIN cardPool cp on cp.cardNumber = c.number
        WHERE c.rarity = {rarity}
        AND c.isShopCard = 1
        """):
            card = entities.Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cardList.append(card)
        return cardList
    #endregion
    #starting deck
    #region 
    """
    0 id
    1 isoAddress
    2 cardNumber
    3 cardGroup
    4 rarity
    """
    def getStartingDeck(self):
        startingDeckList = list()

        for row in self.cursor.execute("""
        SELECT id, isoAddress, cardNumber, cardGroup, rarity FROM startingDeck
        JOIN cards on cardNumber = number
        """):
            slot = entities.StartingDeckSlot(row[0], row[1], row[2], row[3], row[4])
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
    5 rarity
    6 isKeyCard
    """
    def getAllLocations(self):
        locationList = list()
        
        for row in self.cursor.execute("""
        SELECT l.id, l.name, l.level, l.cardNumber, l.isoAddress, c.rarity, c.isKeyCard
        FROM location l
        JOIN cards c on l.cardNumber = c.number
        """):
            location = entities.CardLocation(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
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
    4 rarity
    """
    def getShopCardSlots(self):
        shopCardsList = list()

        for row in self.cursor.execute("""
        SELECT id, isoAddress, cardNumber, level, rarity 
        FROM shopCards
        JOIN cards on cardNumber = number
        """):
            slot = entities.ShopCardSlot(row[0], row[1], row[2], row[3], row[4])
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
    4 cardGroup
    5 rarity
    """
    def getBonusDrawCards(self):
        bonusCardsList = list()

        for row in self.cursor.execute("""
        SELECT id, isoAddress, cardNumber, level, cardGroup, rarity 
        FROM bonusDrawCards
        JOIN cards on cardNumber = number
        """):
            slot = entities.BonusDrawCardSlot(row[0], row[1], row[2], row[3], row[4], row[5])
            bonusCardsList.append(slot)
        return bonusCardsList
    #endregion
