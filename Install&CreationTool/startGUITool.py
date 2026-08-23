from guizero import *
import os
from tkinter import filedialog, Tk


def createDrive():
    driveMaker.visible = True
    def openSelect():
        Tk().withdraw()   # we don't want a full GUI, so keep the root window from appearing
        drivePath = select_folder()  # show an "Open" dialog box and return the path to the selected drive
        print("Drive: " + drivePath)
        print(os.listdir(drivePath))
    PushButton(driveMaker, text="Select Drive Root", command=openSelect, grid=[0,0])
    # User writes .ini file
    iniFileTitleBox = TitleBox(driveMaker, "autorun.ini", grid=[0,1])
    iniFile = TextBox(iniFileTitleBox, text="[autorun]\nicon = (Icon file)\nlabel = (Drive Name Here)\nopen = start.bat",multiline=True, width=50, height=25)
    # User writes start.bat
    batFileTitleBox = TitleBox(driveMaker, "start.bat", grid=[1,1])
    batFile = TextBox(batFileTitleBox, text="start steam://run/400 -fullscreen (starts portal in fullscreen)\nexit",multiline=True, width=50, height=25)



app = App(title="Install & Creation Tool")
driveMaker = Window(app, title="Drive Maker", visible=False, layout="grid", width=640, height=360)
PushButton(app, text="Create Drive", command=createDrive)



app.display()