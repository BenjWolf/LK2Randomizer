import random
from dataAccess import DBConnection
from output import Output

class Randomizer:
    def __init__(self):
        self.connector = DBConnection()
        self.pairs = list()

    def doRandomization(self, formDataDict):
        self.locationRandomization()

        isoPath = formDataDict["selectISOText"]
        seed = formDataDict["seedEntryText"]
        genIsoBool = formDataDict["genIsoSelected"]

        out = Output()
        if not out.doOutput(isoPath, seed, genIsoBool, self.pairs):
            pass #throw exception
        return True

    def locationRandomization(self): #do not randomize key cards locations
        self.locationList = self.connector.getAllLocations()
        self.cardList = self.connector.getAllCards()
        for loc in self.locationList:
            if self.connector.checkKeyCardByNumber(loc.originalCardNum): #do not randomize
                card = self.connector.getCardByNumber(loc.originalCardNum)
                pair = Pairing(loc, card)
            else:
                card = random.choice(self.cardList)
                pair = Pairing(loc, card)

            self.pairs.append(pair)

class Pairing:
    '''
    location can be chest, quest, npc
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

