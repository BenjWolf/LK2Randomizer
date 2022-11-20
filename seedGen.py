from ast import Constant
import random
from LK2Randomizer import Constants


class SeedGenerator:

    def __init__(self):
        self.seedChars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T',
'U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
'v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

    def getSeed(self):
        seed = str()
        for x in range(Constants.seedLength):
            seed += random.choice(self.seedChars)
        return seed

