import tkinter as tk

class Card:
    """
    number (int)
    name (str)
    hexCode (byte)
    rarity (int): 1 through 8
    isKeyCard (bool)
    isShopCard (bool)
    element (string) Fire, Water, Earth, Wood, Neutral, Mech
    type_ (string) Independent, Helper, Weapon, Summons, Transform
    """
    def __init__(self, number, name, hexCode, rarity, isKeyCard, isShopCard, element, type_):
        self.number = number
        self.name = name
        hexCode = str(hexCode) #make sure it's string
        hexCode = int(hexCode, 16) #convert to int, base 16
        self.hexCode = hexCode.to_bytes(1, byteorder='big') #translate to byte
        self.rarity = rarity
        if isKeyCard == 0:
            self.isKeyCard = False
        else:
            self.isKeyCard = True
        if isShopCard == 0:
            self.isShopCard = False
        else:
            self.isShopCard = True
        self.element = element
        self.type_ = type_


class StartingDeckSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    cardGroup (int)
    rarity (int)
    """
    def __init__(self, id, isoAddress, cardNumber, cardGroup, rarity):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber
        self.cardGroup = cardGroup
        self.rarity = rarity


class CardLocation:
    """
    A CardLocation is a chest, quest, or npc
    id (int)
    name (string)
    level (string)
    cardNumber (int)
    isoAddress (byte)
    rarity (int)
    isKeyCard (bool)
    """
    def __init__(self, id, name, level, cardNumber, isoAddress, rarity, isKeyCard):
        self.id = id
        self.name = name
        self.level = level
        self.cardNumber = cardNumber
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.rarity = rarity
        if isKeyCard == 0:
            self.isKeyCard = False
        else:
            self.isKeyCard = True

class ShopCardSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    level (string)
    rarity (int)
    """
    def __init__(self, id, isoAddress, cardNumber, level, rarity):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber
        self.level = level
        self.rarity = rarity

class BonusDrawCardSlot:
    """
    id (int)
    isoAddress (byte)
    cardNumber (int)
    level (string)
    cardGroup (int)
    """
    def __init__(self, id, isoAddress, cardNumber, level, cardGroup, rarity):
        self.id = id
        self.isoAddress = int(isoAddress,16) #convert to int, base 16
        self.cardNumber = cardNumber
        self.level = level
        self.cardGroup = cardGroup
        self.rarity = rarity

class MainScreenTkVars:
    def __init__(self):
        self.selectISOText = tk.StringVar()
        self.balancedRandomization = tk.BooleanVar(value=True)
        self.useAllCards = tk.BooleanVar(value=True)
        self.seedEntryText = tk.StringVar()
        self.genIsoSelected = tk.BooleanVar()

class CardCheckbuttonVars:
    def __init__(self, card, isSelected):
        self.card = card
        self.cardSelected = tk.BooleanVar()
        self.cardSelected.set(isSelected)

class CategoryCheckbuttonVars:
    def __init__(self, field, category):
        self.field = field
        self.category = category
        self.categorySelected = tk.BooleanVar(value=True)


