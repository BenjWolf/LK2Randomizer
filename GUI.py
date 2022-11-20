import tkinter as tk
import tkinter.filedialog as fdialog
from seedGen import SeedGenerator
from LK2Randomizer import Constants

#import entities

class MainScreen:

    def __init__(self):
        #generate seed
        seed = SeedGenerator().getSeed()
        rootWindow = self.makeRootWindow()
        self.makeTkVars(seed)
        self.makeFrames(rootWindow)
        rootWindow.mainloop()

    def makeRootWindow(self):
        rootWindow = tk.Tk()
        rootWindow.resizable('false', 'false')
        rootWindow.title(Constants.versionName)
        return rootWindow

    def makeTkVars(self, seed):
        self.selectISOText = tk.StringVar()
        self.seedEntryText = tk.StringVar(value=seed)


    def makeFrames(self, rootWindow):
        frame = tk.Frame(rootWindow, bd=10)
        frame.pack()

        selectISOEntry = tk.Entry(frame, width=48, textvariable=self.selectISOText)
        selectISOEntry.pack(side='left')

        selectISObtn = tk.Button(frame, text='Select .iso', command=lambda: self.selectISObtn_OnClick())
        selectISObtn.pack(side='left')

        frame2 = tk.Frame(rootWindow, bd=10)
        frame2.pack()

        seedLabel = tk.Label(frame2, text='Seed')
        seedLabel.pack(side='left')

        seedEntry = tk.Entry(frame2, textvariable=self.seedEntryText)
        seedEntry.pack(side='left')

        frame3 = tk.Frame(rootWindow, bd=10)
        frame3.pack()

        submitButton = tk.Button(frame3, text='Start Randomization', command=lambda: self.startRandomization_OnClick())
        submitButton.pack(side='top')

    def selectISObtn_OnClick(self):
        #browse for .iso file
        filename = fdialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('ISO files', '*.iso'), ('all files', '*.*')))
        self.selectISOText.set(filename)

    def startRandomization_OnClick(self):
        pass