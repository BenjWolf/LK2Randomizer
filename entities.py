import tkinter as tk

class Card:
    """
    number (int)
    name (str)
    hexCode (byte)
    rarity (int): 1 through 8
    """
    def __init__(self, number, name, hexCode, rarity):
        self.number = number
        self.name = name
        hexCode = str(hexCode) #make sure it's string
        hexCode = int(hexCode, 16) #convert to int, base 16
        self.hexCode = hexCode.to_bytes(1, byteorder='big') #translate to byte
        self.rarity = rarity

class StartingDeckSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    """
    def __init__(self, id, isoAddress, cardNumber):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber


class CardLocation:
    """
    A CardLocation is a chest, quest, or npc
    id (int)
    name (string)
    level (string)
    cardNumber (int)
    isoAddress (byte)
    """
    def __init__(self, id, name, level, cardNumber, isoAddress):
        self.id = id
        self.name = name
        self.level = level
        self.cardNumber = cardNumber
        self.isoAddress = int(isoAddress,16) #convert to int, base 16

class ShopCardSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    level (string)
    """
    def __init__(self, id, isoAddress, cardNumber, level):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber
        self.level = level

class BonusDrawCardSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    level (string)
    """
    def __init__(self, id, isoAddress, cardNumber, level):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber
        self.level = level

class MainScreenTkVars:
    def __init__(self):
        self.selectISOText = tk.StringVar()
        self.seedEntryText = tk.StringVar()
        self.genIsoSelected = tk.BooleanVar()



