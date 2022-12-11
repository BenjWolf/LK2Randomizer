import time
import shutil
from LK2Randomizer import Constants

class Output:
    def __init__(self):
        pass

    def doOutput(self, isoPath, seed, genIsoBool, pairs):
        if genIsoBool:
            newISO = self.copyISO(isoPath, seed)
            self.writeToISO(newISO, pairs)
        self.writeToLog(seed, pairs)
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

    def writeToLog(self, seed, pairs):
        localTime = time.asctime(time.localtime(time.time()))
        logFile = 'log ' + seed + '.txt'
        with open(logFile, 'w') as log:
            log.write(Constants.versionName + '\n')
            log.write('Randomized on: ' + localTime + '\n')
            log.write('Seed: ' + seed + '\n\n')
            for pair in pairs:
                log.write(f"{pair.location.level} {pair.location.name} has {pair.item.name}\n")