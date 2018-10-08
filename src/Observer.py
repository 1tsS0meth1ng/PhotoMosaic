from src.GeneticProgram import GeneticProgram
from src.ImagePool import ImagePool
from tkinter import *
from PIL import ImageTk
from decimal import Decimal
import tkinter as tk


class View:

    image = None
    root = None
    panel = None
    startStopButton = None
    mutationPercent = None
    crossOverChance = None
    genePoolSize = None
    tournamentSize = None
    maxAmountOfGenerations = None
    saveBtn = None
    imageName = None
    selectionType = 0
    SELECTION_TYPES = [("tournament", 0), ("Roulette", 1)]
    IMAGESIZE = 500

    def __init__(self):
        imagePool = ImagePool()
        self.image = imagePool._originalImage
        self.genetic = GeneticProgram(self)

    def update(self, arg):
        self.image.close()
        self.image = arg
        reMg= self.fiximage(self.image, self.IMAGESIZE)
        imageUpd = ImageTk.PhotoImage(reMg)
        self.panel.configure(image=imageUpd)
        self.panel.image = imageUpd

    def enableAll(self):
        self.tournamentSize['state'] = NORMAL
        self.genePoolSize['state'] = NORMAL
        self.mutationPercent['state'] = NORMAL
        self.crossOverChance['state'] = NORMAL
        self.maxAmountOfGenerations['state'] = NORMAL

    def disableAll(self):
        self.tournamentSize['state'] = DISABLED
        self.genePoolSize['state'] = DISABLED
        self.mutationPercent['state'] = DISABLED
        self.crossOverChance['state'] = DISABLED
        self.maxAmountOfGenerations['state'] = DISABLED

    def startGenetic(self):
        self.startStopButton.configure(text="Stop")
        self.startStopButton.configure(command=self.genetic.stop)
        self.genetic.selectionType = self.selectionType
        self.genetic.tournamentSize = int(self.tournamentSize.get())
        self.genetic.genePoolSize = int(self.genePoolSize.get())
        self.genetic.mutationChancePercent = Decimal(self.mutationPercent.get())
        self.genetic.crossOverChance = Decimal(self.crossOverChance.get())
        self.genetic.maximumAmountOfGenerations = int(self.maxAmountOfGenerations.get())

        self.disableAll()

        self.genetic.start()

    def enableSave(self):
        self.saveBtn["state"]=NORMAL

    def setSelection(self,val):
        self.selectionType=val
        if(val!=0):
            self.tournamentSize['state'] = DISABLED
        else:
            self.tournamentSize['state']=NORMAL

        print(self.selectionType)


    def run(self):
        self.root = Tk()
        topFrame = Frame(self.root)
        topFrame.pack(side="top")

        bottomFrame= Frame(self.root)
        bottomFrame.pack(side="bottom")

        self.startStopButton=Button(topFrame, text='Start', command=self.startGenetic)
        self.startStopButton.grid(column=0,row=0, columnspan=5)

        tk.Radiobutton(topFrame,
                       text=self.SELECTION_TYPES[0][0],
                       padx=20,
                       variable=self.selectionType,
                       value=0,
                       command=lambda :self.setSelection(0)).grid(column=0,row=1)

        tk.Radiobutton(topFrame,
                       text=self.SELECTION_TYPES[1][0],
                       padx=20,
                       variable=self.selectionType,
                       value=1,
                       command=lambda :self.setSelection(1)).grid(column=0,row=2)

        tk.Label(topFrame,text="Genepool Size").grid(column=1,row=2)
        self.genePoolSize = Entry(topFrame)
        self.genePoolSize.grid(column=2,row=2)
        self.genePoolSize.insert(1,"40")

        tk.Label(topFrame,text="Chance of mutation [0-1]").grid(column=3,row=1)
        self.mutationPercent= Entry(topFrame)
        self.mutationPercent.grid(column=4,row=1)
        self.mutationPercent.insert(2,"0.1")

        tk.Label(topFrame, text="tournament size").grid(column=1, row=1)
        self.tournamentSize = Entry(topFrame)
        self.tournamentSize.grid(column=2, row=1)
        self.tournamentSize.insert(0, "5")

        tk.Label(topFrame,text="cross over chance [0-1]").grid(column=3,row=2)
        self.crossOverChance= Entry(topFrame)
        self.crossOverChance.grid(column=4,row=2)
        self.crossOverChance.insert(3,"0.9")

        tk.Label(topFrame,text="maximum generations (if 0 will runtill told to stop)").grid(row=3,column=1)
        self.maxAmountOfGenerations=Entry(topFrame)
        self.maxAmountOfGenerations.grid(row=3,column=2)
        self.maxAmountOfGenerations.insert(4,"0")

        self.saveBtn = Button(bottomFrame, text="Save Picture", state=DISABLED, command=self.saveImage)
        self.saveBtn.pack(side="bottom")

        reImg = self.fiximage(self.image, self.IMAGESIZE)
        img = ImageTk.PhotoImage(reImg)
        self.panel = tk.Label(bottomFrame, image=img)
        self.panel.pack(side="bottom", fill="both", expand="yes")

        self.root.mainloop()

    def fiximage(self, img, n):
        print(img.size)
        nwImg= None
        if img.size[0] >= img.size[1]:
            wpercent = (n / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            nwImg = img.resize((n, hsize))
        else:
            hpercent = (n / float(img.size[1]))
            wsize = int((float(img.size[1]) * float(hpercent)))
            nwImg = img.resize((wsize, n))
        return nwImg

    def saveImage(self):
        toplevel = Toplevel()
        Label(toplevel, text="give the picture a name (end it with .jpg)", height=0, width=100).pack()
        imageName = Entry(toplevel)
        imageName.pack()
        Button(toplevel, text="Save", command=lambda: self.saveCurrImage(imageName.get(), toplevel)).pack()

    def saveCurrImage(self, imageName, topLevel):
        self.image.save(imageName, "JPEG")
        topLevel.destroy()
