import os
import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from LK2Randomizer import Constants
from entities import MainScreenTkVars, CardCheckbuttonPair
from randomizer import Randomizer, SeedGenerator
from dataAccess import DBConnection

class MainScreen:

    def __init__(self):
        rootWindow = self.makeRootWindow()
        self.tkVars = MainScreenTkVars()
        self.setInitialSeed()
        cardChkVars = self.setUpCardCheckbuttons() #list of CardCheckbuttonPair
        self.makeFrames(rootWindow, cardChkVars)
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
            cardChkVars.append(CardCheckbuttonPair(card, True))
        return cardChkVars    

    def makeFrames(self, rootWindow, cardChkVars):
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
        
        editCardPoolBtn = tk.Button(cardsFrame, text='Edit Card Pool', command=lambda: self.editCardPool_OnClick(rootWindow, cardChkVars))
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
            newPair = CardCheckbuttonPair(cardChk.card, cardChk.cardSelected.get())
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

    def editCardPool_OnClick(self, rootWindow, cardChkVars):
        CardScreen(rootWindow, cardChkVars)
    #endregion

class CardScreen():
    def __init__(self, rootWindow, cardChkVars):
        cardWindow = tk.Toplevel(rootWindow)
        cardWindow.geometry("300x600")
        cardWindow.title('Card Pool')
        cardWindow.resizable('false', 'false')
        mainFrame = tk.Frame(cardWindow)
        mainFrame.pack(side='left')
        myCanvas = tk.Canvas(mainFrame, height=600, width=280)
        myCanvas.pack(side='left')
        scrollbar = ttk.Scrollbar(mainFrame, orient='vertical', command=myCanvas.yview)
        scrollbar.pack(side='left', fill='y')
        myCanvas.configure(yscrollcommand=scrollbar.set)
        myCanvas.bind("<Configure>",lambda e: myCanvas.config(scrollregion= myCanvas.bbox('all')))
        second_frame = tk.Frame(myCanvas)
        myCanvas.create_window((0,0),window= second_frame, anchor='n')
        self.makeCheckBoxes(second_frame, cardChkVars)

    def makeCheckBoxes(self, frame, cardChkVars):
        for pair in cardChkVars:
            checkText = str(pair.card.number) + ' ' + pair.card.name
            tk.Checkbutton(frame, text=checkText, variable=pair.cardSelected).grid(column=1, padx=30, sticky='w')

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