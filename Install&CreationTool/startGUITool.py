from guizero import *
from tkinter import Tk
from tkinter.filedialog import *
import os
import hashlib
import win32api

nonNTFS = []
def createDrive():
    indexNonNTFSVolumes()
    global securityCode, iniFile, batFile
    app.visible = True
    def openSelectDriveRoot():
        global drivePath
        drivePath = driveIndex.value
    def selectIcon():
        Tk().withdraw()
        iconFile = askopenfilename(defaultextension=".ico", title="Select Icon - Drive Flash Utility")
        print("Icon: " + iconFile)
    # PushButton(driveMaker, text="Select Drive Root", command=openSelectDriveRoot, grid=[0,0])
    driveIndex = Combo(app, options=nonNTFS, grid=[0, 0], command=openSelectDriveRoot)
    # User writes .ini file
    iniFileTitleBox = TitleBox(app, "autorun.inf", grid=[0, 1])
    iniFile = TextBox(iniFileTitleBox, text="[autorun]\n"
                                            "icon = autorun.ico\n"
                                            "label = (Drive Name Here)\n"
                                            "open = start.bat", multiline=True, width=55, height=15)

    # User writes start.bat
    batFileTitleBox = TitleBox(app, "start.bat", grid=[1, 1])
    Text(batFileTitleBox, "Enter CMD commands here, separated with a newline")
    batFile = TextBox(batFileTitleBox, text="start steam://run/400 -fullscreen\n"
                                            "exit",multiline=True, width=55, height=15)

    # User inputs security code
    securityCodeBox = TitleBox(app, "Trust Password", grid=[0, 2])
    securityCode = TextBox(securityCodeBox, text="", hide_text=True, width=10, height=1, command=hashIT)
    # Add Icon
    PushButton(app, text="Select Icon (.ico)", command=selectIcon, grid=[1, 0])
    # Flash
    PushButton(app, text="Flash", command=flashDrive, grid=[1, 2])

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
    app.info(title="Drive Flash Utility", text="Drive was flashed successfully, to apply changes unplug your drive and plug it back in.")
    os.chdir("C:\\")
def indexNonNTFSVolumes():
    nonNTFS.clear()
    nonNTFS.insert(0, "Select Drive")
    drives = win32api.GetLogicalDriveStrings()
    dx = [x for x in drives.split("\000") if x]
    for drive in dx:
        try:
            vol_info = win32api.GetVolumeInformation(drive)
            if vol_info[4] != "NTFS":
                # Call GetVolumeInformation
                nonNTFS.append(drive)
                print(drive, vol_info[0], vol_info[4])
        except:
            print("Drive(s) found:")
app = App(title="Drive Flash Utility", layout="grid", width=700, height=400)
createDrive()
app.display()