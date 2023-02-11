import os
import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from unicodedata import category
from LK2Randomizer import Constants
from entities import MainScreenTkVars, CardCheckbuttonVars, CategoryCheckbuttonVars
from randomizer import Randomizer, SeedGenerator
from dataAccess import DBConnection

class MainScreen:

    def __init__(self):
        rootWindow = self.makeRootWindow()
        self.tkVars = MainScreenTkVars()
        self.setInitialSeed()
        cardChkVars = self.setUpCardCheckbuttons() #list of CardCheckbuttonPair
        categoryChkVars = self.setUpCategoryCheckbuttons() # list of 
        self.makeFrames(rootWindow, cardChkVars, categoryChkVars)
        rootWindow.mainloop()

    def makeRootWindow(self):
        rootWindow = tk.Tk()
        rootWindow.resizable('false', 'false')
        rootWindow.title(Constants.versionName)
        return rootWindow     

    def setInitialSeed(self):
        seed = SeedGenerator().getSeed()
        self.tkVars.seedEntryText.set(seed)

    def setUpCardCheckbuttons(self):
        db = DBConnection()
        cardList = db.getAllCards()
        cardChkVars = list()
        for card in cardList:
            cardChkVars.append(CardCheckbuttonVars(card, True))
        return cardChkVars    

    def setUpCategoryCheckbuttons(self):
        categoryChkVars = list()
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Fire'))
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Water'))
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Earth'))
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Wood'))
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Neutral'))
        categoryChkVars.append(CategoryCheckbuttonVars('element', 'Mech'))
        categoryChkVars.append(CategoryCheckbuttonVars('type', 'Independent'))
        categoryChkVars.append(CategoryCheckbuttonVars('type', 'Helper'))
        categoryChkVars.append(CategoryCheckbuttonVars('type', 'Weapon'))
        categoryChkVars.append(CategoryCheckbuttonVars('type', 'Summons'))
        categoryChkVars.append(CategoryCheckbuttonVars('type', 'Transform'))
        return categoryChkVars

    def makeFrames(self, rootWindow, cardChkVars, categoryChkVars):
        #selectFrame
        selectFrame = tk.Frame(rootWindow, bd=10)
        selectFrame.pack()

        savedFilePath = Utility.loadSavedFilePath()
        self.tkVars.selectISOText.set(savedFilePath)
        selectISOEntry = tk.Entry(selectFrame, width=48, textvariable=self.tkVars.selectISOText)
        selectISOEntry.pack(side='left')

        selectISObtn = tk.Button(selectFrame, text='Select .iso', command=lambda: self.selectISObtn_OnClick())
        selectISObtn.pack(side='left')

        #cardsFrame
        cardsFrame = tk.Frame(rootWindow, bd=10)
        cardsFrame.pack()
        
        editCardPoolBtn = tk.Button(cardsFrame, text='Edit Card Pool', command=lambda: self.editCardPool_OnClick(rootWindow, cardChkVars, categoryChkVars))
        useAllCardsChk = tk.Checkbutton(cardsFrame, text='Use all cards?', variable=self.tkVars.useAllCards, command=lambda: self.useAllCards_Changed(editCardPoolBtn))
        useAllCardsChk.select()

        useAllCardsChk.pack()

        #seedFrame
        seedFrame = tk.Frame(rootWindow, bd=10)
        seedFrame.pack()

        seedLabel = tk.Label(seedFrame, text='Seed')
        seedLabel.pack(side='left')

        seedEntry = tk.Entry(seedFrame, textvariable=self.tkVars.seedEntryText)
        seedEntry.pack(side='left')

        #goFrame
        goFrame = tk.Frame(rootWindow, bd=10)
        goFrame.pack()
        
        generateIsoChk = tk.Checkbutton(goFrame, text='Generate .iso', variable=self.tkVars.genIsoSelected)
        generateIsoChk.select()
        generateIsoChk.pack()

        self.submitButton = tk.Button(goFrame, text='Start Randomization', bg='#4caf50', activebackground='#ffeb3b', command=lambda: self.startRandomization_OnClick(cardChkVars))
        self.submitButton.pack()

    def convertCardData(self, cardChkVars):
        cardChkValues = list()
        for cardChk in cardChkVars:
            newPair = CardCheckbuttonVars(cardChk.card, cardChk.cardSelected.get())
            newPair.cardSelected = newPair.cardSelected.get()
            cardChkValues.append(newPair)
        return cardChkValues
    
    def convertTkVarsToData(self, tkVars):
        '''
        Converts entity object of tk.Vars
        to dictionary with raw data values
        '''
        dataDict = tkVars.__dict__.copy()
        for key, value in dataDict.items():
            dataDict[key] = value.get()
        return dataDict

    def countCardsSelected(self, cardChkVars):
        cardCount = 0
        for cardChk in cardChkVars:
            if cardChk.cardSelected.get():
                cardCount = cardCount + 1
        return cardCount

    #ShowMessage
    #region 
    def showSeedAlphaErrorMessage(self):
        messagebox.showerror('Bad Seed', 'The seed must be alphanumeric. No punctuation or symbols.')

    def showISOErrorMessage(self):
        messagebox.showerror('File Error', 'Please choose an uncompressed Lost Kingdoms II .iso (USA 1.35 GB)')
        
    def showDoneMessage(self):
        doneMessage = 'The patched .iso + log is ready.'
        if not self.tkVars.genIsoSelected.get(): #no iso
            doneMessage = 'The log is ready.'
        messagebox.showinfo('Done', doneMessage)

    def showRandomizeErrorMessage(self):
        messagebox.showerror('Application Error', 'Something went wrong with randomization.')
        messagebox.showerror()

    def showNoCardsSelectedMessage(self):
        messagebox.showerror('Selection Error', 'You need to select at least one card, dummy.')
    #endregion

    #events
    #region
    def selectISObtn_OnClick(self):
        #browse for .iso file
        filename = fdialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('ISO files', '*.iso'), ('all files', '*.*')))
        self.tkVars.selectISOText.set(filename)

    def startRandomization_OnClick(self, cardChkVars):
        try:
            # test for good .iso Path
            if not Utility.checkForGoodISO(self.tkVars.selectISOText.get()): 
                raise IOError
            seedString = self.tkVars.seedEntryText.get()
            if not seedString.isalnum():  # is seed alpha-numeric?
                raise ValueError
            if self.tkVars.useAllCards.get() is False: #using selected cards
                if self.countCardsSelected(cardChkVars) == 0: #no cards selected
                    raise Exception
        except IOError:
            self.showISOErrorMessage()
        except ValueError:
            self.showSeedAlphaErrorMessage()
        except Exception:
            self.showNoCardsSelectedMessage()
        else:  #good .iso
            randomizer = Randomizer()
            formDataDict = self.convertTkVarsToData(self.tkVars)
            #check if we're using all cards
            if self.tkVars.useAllCards.get() is False:
                cardSelectionList = self.convertCardData(cardChkVars)
            else:
                cardSelectionList = False
            try:
                if not randomizer.doRandomization(formDataDict, cardSelectionList):
                    raise IOError
            except IOError:
                self.showRandomizeErrorMessage()
            else: #success
                Utility.saveFilePath(formDataDict["selectISOText"])
                self.showDoneMessage()

    def useAllCards_Changed(self, editCardPoolBtn):
        if self.tkVars.useAllCards.get() is True:
            editCardPoolBtn.pack_forget()
        else:
            editCardPoolBtn.pack()

    def editCardPool_OnClick(self, rootWindow, cardChkVars, categoryChkVars):
        CardScreen(rootWindow, cardChkVars, categoryChkVars)
    #endregion


