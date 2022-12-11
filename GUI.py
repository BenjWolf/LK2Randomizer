import tkinter as tk
import tkinter.filedialog as fdialog
from LK2Randomizer import Constants
from entities import MainScreenTkVars
from randomizer import Randomizer, SeedGenerator


#import entities

class MainScreen:

    def __init__(self):
        rootWindow = self.makeRootWindow()
        self.tkVars = MainScreenTkVars()
        self.setInitialSeed()
        self.makeFrames(rootWindow)
        rootWindow.mainloop()

    def makeRootWindow(self):
        rootWindow = tk.Tk()
        rootWindow.resizable('false', 'false')
        rootWindow.title(Constants.versionName)
        return rootWindow     

    def setInitialSeed(self):
        seed = SeedGenerator().getSeed()
        self.tkVars.seedEntryText.set(seed)

    def makeFrames(self, rootWindow):
        frame = tk.Frame(rootWindow, bd=10)
        frame.pack()

        savedFilePath = Utility.loadSavedFilePath()
        self.tkVars.selectISOText.set(savedFilePath)
        selectISOEntry = tk.Entry(frame, width=48, textvariable=self.tkVars.selectISOText)
        selectISOEntry.pack(side='left')

        selectISObtn = tk.Button(frame, text='Select .iso', command=lambda: self.selectISObtn_OnClick())
        selectISObtn.pack(side='left')

        frame2 = tk.Frame(rootWindow, bd=10)
        frame2.pack()

        seedLabel = tk.Label(frame2, text='Seed')
        seedLabel.pack(side='left')

        seedEntry = tk.Entry(frame2, textvariable=self.tkVars.seedEntryText)
        seedEntry.pack(side='left')

        frame3 = tk.Frame(rootWindow, bd=10)
        frame3.pack()
        
        generateIsoChk = tk.Checkbutton(frame3, text='Generate .iso', variable=self.tkVars.genIsoSelected)
        generateIsoChk.select()
        generateIsoChk.pack()

        submitButton = tk.Button(frame3, text='Start Randomization', command=lambda: self.startRandomization_OnClick())
        submitButton.pack()

    def selectISObtn_OnClick(self):
        #browse for .iso file
        filename = fdialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('ISO files', '*.iso'), ('all files', '*.*')))
        self.tkVars.selectISOText.set(filename)

    def startRandomization_OnClick(self):
        formDataDict = Utility().convertTkVarsToData(self.tkVars)
        randomizer = Randomizer()
        if not randomizer.doRandomization(formDataDict):
            pass #throw exception
        Utility.saveFilePath(formDataDict["selectISOText"])
        print("done")
        

class Utility:
    #def __init__(self):
    #    pass

    def convertTkVarsToData(self, tkVars):
        '''
        Converts entity object of tk.Vars
        to dictionary with raw data values
        '''
        formDataDict = tkVars.__dict__.copy()
        for key, value in formDataDict.items():
            formDataDict[key] = value.get()
        return formDataDict

    def loadSavedFilePath():
        with open(Constants.savedPathFile, 'r') as file:
            savedPath = file.read()
        return savedPath

    def saveFilePath(isoPath):
        with open(Constants.savedPathFile, 'w') as file:
            file.write(isoPath)