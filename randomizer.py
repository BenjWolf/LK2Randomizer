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

        #set card pool in db
        if formDataDict["useAllCards"]:
            db.setAllCardsInPool()
        else: #use cardSelectionList
            #build list of selected cards
            cardNumbers = list() #list of integers
            for selection in cardSelectionList:
                if selection.cardSelected is True:
                    cardNumbers.append(selection.card.number)
            #insert card pool in db
            db.setCardPool(cardNumbers)

        startingDeckPairs = list()
        cardLocationPairs = list()
        shopPairs = list()
        bonusDrawPairs = list()
        if formDataDict["balancedRandomization"]:
            self.balancedRandomization(db, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs)
        else: #no balance
            self.fullRandomization(db, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs)

        #prepare output
        out = Output()
        isoPath = formDataDict["selectISOText"]
        genIsoBool = formDataDict["genIsoSelected"]
        if not out.doOutput(isoPath, ourSeed, genIsoBool, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs):
            success = False
        return success
    
    #balanced
    #region
    def balancedRandomization(self, db, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs):
        cardDictByRarity = self.makeRarityDict(db, False)
        shopCardDictByRarity = self.makeRarityDict(db, True)

        self.startingDeckBalanced(db, cardDictByRarity, startingDeckPairs)
        self.cardLocationBalanced(db, cardDictByRarity, cardLocationPairs)
        self.shopBalanced(db, shopCardDictByRarity, shopPairs)
        self.bonusDrawBalanced(db, cardDictByRarity, bonusDrawPairs)

    def makeRarityDict(self, db, forShopCards):
        cardDictByRarity = dict() #key: rarity (int), value: cardList
        rarityList = [1, 2, 3, 4, 5, 6, 7, 8]
        
        #build rarity dictionary
        for rarity in rarityList:
            if not forShopCards:
                cardDictByRarity[rarity] = db.getCardsFromPoolByRarity(rarity)
            else:
                cardDictByRarity[rarity] = db.getShopCardsFromPoolByRarity(rarity)

        #loop through dict to make sure none are empty
        for rarity, cardList in cardDictByRarity.items():
            if len(cardList) is 0:
                #no cards with this rarity to choose from
                doneSearching = False
                #build list of lower rarities
                lowerRarityToSearchList = list()
                for r in rarityList:
                    if r < rarity:
                        lowerRarityToSearchList.append(r)
                
                #make sure you can go lower (not rarity 1)
                if len(lowerRarityToSearchList) > 0:
                    #start with closest lower rarity
                    lowerRarityToSearchList.reverse()
                    #loop through lower rarities
                    for lowerRarity in lowerRarityToSearchList:
                        lowerList = cardDictByRarity[lowerRarity]
                        #choose first one that has cards
                        if len(lowerList) > 0:
                            #assign cardList of lower rarity to this rarity
                            cardDictByRarity[rarity] = cardDictByRarity[lowerRarity]
                            #ready to check next rarity
                            doneSearching = True
                            break 

                if not doneSearching: 
                    #check higher rarity
                    #build list of higher rarities
                    higherRarityToSearchList = list()
                    for r in rarityList:
                        if r > rarity:
                            higherRarityToSearchList.append(r)

                    #make sure you can go higher (not rarity 8)
                    if len(higherRarityToSearchList) > 0:
                        #loop through higher rarities
                        for higherRarity in higherRarityToSearchList:
                            higherList = cardDictByRarity[higherRarity]
                            #choose first one that has cards
                            if len(higherList) > 0:
                                #assign cardList of higher rarity to this rarity
                                cardDictByRarity[rarity] = cardDictByRarity[higherRarity]
                                #ready to check next rarity
                                doneSearching = True
                                break 
                    if not doneSearching:
                        #no cards available at all - can happen with shop
                        skeletonCard = db.getCardByNumber(1)
                        skellyList = [skeletonCard]
                        cardDictByRarity[rarity] = skellyList
            #else has cards - we're good
        return cardDictByRarity

    def startingDeckBalanced(self, db, cardDictByRarity, startingDeckPairs):
        startingDeckList = db.getStartingDeck()
        currentGroup = 0
        for slot in startingDeckList:
            #use same card for same group
            if currentGroup is not slot.cardGroup:
                #start of new group
                currentGroup = slot.cardGroup
                cardList = cardDictByRarity[slot.rarity]
                card = random.choice(cardList)
            pair = Pairing(slot, card)
            startingDeckPairs.append(pair)

    def cardLocationBalanced(self, db, cardDictByRarity, cardLocationPairs): 
        cardLocationList = db.getAllLocations()
        for loc in cardLocationList:
            if loc.isKeyCard: 
                #location has key card - do not randomize
                vanillaCard = db.getCardByNumber(loc.cardNumber)
                pair = Pairing(loc, vanillaCard)
            else:
                cardList = cardDictByRarity[loc.rarity]
                card = random.choice(cardList)
                pair = Pairing(loc, card)
            cardLocationPairs.append(pair)

    def shopBalanced(self, db, shopCardDictByRarity, shopPairs):
        slotList = db.getShopCardSlots()
        for slot in slotList:
            cardList = shopCardDictByRarity[slot.rarity]
            card = random.choice(cardList)
            pair = Pairing(slot, card)
            shopPairs.append(pair)

    #todo
    def bonusDrawBalanced(self, db, cardDictByRarity, bonusDrawPairs):
        bonusList = db.getBonusDrawCards()
        currentGroup = 0
        for slot in bonusList:
            #use same card for same group
            if currentGroup is not slot.cardGroup:
                #start of new group
                currentGroup = slot.cardGroup
                cardList = cardDictByRarity[slot.rarity]
                card = random.choice(cardList)
            pair = Pairing(slot, card)
            bonusDrawPairs.append(pair)
    #endregion

    #fullRand
    #region
    def fullRandomization(self, db, startingDeckPairs, cardLocationPairs, shopPairs, bonusDrawPairs):
        cardList = db.getCardsFromPool()

        self.startingDeckRandomization(db, cardList, startingDeckPairs)
        self.cardLocationRandomization(db, cardList, cardLocationPairs)
        self.shopRandomization(db, shopPairs)
        self.bonusDrawRandomization(db, cardList, bonusDrawPairs)

    def startingDeckRandomization(self, db, cardList, startingDeckPairs):
        startingDeckList = db.getStartingDeck()
        for slot in startingDeckList:
            card = random.choice(cardList)
            pair = Pairing(slot, card)
            startingDeckPairs.append(pair)
            
    def cardLocationRandomization(self, db, cardList, cardLocationPairs): 
        cardLocationList = db.getAllLocations()
        for loc in cardLocationList:
            if loc.isKeyCard: 
                #location has key card - do not randomize
                vanillaCard = db.getCardByNumber(loc.cardNumber)
                pair = Pairing(loc, vanillaCard)
            else:
                card = random.choice(cardList)
                pair = Pairing(loc, card)
            cardLocationPairs.append(pair)

    def shopRandomization(self, db, shopPairs):
        #filter shop cards into new list
        shopCardList = list()
        shopCardList = db.getShopCardsFromPool()
        if len(shopCardList) is 0: #no shop cards available
            shopCardList.append(db.getCardByNumber(1)) #put in skeleton

        #pick random cards for slots
        slotList = db.getShopCardSlots()
        for slot in slotList:
            card = random.choice(shopCardList)
            pair = Pairing(slot, card)
            shopPairs.append(pair)

    def bonusDrawRandomization(self, db, cardList, bonusDrawPairs):
        bonusList = db.getBonusDrawCards()
        for slot in bonusList:
            card = random.choice(cardList)
            pair = Pairing(slot, card)
            bonusDrawPairs.append(pair)
    #endregion

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

