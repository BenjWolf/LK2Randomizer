import tkinter as tk

class Card:
    """
    number (int)
    name (str)
    hexCode (byte)
    rarity (int): 1 through 8
    isKeyCard (int): 0 or 1
    """
    def __init__(self, number, name, hexCode, rarity, isKeyCard):
        self.number = number
        self.name = name
        hexCode = str(hexCode) #make sure it's string
        hexCode = int(hexCode, 16) #convert to int, base 16
        self.hexCode = hexCode.to_bytes(1, byteorder='big') #translate to byte
        self.rarity = rarity
        self.isKeyCard = isKeyCard

class Location:
    """
    A location is a chest, quest, or npc
    id (int)
    name (string)
    level (string)
    originalCardNum (int)
    isoAddress (byte)
    missable (int) 0 or 1
    """
    def __init__(self, id, name, level, originalCardNum, isoAddress, missable):
        self.id = id
        self.name = name
        self.level = level
        self.originalCardNum = originalCardNum
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.missable = missable

class MainScreenTkVars:
    def __init__(self):
        self.selectISOText = tk.StringVar()
        self.seedEntryText = tk.StringVar()
        self.genIsoSelected = tk.BooleanVar()



