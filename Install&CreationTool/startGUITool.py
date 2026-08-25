from libraries.guizero import *
from tkinter import Tk, Message
from tkinter.filedialog import *
import os
import hashlib

def createDrive():
    global securityCode, iniFile, batFile
    driveMaker.visible = True
    def openSelectDriveRoot():
        global drivePath
        Tk().withdraw()   # we don't want a full GUI, so keep the root window from appearing
        drivePath = select_folder()  # show an "Open" dialog box and return the path to the selected drive
        print("Drive: " + drivePath)
        print(os.listdir(drivePath))
    def selectIcon():
        Tk().withdraw()
        iconFile = askopenfilename(defaultextension=".ico", title="Select Icon - Drive Flash Utility")
        print("Icon: " + iconFile)
    PushButton(driveMaker, text="Select Drive Root", command=openSelectDriveRoot, grid=[0,0])
    # User writes .ini file
    iniFileTitleBox = TitleBox(driveMaker, "autorun.inf", grid=[0,1])
    iniFile = TextBox(iniFileTitleBox, text="[autorun]\n"
                                            "icon = autorun.ico\n"
                                            "label = (Drive Name Here)\n"
                                            "open = start.bat", multiline=True, width=55, height=15)

    # User writes start.bat
    batFileTitleBox = TitleBox(driveMaker, "start.bat", grid=[1,1])
    Text(batFileTitleBox, "Enter CMD commands here, separated with a newline")
    batFile = TextBox(batFileTitleBox, text="start steam://run/400 -fullscreen\n"
                                            "exit",multiline=True, width=55, height=15)

    # User inputs security code
    securityCodeBox = TitleBox(driveMaker, "Trust Password", grid=[0, 2])
    securityCode = TextBox(securityCodeBox, text="", hide_text=True, width=10, height=1, command=hashIT)
    # Add Icon
    PushButton(driveMaker, text="Select Icon (.ico)", command=selectIcon, grid=[1,0])
    # Flash
    PushButton(driveMaker, text="Flash", command=flashDrive, grid=[1,2])

def hashIT():
    global h
    password = securityCode.value
    h = hashlib.new('sha256', usedforsecurity=True)
    h.update(bytes(password, "utf-8"))
def flashDrive():
    os.chdir(drivePath)
    with open("autorun.inf", "w") as f:
        f.write(iniFile.value)
        f.close()
    with open("start.bat", "w") as f:
        f.write(batFile.value)
        f.close()
    with open("trust.txt", "w") as f:
        f.write(h.hexdigest())
        f.close()
    driveMaker.info(title="Drive Flash Utility", text="Drive was flashed successfully, to apply changes unplug your drive and plug it back in.")
    os.chdir("C:\\")
app = App(title="Install & Creation Tool")
driveMaker = Window(app, title="Drive Flash Utility", visible=False, layout="grid", width=660, height=370)
PushButton(app, text="Create Drive", command=createDrive)



app.display()