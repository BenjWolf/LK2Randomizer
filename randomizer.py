import random
from dataAccess import DBConnection
from output import Output

class Randomizer:
    def __init__(self):
        pass
    def doRandomization(self, formDataDict, cardSelectionList):
        db = DBConnection()
        success = True
        
        #set seed
        ourSeed = formDataDict["seedEntryText"]
        random.seed(ourSeed)
        
        if cardSelectionList: #has data
            cardList = list()
            for selection in cardSelectionList:
                if selection.cardSelected is True:
                    cardList.append(selection.card)
        else:
            cardList = db.getAllCards()

        #starting deck
        startingDeckPairs = self.startingDeckRandomization(db, cardList)

        #location
        cardLocationPairs = self.cardLocationRandomization(db, cardList)

        #shop
        shopPairs = self.shopRandomization(db, cardList)

        #bonus draw
        bonusDrawPairs = self.bonusDrawRandomization(db, cardList)

        #prepare output
        out = Output()
        isoPath = formDataDict["selectISOText"]
        genIsoBool = formDataDict["genIsoSelected"]
        if not out.doOutput(isoPath, ourSeed, genIsoBool, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs):
            success = False
        return success

    def startingDeckRandomization(self, db, cardList):
        startingDeckList = db.getStartingDeck()
        startingDeckPairs = list()
        for slot in startingDeckList:
            card = random.choice(cardList)
            pair = Pairing(slot, card)
            startingDeckPairs.append(pair)
        return startingDeckPairs

    def cardLocationRandomization(self, db, cardList): #do not randomize key cards locations
        cardLocationList = db.getAllLocations()
        cardLocationPairs = list()
        for loc in cardLocationList:
            vanillaCard = db.getCardByNumber(loc.cardNumber)
            if vanillaCard.isKeyCard: 
                #cardLocation has key card - do not randomize
                pair = Pairing(loc, vanillaCard)
            else:
                card = random.choice(cardList)
                pair = Pairing(loc, card)
            cardLocationPairs.append(pair)
        return cardLocationPairs

    def shopRandomization(self, db, cardList):
        #filter shop cards into new list
        shopCardList = list()
        for selectedCard in cardList:
            if selectedCard.isShopCard:
                shopCardList.append(selectedCard)
        #edge case
        if len(shopCardList) is 0: #no shop cards available
            shopCardList.append(db.getCardByNumber(1)) #put in skeleton

        #pick random cards for slots
        slotList = db.getShopCardSlots()
        shopPairs = list()
        for slot in slotList:
            card = random.choice(shopCardList)
            pair = Pairing(slot, card)
            shopPairs.append(pair)
        return shopPairs

    def bonusDrawRandomization(self, db, cardList):
        bonusList = db.getBonusDrawCards()
        bonusPairs = list()
        for slot in bonusList:
            card = random.choice(cardList)
            pair = Pairing(slot, card)
            bonusPairs.append(pair)
        return bonusPairs

class Pairing:
    '''
    location can be StartingDeckCard, CardLocation, ShopCard, BonusDrawCard
    item can be Card
    '''
    def __init__(self, location, item):
        self.location = location
        self.item = item

class SeedGenerator:

    def getSeed(self):
        seedLength = 8
        seedChars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T',
'U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
'v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
        seed = str()
        for x in range(seedLength):
            seed += random.choice(seedChars)
        return seed