class CardScreen():
    def __init__(self, rootWindow, cardChkVars, categoryChkVars):
        cardWindow = tk.Toplevel(rootWindow)
        cardWindow.geometry("600x600")
        cardWindow.title('Card Pool')
        cardWindow.resizable('true', 'true')
        mainFrame = tk.Frame(cardWindow)
        mainFrame.pack(side='left')
        myCanvas = tk.Canvas(mainFrame, height=600, width=580)
        myCanvas.pack(side='left')
        scrollbar = ttk.Scrollbar(mainFrame, orient='vertical', command=myCanvas.yview)
        scrollbar.pack(side='left', fill='y')
        myCanvas.configure(yscrollcommand=scrollbar.set)
        myCanvas.bind("<Configure>",lambda e: myCanvas.config(scrollregion= myCanvas.bbox('all')))
        second_frame = tk.Frame(myCanvas)
        myCanvas.create_window((0,0),window= second_frame, anchor='n')
        self.makeCheckBoxes(second_frame, cardChkVars, categoryChkVars)

    def makeCheckBoxes(self, frame, cardChkVars, categoryChkVars):
        self.makeCategoryChecks(frame, cardChkVars, categoryChkVars)
        for cardChk in cardChkVars:
            checkText = str(cardChk.card.number) + ' ' + cardChk.card.name
            tk.Checkbutton(frame, text=checkText, variable=cardChk.cardSelected).grid(column=1, columnspan=6, padx=30, sticky='w')

    def makeCategoryChecks(self, frame, cardChkVars, categoryChkVars):
        col = 0
        col2 = 0
        for categoryChk in categoryChkVars:
            if categoryChk.field == 'element':
                col += 1
                rw = 1
            elif categoryChk.field == 'type':
                col2 += 1
                col = col2
                rw = 2
            cb = tk.Checkbutton(frame, text=categoryChk.category, variable=categoryChk.categorySelected)
            cb.config(command=lambda: self.categoryChecked(cardChkVars, categoryChkVars))
            cb.grid(column=col, row=rw, padx=5)

    def categoryChecked(self, cardChkVars, categoryChkVars):
        #start with all cards checked
        for cardChk in cardChkVars:
            cardChk.cardSelected.set(True)
        #look for unchecked categories
        for categoryChk in categoryChkVars:
            if categoryChk.categorySelected.get() is False:
                #set cards that match that category to false
                for cardChk in cardChkVars:
                    if categoryChk.field == 'element':
                        if cardChk.card.element == categoryChk.category: #card element is unchecked element
                            cardChk.cardSelected.set(False)
                    elif categoryChk.field == 'type':
                        if cardChk.card.type_ == categoryChk.category: #card type is unchecked type
                            cardChk.cardSelected.set(False)


class Utility:
    #def __init__(self):
    #    pass
    def checkForGoodISO(ISOPath):
        goodISO = True
        if not ISOPath.endswith('.iso'):
            goodISO = False
        if os.path.getsize(ISOPath) != Constants.isoSize:
            goodISO = False
        with open(ISOPath, 'rb') as iso_file:
            if iso_file.read(6) != Constants.gameID:
                goodISO = False
        return goodISO

    def loadSavedFilePath():
        with open(Constants.savedPathFile, 'r') as file:
            savedPath = file.read()
        return savedPath

    def saveFilePath(isoPath):
        with open(Constants.savedPathFile, 'w') as file:
            file.write(isoPath)