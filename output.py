import time
import shutil
from LK2Randomizer import Constants

class Output:
    def __init__(self):
        pass
    
    def doOutput(self, isoPath, seed, genIsoBool, startingDeckPairs, locationPairs, shopPairs, bonusDrawPairs):
        if genIsoBool:
            newISO = self.copyISO(isoPath, seed)
            self.writeToISO(newISO, startingDeckPairs)
            self.writeToISO(newISO, locationPairs)
            self.writeToISO(newISO, shopPairs)
            self.writeToISO(newISO, shopPairs)
            self.writeToISO(newISO, bonusDrawPairs)
        self.writeToLog(seed, startingDeckPairs, locationPairs, shopPairs, bonusDrawPairs)
        return True

    def copyISO(self, isoPath, seed):
        # make copy of .iso with filename @newISO
        newISO = 'Lost Kingdoms II Randomized ' + seed + '.iso'
        shutil.copy(isoPath, newISO)
        return newISO
        
    def writeToISO(self, iso, pairs):
        with open(iso, 'r+b') as iso_file:
            for pair in pairs:
                iso_file.seek(pair.location.isoAddress)
                iso_file.write(pair.item.hexCode)

    def writeToLog(self, seed, startingDeckPairs, locationPairs, shopPairs, bonusDrawPairs):
        localTime = time.asctime(time.localtime(time.time()))
        logFile = 'log ' + seed + '.txt'

        self.logHeader(logFile, localTime, seed)
        self.logStartingDeck(logFile, startingDeckPairs)
        self.logLocation(logFile, locationPairs)
        self.logShop(logFile, shopPairs)
        self.logBonusDraw(logFile, bonusDrawPairs)

    def logHeader(self, logFile, localTime, seed):
        with open(logFile, 'w') as log: #overwrite file first
            log.write(Constants.versionName + '\n')
            log.write('Randomized on: ' + localTime + '\n')
            log.write('Seed: ' + seed + '\n\n')

    def logStartingDeck(self, logFile, startingDeckPairs):
        with open(logFile, 'a') as log:
            log.write('Starting Deck:\n')
            for pair in startingDeckPairs:
                log.write(f"{pair.item.name}. ")
            log.write('\n\n')

    def logLocation(self, logFile, locationPairs):
        with open(logFile, 'a') as log:
            log.write('Cards from chests, quests, and npcs:\n')
            for pair in locationPairs:
                log.write(f"{pair.location.level} {pair.location.name} has {pair.item.name}\n")
            log.write('\n')

    def logShop(self, logFile, shopPairs):
        with open(logFile, 'a') as log:
            log.write('Shop cards:\n')
            n = 0
            for pair in shopPairs:
                if n % 10 == 0: #print level name
                    log.write(f"{pair.location.level}:\n\t")
                log.write(f"{pair.item.name}. ")
                n += 1
                if n % 10 == 0: # every tenth card start new line
                    log.write('\n')
            log.write('\n')

    def logBonusDraw(self, logFile, bonusDrawPairs):
        with open(logFile, 'a') as log:
            log.write('Bonus draw cards:\n')
            n = 0
            for pair in bonusDrawPairs:
                if n % 6 == 0: # level name
                    log.write(f"{pair.location.level}:\n\t")
                log.write(f"{pair.item.name}. ")
                n += 1
                if n % 6 == 0: # every sixth card start new line
                    log.write('\n')
            log.write('\n')