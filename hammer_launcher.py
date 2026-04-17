from tkinter import *  
import os
import sys
import getopt
import requests
import crossfiledialog
import time
import zipfile
import json
import webbrowser

''' TODO and ISSUES

-csgo wont be supported, sdk costs money

-allow setup hammer to update hammer++ automatically?

-portal 2 should be tested on non debian/ubuntu based distros. it only wants to compile if the maps are opened from the full debian-installation path rather than steam path.

-add subwindows to cancel installation if there is no internet connection and things like wine 9 cant be installed

-i dont imagine itll make a difference but testing on x11 should be done probably 

-make reset and delete hammer buttons do something

'''
#--------

''' games to add support to
half life source (might be easy if we snag the gameinfo? im guessing we can reuse hl1mp stuff but not sure)
left 4 dead
left 4 dead 2
'''



#vguititlebar = 1








#arguments
args = sys.argv[1:]
options = "hnsl:"
long_options = ["help", "novgui", "setup", "launch"]
try:
    arguments, values = getopt.getopt(args, options, long_options)
    for currentArg, currentVal in arguments:
        if currentArg in ("-h", "--help"):
            print("Help info goes here")
            sys.exit()
        elif currentArg in ("-n", "--novgui"):
            print("STUB!")
            #print("Disabling custom title bar...")
            #vguititlebar = 0
        elif currentArg in ("-s", "--setup"):
            print("STUB!")
        elif currentArg in ("-l", "--launch"):
            print("STUB!")
except getopt.error as err:
    print("Invalid argument!")
    sys.exit()

print("if youre opening this in the terminal because something went wrong, im sorry.")

settinguphammer = 0

homefolder = os.path.expanduser("~")
print(homefolder)
#check for config folder, if it doesnt exist, then make it dummy.
if os.path.exists(homefolder + "/.config/linuxhammerlauncher/") == False:
    os.mkdir(homefolder + "/.config/linuxhammerlauncher/")


 
'''
window creation
'''
#function needed for vgui titlebar
def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))



# create root window
root = Tk()
def mainwindow():
    for child in root.winfo_children():
        child.destroy()

    # root window title and dimension
    root.title("Linux Hammer Launcher")
    # Set geometry (widthxheight)
    root.minsize(250,200)
    # Set resizability (widthxheight)
    root.resizable(False, False)
    #set icon
    root.tk.call('wm','iconphoto',root._w, Image("photo", file="assets/icon.png"))
    # Change the background color using configure
    root.configure(bg='#4c5844')

    ''' yea idk what im doing. old titlebar code.
    if vguititlebar == 1:
        root.overrideredirect(True)
        title_bar = Frame(root, bg='white', relief='raised', bd=2)
        close_button = Button(title_bar, text='X', command=root.destroy)
        window = Canvas(root, bg='black')
        
        title_bar.pack(expand=1, fill=X)
        close_button.pack(side=RIGHT)
        window.pack(expand=1, fill=BOTH)
        title_bar.bind('<B1-Motion>', move_window)
    '''
        

    titlebar= Frame(root,bg='#4c5844',height=5)
    titlebar.grid(sticky="w")
    
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)




mainwindow()
'''
window creation ^^
'''

#open file picker for game path
def findgame():
    global subwinpressable
    global freetocontinue
    global gamefolderpath
    
    if subwinpressable == 1:
        subwinpressable = 0
        gamefolderpath = os.path.realpath(crossfiledialog.choose_folder()) + "/"
        print(gamefolderpath)
        if os.path.basename(gamefolderpath[:-1]).casefold() == "sourcefilmmaker":
            print("YEA ITS SFM")
            if not gamefolderpath.endswith("/"):
                gamefolderpath = gamefolderpath + "/"
            if gamefolderpath == "/":
                subwindow('gamedirectorypickerinvalid')
            elif os.path.exists(gamefolderpath + "game/bin/") == False:
                subwindow('gamedirectorypickerinvalid')
            elif os.path.exists(gamefolderpath + "game/bin/") == True:
                freetocontinue = 1
        else:
            if not gamefolderpath.endswith("/"):
                gamefolderpath = gamefolderpath + "/"
            if gamefolderpath == "/":
                subwindow('gamedirectorypickerinvalid')
            elif os.path.exists(gamefolderpath + "bin/") == False:
                subwindow('gamedirectorypickerinvalid')
            elif os.path.exists(gamefolderpath + "bin/") == True:
                freetocontinue = 1
#open file picker for tf path
def findtf():
    global subwinpressable
    global freetocontinue
    global tffolderpath
    
    if subwinpressable == 1:
        subwinpressable = 0
        tffolderpath = os.path.realpath(crossfiledialog.choose_folder()) + "/"
        print(tffolderpath)
        if not tffolderpath.endswith("/"):
            tffolderpath = tffolderpath + "/"
        if tffolderpath == "/":
            subwindow('tfdirectorypickerinvalid')
        elif os.path.exists(tffolderpath + "tf/") == False:
            subwindow('tfdirectorypickerinvalid')
        elif os.path.exists(tffolderpath + "tf/") == True:
            freetocontinue = 1
            
#open file picker for hammer++ archive, if valid, extract to game winbin
def installhammer():
    successfulzip = 0
    ziplocation = crossfiledialog.open_file()
    hammerzip = zipfile.ZipFile(ziplocation, 'r')
    zipcontents = hammerzip.namelist()
    print(zipcontents)
    for i in range(len(zipcontents)):
        if "hammerplusplus.exe" in zipcontents[i]:
            successfulzip = 1
        else:
            pass
    
    if successfulzip == 1:
        print('ITS A HAMMAH (pluspkus')
        for file in hammerzip.namelist():
            if file.startswith('hammerplusplus_gmod_build8870/bin/'):
                hammerzip.extract(file, gamefolderpath + 'binwin/')
                os.system('cp -r "' + gamefolderpath + 'binwin/hammerplusplus_gmod_build8870')
    else:
        subwindow('hammerinstallinvalid')



#detect if proton is installed, if not, recreate subwindow. this sucks and is stupif but idk how else to do it and idk if ubtton will work because itll just skip and GAH
def checkproton():
    global gamefolderpath
    global gamename
    print("CHECKING FOR PROTON NOW")
    print(gamename)
    #game specific checking, should only need to be used for HL2 and Portal 2 but who knows
    if gamename == "half-life 2" or gamename == "portal 2":
        if os.path.exists(gamefolderpath + "bin/tier0.dll") == False:
            time.sleep(1)
            subwindow('protonenable')
    elif gamename == "team fortress 2 classified":
        if os.path.exists(gamefolderpath + "bin/x64/tier0.dll") == False:
            time.sleep(1)
            subwindow('protonenable')
    else:
        if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
            time.sleep(1)
            subwindow('protonenable')
def checksdk():
    global gamefolderpath
    global gamename
    if gamename == "portal 2":
        if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
            time.sleep(1)
            subwindow('p2sdkenable')
#check for hammer install
bintype = "undetected"
def checkhammer():
    global bintype
    global gamefolderpath
    if os.path.exists(gamefolderpath + "bin/win64/hammerplusplus.exe") == True:
        bintype = "win64"
    elif os.path.exists(gamefolderpath + "bin/x64/hammerplusplus.exe") == True:
        bintype = "x64"
    elif os.path.exists(gamefolderpath + "bin/hammerplusplus.exe") == True:
            bintype = "."
    
    if bintype == "undetected":
        time.sleep(1)
        subwindow('hammerenable')

def autohammer():
    global gamefolderpath
    global gamename
    #auto set up hammer++. wow
    tf2branch = ['team fortress 2','counter-strike source','half-life 1 source deathmatch','half-life 2 deathmatch','day of defeat source','sourcefilmmaker','team fortress 2 classified']
    sp2013branch = ['half-life 2','portal','source sdk base 2013 singleplayer','source sdk base 2007','source sdk base 2006']
    mp2013branch = ['klonoa 2 lunateas veil']
    gmodbranch = ['garrysmod','black mesa','alien swarm']
    portal2branch = ['portal 2']
    l4d2branch = ['left 4 dead','left 4 dead 2']
    csgobranch = ['csgo legacy','counter-strike global offensive']
    #source sdk base mp 2013 is also in the tf2branch but idk how to detect for it. why valve did you not make a seperate appid just for the tf2 branch of mp

    hammerplusplustype = ""
    version = ""
    frozenbuild = False

    if gamename in tf2branch:
        hammerplusplustype = "tf2"
    elif gamename in sp2013branch:
        hammerplusplustype = "2013sp"
    elif gamename in mp2013branch:
        hammerplusplustype = "2013mp"
    elif gamename in gmodbranch:
        hammerplusplustype = "gmod"
    elif gamename in portal2branch:
        hammerplusplustype = "portal2"
    elif gamename in l4d2branch:
        hammerplusplustype = "l4d2"
    elif gamename in csgobranch:
        hammerplusplustype = "csgo"
        version = "8864"
        frozenbuild = True
    else:
        print("unknown game branch!")
        return


    if not frozenbuild:
        print("getting the latest hammer plus plsu verison WOWWWWWWWWWWWWWWWWWWW")
        hammerplusplusversiontxt = "https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/refs/heads/main/version.txt"
        response = requests.get(hammerplusplusversiontxt)
        if response.status_code == 200:
            version = response.text
        else:
            print("failed to get the latest hammer++ version!")
            return

    print("using hammer++ version "+version)

    hammerpluspluszip = "hammerplusplus_"+hammerplusplustype+"_build"+version

    hammerplusplusurl = "https://github.com/ficool2/HammerPlusPlus-Website/releases/download/"+version+"/"+hammerpluspluszip+".zip"

    file_Path = configpath + hammerpluspluszip+".zip"
    print("Downloading "+hammerpluspluszip)
    response = requests.get(hammerplusplusurl)
    if response.status_code == 200:
        with open(file_Path, 'wb') as file:
            file.write(response.content)
        print("downloaded hammer++ for "+hammerplusplustype)
        version = response.text
        print("copying hammerplusplus files to bin")
        print("cd " + configpath + " && unzip " + hammerpluspluszip + ".zip && " + "cp -rv --update=older '" + configpath + hammerpluspluszip + "/bin/'* '" + gamefolderpath + "bin/'")
        os.system("cd " + configpath + " && unzip "+ hammerpluspluszip + ".zip && " + "cp -rv --update=older '" + configpath + hammerpluspluszip + "/bin/'* '" + gamefolderpath + "bin/'")
        print("removing temp hammer++ files...")
        os.remove(file_Path)
        print("cd " + configpath + " && rm -rv "+hammerpluspluszip+"/")
        os.system("cd " + configpath + " && rm -rv "+hammerpluspluszip+"/")
    else:
        print("hammer++ zip FAILED to download. Too bad!")
        return

'''subwindow creation'''
def subwindow(subwintype):
    global gamefolderpath
    global gamename
    global subwinpressable
    global bintype
    subwinpressable = 1

    for child in root.winfo_children(): 
        if not str(child) == '.!label2':
            child.destroy()
    # i cant figure this out for the life of me
    #if vguititlebar == 1:
    #    root.wm_attributes('-type', 'dialog')

    #wine set up window
    if subwintype == 'winesetup':
        #root.geometry('210x100')
        lbl = Label(root, text = "Setting up Wine. Please wait... \n This might take a while.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid()
        root.update()
    #game directory chooser
    elif subwintype == 'gamedirectorypicker':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Please navigate to the folder for the \n game you want to map for.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        findgame()
    #game directory chooser if you frick it up
    elif subwintype == 'gamedirectorypickerinvalid':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Could not find bin... \n Re-select the correct game folder.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        
        findgame()
        root.update()
        
    #tf2 directory chooser
    elif subwintype == 'tfdirectorypicker':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "SFM requires Team Fortress 2 to be installed for setup.\n Please navigate to your Team Fortress 2 folder.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/Team Fortress 2/", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(3)
        findtf()
    #tf directory chooser if you frick it up   
    elif subwintype == 'tfdirectorypickerinvalid':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Could not find TF2... \n SFM requires Team Fortress 2 to be installed for setup.\n Please re-select your Team Fortress 2 folder.", bg='#4c5844', \
        fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/Team Fortress 2/", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        
        findtf()
        root.update()
        
    #proton set up window
    if subwintype == 'protonenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Windows bin folder not detected. \n Go into steam and enable Proton for this game before continuing. \n You can turn off Proton later. \n \n \
        This window should auto-detect Proton on its own.",
        bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        root.update()
        checkproton()
        
    #P2SDK set up window for portal 2
    if subwintype == 'p2sdkenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Portal 2 Authoring Tools not detected. \n Go into steam and install Portal 2 Authoring Tools before continuing. \n \n This \
window should auto-detect Portal 2 Authoring Tools on its own.",
        bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        root.update()
        checksdk()
    #hammer++ set up window if it was automated
    if subwintype == 'hammerautomated':
        #root.geometry('600x140')
        lbl = Label(root, text = "Downloading Hammer++...", bg='#4c5844', \
        fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Do not close this window!", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        root.update()
        autohammer()
    #hammer++ set up window THE CORRECT USED ONE
    if subwintype == 'hammerenable':
        #root.geometry('600x140')
        lbl = Label(root, text = "Hammer++ could not be automatically installed. Please download it at \n https://ficool2.github.io/HammerPlusPlus-Website/download.html \nand copy its bin folder into:\
         \n " + gamefolderpath + "bin/",
        bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        root.update()
        checkhammer()
    #hammer++ install window
    elif subwintype == 'hammerinstall':
        #root.geometry('430x140')
        lbl = Label(root, text = "Please download Hammer++ and select the downloaded archive for it.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "You can install Hammer++ here: \n https://ficool2.github.io/HammerPlusPlus-Website/download.html", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)

        root.update()
        time.sleep(1)
        installhammer()
    #hammer++ install window if you freaked it up
    elif subwintype == 'hammerinstallinvalid':
        #root.geometry('423x140')
        lbl = Label(root, text = "Hammer++ executable not found. Did you select the correct \narchive?", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "You can install Hammer++ here: \n https://ficool2.github.io/HammerPlusPlus-Website/download.html", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        installhammer()
    #installing tools plus plus
    elif subwintype == 'toolsplusplusinstall':
        #root.geometry('260x130')
        lbl = Label(root, text = "++ compile tools are being installed and set up...\nThese are required for certain games. Please wait.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Hammer++ will start and close on its own. This is normal.", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(7)
    elif subwintype == 'editingconfigs':
        #root.geometry('260x130')
        lbl = Label(root, text = "Configuring Hammer++...", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Do not close this window!", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(1)
    elif subwintype == 'waiting':
        #root.geometry('260x130')
        lbl = Label(root, text = "Setting up...\nPlease wait.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Hammer++ may start and close on its own. This is normal.", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(7)
    #finishing up
    elif subwintype == 'finishingup':
        #root.geometry('260x130')
        lbl = Label(root, text = "Hammer++ for your game has \nset up. You can turn Proton off \nfor this game now. \nThe main window will open again now.", bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='#c3b550', font=("Tahoma", 9))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Thanks for using Linux Hammer Launcher! ^c^", bg='#4c5844', fg='#99a48e', font=("Tahoma", 9))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(7)
        


'''
sub window creation
'''
subwinkill = 0

#set gamesfile
gameconfig = 'none'


'''
Non GUI functions
'''

# close window when program is launched
def closelauncher():
    root.destroy()

# start correct game
game = "gmod";
def launchhammer(game, title):
    gamefolderfinder = game
    closelauncher()
    titlelowered = title.casefold()
    print("length of directory is " + str(len(os.path.basename(gamefolderfinder[:-1]))))
    print("directory up one is " + gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])])
    #set favorites in wineprefix to game folder
    gamefolderfinder = gamefolderfinder[:-19]
    print(gamefolderfinder + " HAMMER TEXT REMOVED!")
    while os.path.basename(gamefolderfinder) != title:
        print(os.path.basename(gamefolderfinder) == title)
        gamefolderfinder = gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])][:-1]
        print(gamefolderfinder + " found!")
    print(gamefolderfinder + " found!")
    print(os.getlogin())
    #game specific commands
    #hl2 shares the same bin between versions excluding a small handful of files (for only some people??) for some reason, remove bin and create new one from binwin with said files
    delcopybins = ['half-life 2']
    mergecopybins = ['portal', 'portal 2', 'half-life 1 source deathmatch']
    
    if titlelowered in delcopybins:
        if os.path.isdir(gamefolderfinder + "/bin/"):
            os.system("rm -r '" + gamefolderfinder + "/bin/'")
        print("cp -r '" + gamefolderfinder + "/binwin/' '" + gamefolderfinder + "/bin/'" )
        os.system("cp -r '" + gamefolderfinder + "/binwin/' '" + gamefolderfinder + "/bin/'" )
    elif titlelowered in mergecopybins:
        print("cp -r '" + gamefolderfinder + "/binwin/'* '" + gamefolderfinder + "/bin/'" )
        os.system("cp -r '" + gamefolderfinder + "/binwin/'* '" + gamefolderfinder + "/bin/'" )
    
    #add game folder for game to favorites
    print(configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps")
    if os.path.exists(configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps") == False:
        print("ln -s '" + gamefolderfinder + "/' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")
        os.system("ln -s '" + gamefolderfinder + "/' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")

    #game specific stuff
    #game specific stuff will go here, like launching portal 2 hammer after copying binwin to default bin

    # HL1MP does not have a built in gameinfo. re-copying it here just in case it decides to Die
    if titlelowered == "half-life 1 source deathmatch":
        print("COPYING HL1MP TXT")
        print("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderfinder + "/hl2/gameinfo.txt'")
        os.system("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderfinder + "/hl2/gameinfo.txt'")
    
    #tf2c needs to update gameinfo, this goes here instead of confighammer because tf2c updates revert the gameinfo back to the broken one
    if titlelowered == "team fortress 2 classified":
        with open(gamefolderfinder + '/tf2classified/gameinfo.txt', 'r') as file:
            data = file.read()
            data = data.replace('			//game+mod	|appid_440|tf/custom/*', '			//game+mod	"|all_source_engine_paths|../Team Fortress 2/tf/custom/*')
            #data = data.replace('			game+mod+vgui		|gameinfo_path|vpks/tf2c_assets.vpk', '')
            data = data.replace('			game+mod	|gameinfo_path|vpks/tf2c_overrides.vpk', '			game+mod	|gameinfo_path|overrides')
            data = data.replace('			game_lv				|appid_440|tf/tf2_lv.vpk', '			game_lv				"|all_source_engine_paths|../Team Fortress 2/tf/tf2_lv.vpk"')
            data = data.replace('			game+mod			|appid_440|tf/tf2_textures.vpk', '			game+mod			"|all_source_engine_paths|../Team Fortress 2/tf/tf2_textures.vpk"')
            data = data.replace('			game+mod			|appid_440|tf/tf2_sound_vo_english.vpk', '			game+mod			"|all_source_engine_paths|../Team Fortress 2/tf/tf2_sound_vo_english.vpk"')
            data = data.replace('			game+mod			|appid_440|tf/tf2_sound_misc.vpk', '			game+mod			"|all_source_engine_paths|../Team Fortress 2/tf/tf2_sound_misc.vpk"')
            data = data.replace('			game+mod+vgui		|appid_440|tf/tf2_misc.vpk', '			game+mod+vgui		"|all_source_engine_paths|../Team Fortress 2/tf/tf2_misc.vpk"')
            data = data.replace('			game				|appid_440|hl2/hl2_textures.vpk', '			game				"|all_source_engine_paths|../Team Fortress 2/hl2/hl2_textures.vpk"')
            data = data.replace('			game				|appid_440|hl2/hl2_sound_vo_english.vpk', '			game				"|all_source_engine_paths|../Team Fortress 2/hl2/hl2_sound_vo_english.vpk"')
            data = data.replace('			game				|appid_440|hl2/hl2_sound_misc.vpk', '			game				"|all_source_engine_paths|../Team Fortress 2/hl2/hl2_sound_misc.vpk"')
            data = data.replace('			game+vgui			|appid_440|hl2/hl2_misc.vpk', '			game+vgui			"|all_source_engine_paths|../Team Fortress 2/hl2/hl2_misc.vpk"')
            data = data.replace('			platform+vgui		|appid_440|platform/platform_misc.vpk', '			platform+vgui		"|all_source_engine_paths|../Team Fortress 2/platform/platform_misc.vpk"')
            data = data.replace('			// game				|appid_440|tf', '			// game				"|all_source_engine_paths|../Team Fortress 2/tf"')
            data = data.replace('			game				|appid_440|hl2', '			game				"|all_source_engine_paths|../Team Fortress 2/hl2"')
            data = data.replace('			platform			|appid_440|platform', '			platform			"|all_source_engine_paths|../Team Fortress 2/platform"')
        with open(gamefolderfinder + '/tf2classified/gameinfo.txt', 'w') as file:
            file.write(data)
    #stupid sfm grabage
    if titlelowered == "sourcefilmmaker":
        with open(gamefolderfinder + '/game/usermod/gameinfo.txt', 'r') as file:
            data = file.read()
            if '"Game"		"|all_source_engine_paths|hl2/hl2_textures.vpk"' in data:
                print("no need to change anything gameinfo has teh stuffs")
            else:
                print("need to add to gameinfo to work")
                data = data.replace('		"SearchPaths"\n		{\n', '		"SearchPaths"\n		{\n			"Game"		"|all_source_engine_paths|hl2/hl2_textures.vpk"\n\
			"Game"		"|all_source_engine_paths|hl2/hl2_sound_vo_english.vpk"\n			"Game"		"|all_source_engine_paths|hl2/hl2_sound_misc.vpk"\n\
			"Game"		"|all_source_engine_paths|hl2/hl2_misc.vpk"\n')
        with open(gamefolderfinder + '/game/usermod/gameinfo.txt', 'w') as file:
            file.write(data)
            
            
            
    
    #launch wine9 with hammer using correct prefix
    print('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    os.system('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    root.quit()

def clicked():
    print("clicked!")
    


#set config folder
configpath = os.path.expanduser('~') + "/.config/linuxhammerlauncher/"


#function to find which line numbers have GameExe in them

def find_gameexe_line_numbers(file_path, target_word):
    line_numbers = []
    with open(file_path, 'r') as file:
        for line_no, line in enumerate(file, start=1):
            if target_word in line:
                line_numbers.append(line_no)
    return line_numbers


#state and print
def stateandprint(string):
    #this frick is crapped
    print(string)

#edit hammer config/settings
def hammerconfig(binfolder, plusplusconfig):
    global gamefolderwindowified
    global gamefolderpath
    global gamename
    global backupgamefolderpath
    global tffolderpath
    global binfolderwindowified
    global bintypewindowified
    global combi3paths
    print("using binfolder "  + binfolder)
    combi3paths = gamefolderpath + binfolder + bintype
    
    #copy bin folder as binwin in same directory if it does not exist. auto delete if it already exists (though this might mess up user data. open dialog to ask user?)
    #sfm specific garbage
    if gamename == "game":
        if os.path.exists(gamefolderpath + "binwin") == True:
            print("BINWIN ALREADY EXISTS! deleting...")
            os.system("rm -r '" + gamefolderpath + "binwin/'")
        print("game folder path is " + gamefolderpath)
        if os.path.exists(gamefolderpath + "binwin") == False:
            print("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
            os.system("cp -r '" + tffolderpath + "bin/' '" + gamefolderpath + "binwin/'")
    else:
        if os.path.exists(gamefolderpath + "binwin") == True:
            print("BINWIN ALREADY EXISTS! deleting...")
            os.system("rm -r '" + gamefolderpath + "binwin/'")
        print("game folder path is " + gamefolderpath)
        if os.path.exists(gamefolderpath + "binwin") == False:
            print("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
            os.system("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")

    #gameconfig & settings generation
    timeout_time = 10

    #create a .sh file to run, timeout doesnt like WINEPREFIX= being there.
    #i do not know why sfm is trying to use a bash file to run. i dont need to know why as long as this works. sfm has its gameconfig made from scratch there is zero reason for it to launch
    #hammer
    print(gamefolderpath + "IS IT SFM????")
    if gamename == "game":
        print("please for the love of god stop using the sh file you dont need it sfm. why are we even generating them like this anymore anyways we have a thing to make them from scratch now is there\
any point in using such a jank system still whyd i make it like this")
        print("idk :3")
    else:
        bashfile = open(configpath + "temprunhammerbash.sh", "w")
        print("'WINEPREFIX="' + configpath + prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + '/hammerplusplus.exe"')
        bashfile.write('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + '/hammerplusplus.exe"')
        bashfile.close()
        os.system("chmod +x " + configpath + "temprunhammerbash.sh")
        #keep starting hammer for increasing amounts of time until gameconfig is generated
        #this whole system should probably be changed to just be a fallback option for when a game is run that we havent defined in the gameconfigmaker
        while os.path.isfile(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt") == False:
            print("timeout " + str(timeout_time) + " " + configpath + "temprunhammerbash.sh")
            os.system("timeout " + str(timeout_time) + " " + configpath + "temprunhammerbash.sh")
            timeout_time += 5
            root.update()

        os.remove(configpath + "temprunhammerbash.sh")
    #all this should only frickig do when the file exists god
    if os.path.isfile(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt") == True:
        subwindow("editingconfigs")
        if plusplusconfig == True:
            #edit gameconfig for hammer
            print("modifiying gameconfig for "  + binfolder)
            print(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt")
            #vbsp
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r') as file:
                data = file.read()
                data = data.replace("\\vbsp.exe", "\\vbspplusplus.exe")
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.write(data)
            #vvis
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r') as file:
                data = file.read()
                data = data.replace("\\vvis.exe", "\\vvisplusplus.exe")
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.write(data)
            #vrad
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r') as file:
                data = file.read()
                data = data.replace("\\vrad.exe", "\\vradplusplus.exe")
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.write(data)
        #binwin, if HL2 or any other game that cant run from binwin, dont config this.
        if binfolder == "binwin/":
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r') as file:
                data = file.read()
                data = data.replace("\\bin\\", "\\binwin\\")
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.write(data)

            #update settings.ini for people who already have used hammerplusplus before
            if os.path.exists(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini") == True:
                with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'r') as file:
                    data = file.read()
                    data = data.replace("\\bin\\", "\\binwin\\")
                with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'w') as file:
                    file.write(data)

        # dummy version
        batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
        batfile.write('@echo off\n\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
        batfile.close()

        #check for steam. if find steam make bat!! if not. too bad. fool
        steampath = os.popen("which steam").read()
        if os.path.exists(steampath[:-1]) == True:
            print("found steam!")
            #detect appid
            if os.path.exists(gamefolderpath + "steam_appid.txt") == True:
                with open(gamefolderpath + "steam_appid.txt", 'r') as appidfile:
                    print(gamefolderpath + "steam_appid.txt")
                    game_appid = str(appidfile.read())[:-2]
                    print("appid is " + game_appid)

                #create TRUE run game bat
                print(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat")
                batfile = open(gamefolderpath + "binwin/linuxhammerlauncher_rungame.bat", 'w')
                batfile.write('@echo off\nstart /unix ' + steampath[:-1] +' steam://rungameid/' + str(game_appid) + '//"%3 %4"\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
                batfile.close()
            else:
                print("steam_appid missing from game directory!")
        else:
            print("could not find steam. flatpak moment!")

        #create win version of gamefolderpath
        gamefolderwindowified = "Z:" + os.path.realpath(gamefolderpath).replace("/", "\\")
        binfolderwindowified = binfolder.replace("/","\\")
        bintypewindowified = bintype.replace("/","\\")
        print(os.path.realpath(gamefolderwindowified))
        print(binfolderwindowified)
        #set map vmf directory in config. check for picky map locations per hammer and config (like portal 2)
        print("THE LINE NUMS TO REPLACE ARE:")
        linestoconfig = (find_gameexe_line_numbers(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", '"MapDir"'))
        for i in range(len(linestoconfig)):
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r', encoding='utf-8') as file:
                lines = file.readlines()
            if gamename == "portal 2":
                lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\sdk_content\\maps"\n'
            elif gamename == "day of defeat source":
                lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\dod\\maps"\n'
            else:
                lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\mapsrc"\n'
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.writelines(lines)
        #set gameExe to .bat
        linestoconfig = (find_gameexe_line_numbers(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", '"GameExe"'))
        for i in range(len(linestoconfig)):
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r', encoding='utf-8') as file:
                lines = file.readlines()
            lines[linestoconfig[i] - 1] = '				"GameExe"		"' + gamefolderwindowified + "\\" + binfolderwindowified + 'linuxhammerlauncher_rungame.bat"\n'
            with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
                file.writelines(lines)
    else:
        #create win version of gamefolderpath. still need these.
        gamefolderwindowified = "Z:" + os.path.realpath(gamefolderpath).replace("/", "\\")
        binfolderwindowified = binfolder.replace("/","\\")
        bintypewindowified = bintype.replace("/","\\")
        print(os.path.realpath(gamefolderwindowified))
        print(binfolderwindowified)
        #still need the game bat too
        # dummy version
        batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
        batfile.write('@echo off\n\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
        batfile.close()
    
    #TF2C and HL1MP (and and SFM) needs its gameconfig made from scratch
    if gamename == "team fortress 2 classified":
        gameconfigmake("tf2c")
    if gamename == "half-life 1 source deathmatch":
        gameconfigmake("hl1mp")
    if gamename == "game":
        gameconfigmake("sfm")
    if gamename == "half-life 2 deathmatch":
        gameconfigmake("hl2mp")
    #sfm garbage stupid garbage that i hate so much copy paste hl2 garbage but not from half life but instead from team fortress 2 because screw you and into sfm because hammer++ hates having its 
    #stupif shaders outside of vpks in just plain files because it oH SO NEEDS THEM TO BE IN VPKS im so normal im so normal im so normal im so normal
    if gamename == "game":
        print("A SINGULAR 'GUH' SO I KNOW WHERE THE THING IS")
        print("cp -rv --update=none '" + tffolderpath + "hl2/' '" + gamefolderpath + "'")
        os.system("cp -rv --update=none '" + tffolderpath + "hl2/' '" + gamefolderpath + "'")
    

#create a gameconfig
def gameconfigmake(game):
    global bintypewindowified
    global gamefolderwindowified
    global gamefolderpath
    global gamename
    global combi3paths
    global binfolderwindowified
    if game == "tf2c":
        codename = "tf2classified"
        fgdname = "tf2c"
        pluspluscomp = "plusplus"
    if game == "hl1mp":
        codename = "hl1mp"
        fgdname = "halflife2"
        pluspluscomp = "plusplus"
    if game == "sfm":
        codename = "usermod"
        fgdname = "tf"
        pluspluscomp = "plusplus"
    if game == "hl2mp":
        codename = "hl2mp"
        fgdname = "hl2mp"
        pluspluscomp = "plusplus"
        
    hammerconfig = '"Configs"\n{\n	"Games"\n	{\n		"' + os.path.basename(gamefolderpath[:-1]) + '"\n		{\n			"GameDir"		"' + gamefolderwindowified + "\\" + codename + '"\n' \
    + '			"Hammer"\n			{\n				"GameData0"		"' + gamefolderwindowified + '\\binwin\\' + fgdname + '.fgd"\n' + '				"TextureFormat"		"5"\n\
                    "MapFormat"		"4"\n				"DefaultTextureScale"		"0.250000"\n				"DefaultLightmapScale"		"16"\n				"GameExe"		"' + \
    gamefolderwindowified + "\\" + binfolderwindowified + \
    'linuxhammerlauncher_rungame.bat"\n' + '				"DefaultSolidEntity"		"func_detail"\n\
				"DefaultPointEntity"		"info_player_start"\n				"BSP"		"' + gamefolderwindowified + "\\" + binfolderwindowified + bintypewindowified + "\\"\
    'vbsp' + pluspluscomp + '.exe"\n' + \
    '				"Vis"		"' + gamefolderwindowified + "\\" + binfolderwindowified + bintypewindowified + "\\" + 'vvis' + pluspluscomp + '.exe"\n' + \
    '				"Light"		"' + gamefolderwindowified + "\\" + binfolderwindowified + bintypewindowified + "\\" + 'vrad' + pluspluscomp + '.exe"\n' + \
    '				"MDL"		"' + gamefolderwindowified + "\\" + binfolderwindowified + bintypewindowified + "\\" + 'studiomdl.exe"\n' + \
    '				"GameExeDir"		"' + gamefolderwindowified + '"\n' + \
    '				"MapDir"		"' + gamefolderwindowified + '\\mapsrc"\n' + \
    '				"BSPDir"		"' + gamefolderwindowified + "\\" + codename + '\\maps"\n' + \
    '				"PrefabDir"		"' + gamefolderwindowified + "\\" + binfolderwindowified + bintypewindowified + '\\Prefabs"\n' + \
    '				"CordonTexture"		"tools/toolsskybox"\n				"MaterialExcludeCount"		"0"\n				"Previous"		"1"\n			}\n		}\n	}\n	"SDKVersion"		"5"\n}\n'
    
    print("\n\n\n\n\n\n")
    print(hammerconfig)
    with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as hppgameconfigfile:
        hppgameconfigfile.write(hammerconfig)
        
    #set gameexe
    print("THE LINE NUMS TO REPLACE ARE:")
    linestoconfig = (find_gameexe_line_numbers(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", '"GameExe"'))
    for i in range(len(linestoconfig)):
        with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[linestoconfig[i] - 1] = '				"GameExe"		"' + gamefolderwindowified + "\\" + binfolderwindowified + 'linuxhammerlauncher_rungame.bat"\n'
        with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
            file.writelines(lines)
    





'''
set up hammer wineprefix, set statuses along the way
'''

def setuphammer():
    global tffolderpath
    global settinguphammer
    global root
    global gamefolderpath
    global gamename
    global backupgamefolderpath
    global gameconfig
    backupgamefolderpath = "na"
    
    if settinguphammer == 0:
        settinguphammer = 1
        subwindow('winesetup')
        
        file_Path = configpath + 'runner/wine-9.0.1.tar.zst'
        wine9url = "https://archive.archlinux.org/packages/w/wine/wine-9.0-1-x86_64.pkg.tar.zst"
        #check if wine9 exists in runner folder, if it does not them download from arch repo (will work on any distro i think??????)
        stateandprint("Checking if Wine 9 exists.")
        print(os.path.exists(configpath + "runner/wine-9.0.1/"))
        if os.path.exists(configpath + "runner/wine-9.0.1/") == False:
            #download wine9
            stateandprint("Downloading Wine 9.0.1")
            response = requests.get(wine9url)
            if response.status_code == 200:
                with open(file_Path, 'wb') as file:
                    file.write(response.content)
                stateandprint("Downloaded Wine 9.0.1!")
            else:
                stateandprint("Failed to download Wine 9. \n Check your internet connection?")
            #extract wine9 targz
            stateandprint("Downloaded Wine 9.0.1! \nExtracting Wine...")
            os.system("cd " + configpath + "runner/" + " && tar --use-compress-program=unzstd -xvf " + configpath + "runner/wine-9.0.1.tar.zst")
            #rename extracted wine files from usr to wine-9.0.1
            stateandprint("Naming wine folder... \n Deleting downloaded archive...")
            os.system("mv " + configpath + "runner/usr/" + " " + configpath + "runner/wine-9.0.1/")
            #remove archive
            os.remove(configpath + "runner/wine-9.0.1.tar.zst")
        elif os.path.exists(configpath + "runner/wine-9.0.1/") == True:
            stateandprint("Wine 9 Exists! Continuing...")
        #check for prefix folder, if it doesnt exist, make it, dummy.
        if os.path.exists(configpath + "prefix/") == False:
            os.mkdir(configpath + "prefix/")
        #check for drive c in prefix folder, if its not there generate a wineprefix
        if os.path.exists(configpath + "prefix/drive_c/") == False:
            stateandprint("Generating Wine Prefix...")
            os.system('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + 'wineboot')
            #replace systheme=1 in registry to 0 for lag improvement
            while os.path.exists(configpath + "prefix/user.reg") == False:
                pass
            stateandprint("Set Wine Theme to None")
            with open(configpath + 'prefix/user.reg', 'r') as file:
                data = file.read()
                data = data.replace('"ThemeActive"="1"', '"ThemeActive"="0"')
            with open(configpath + 'prefix/user.reg', 'w') as file:
                file.write(data)
            
        #install DXVK
        stateandprint("Installing DXVK")
        os.system('WINEPREFIX="' + configpath + 'prefix/" winetricks dxvk2030')
        stateandprint("Installed DXVK!")
        
        #ask user for path to game
        freetocontinue = 0
        subwindow('gamedirectorypicker')

        gamename = os.path.basename(gamefolderpath[:-1]).casefold()
        
        #check if sfm is being used and ask for tf2 install
        if gamename == "sourcefilmmaker":
            subwindow('tfdirectorypicker')
            print(tffolderpath)
            #swap out gamefolderpath for tffolderpath and switch back later when SFM one is needed
            backupgamefolderpath = gamefolderpath
            backupgamename = gamename
            gamefolderpath = tffolderpath
            gamename = os.path.basename(tffolderpath[:-1]).casefold()
        elif gamename == "portal 2":
            #check if portal 2 is used, ask for enable proton and sdk
            subwindow('protonenable')
            subwindow('p2sdkenable')
        else:
            #check if proton is enabled, if not, prompt user to enable proton before continuing. check hammer usually, but some game specific checks (like hl2 and tier0.dll) are needed
            subwindow('protonenable')
        #check for hammerplusplus
        subwindow('hammerautomated')
        subwindow('hammerenable')

        # HL1MP does not have a built in gameinfo. why? no idea.
        if gamename == "half-life 1 source deathmatch":
            print("COPYING HL1MP TXT")
            print("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderpath + "hl2/gameinfo.txt'")
            os.system("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderpath + "hl2/gameinfo.txt'")
    
        #install plusplus tools, some games dont work for this
        noplusplus = ['portal 2', 'half-life 2', 'portal']
        if gamename not in noplusplus:
            subwindow("toolsplusplusinstall")
            
            file_Path = configpath + 'tools_plusplus.zip'
            tools_plusplusurl = "https://github.com/ficool2/misc_tools/releases/download/v1/tools_plusplus.zip"
            
            print("Downloading Tools ++")
            response = requests.get(tools_plusplusurl)
            if response.status_code == 200:
                with open(file_Path, 'wb') as file:
                    file.write(response.content)
                stateandprint("Downloaded Tools++!")
            else:
                stateandprint("Failed to download Tools++. \n Check your internet connection?")
            print("copying tools files to bin")
            print("cd " + configpath + " && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "tools_plusplus/tools/'* '" + gamefolderpath + "bin/" + bintype + "/'")
            os.system("cd " + configpath + " && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "tools_plusplus/tools/'* '" + gamefolderpath + "bin/" + bintype + "/'")
            print("removing temp tools++ files...")
            os.remove(file_Path)
            print("cd " + configpath + " && rm -rv tools_plusplus/")
            os.system("cd " + configpath + " && rm -rv tools_plusplus/")
        else:
            subwindow("waiting")
            time.sleep(10)
        
        # it's probably better to do this when the launcher starts to check for duplicates for all games. But Whatever................ this works! kinda.
        if gamename == "sourcefilmmaker":
            gamefolderpath = backupgamefolderpath
            gamename = backupgamename


        print("CHECKING FOR CONFIG DUPLICATES")

        gameline = []

        lines = []

        gameconfig = open(configpath + "games.txt", 'r')

        specified_lines = [99]

        for pos, l_num in enumerate(gameconfig):
            if pos in specified_lines:
                currentgamedef = l_num
            else:
                currentgamedef = l_num
            if gamename == json.loads(currentgamedef.replace("'", '"'))[0].casefold():
                # murdering THESE specifically becuase i hate them
                print("duplicate game detected in config on line " + str(pos))
                gameline.append(pos)

        print(gameline)

        gameconfig.close()

        # there's probably a cleaner way of doing this but What Ever
        with open(configpath + "games.txt", 'r') as gr:
            lines = gr.readlines()

        print("CLEANING CONFIG")

        # cleanup all duplicates. should probably only do when there are actually duplicates but Who Cares
        with open(configpath + "games.txt", 'w') as gc:
            for duplicate, line in enumerate(lines):
                if duplicate not in gameline:
                    print("not removing line "+ str(duplicate))
                    gc.write(line)

        print("SETTING UP NEW CONFIG")
        #write new game definition to config file. check if file exists
        gameconfig = open(configpath + "games.txt", "a")
        
        version = "1"
        hammerplusplusversiontxt = "https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/refs/heads/main/version.txt"
        response = requests.get(hammerplusplusversiontxt)
        if response.status_code == 200:
            version = response.text

        #game specific configuring.
        noupdate = ['csgo legacy','counter-strike global offensive']
        if gamename in noupdate:
            print("not autoupdating this hammer++")
            version = "0"

        nobinwin = ['half-life 2', 'portal', 'portal2']
        if gamename in nobinwin:
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/hammerplusplus.exe', '"+version+"']" + "\n"
            if os.path.exists(gamefolderpath + "bin/GameConfig.txt") == True:
                os.remove(gamefolderpath + "bin/GameConfig.txt")
            hammerconfig("bin/", False) #second value is for whether or not to config ++ tools
            os.system("cp '" + gamefolderpath + "bin/hammerplusplus/hammerplusplus_gameconfig.txt' '" + gamefolderpath + "binwin/hammerplusplus/hammerplusplus_gameconfig.txt'")
        elif gamename == "half-life 1 source deathmatch":
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/hammerplusplus.exe', '"+version+"']" + "\n"
            if os.path.exists(gamefolderpath + "bin/GameConfig.txt") == True:
                os.remove(gamefolderpath + "bin/GameConfig.txt")
            hammerconfig("bin/", True)
            os.system("cp '" + gamefolderpath + "bin/hammerplusplus/hammerplusplus_gameconfig.txt' '" + gamefolderpath + "binwin/hammerplusplus/hammerplusplus_gameconfig.txt'")
        elif gamename == "sourcefilmmaker":
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "game/binwin/" + bintype + "/hammerplusplus.exe', '"+version+"']" + "\n"
            gamefolderpath = backupgamefolderpath + "game/"
            hammerconfig("binwin/", True)
        else:
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "binwin/" + bintype + "/hammerplusplus.exe', '"+version+"']" + "\n"
            hammerconfig("binwin/", True)
        
        gameconfig.write(gamedefinition)
        print(gamedefinition)
        gameconfig.close() 
        
        
        
        #show finishing up window
        subwindow('finishingup')
        
        #make button clickable
        settinguphammer = 0
        #go back to main window
        root.destroy()
        root = Tk()
        mainwindow()
        rendermainwindow()
        
#.config/linuxhammerlauncher/



#check for prefix folder, if it doesnt exist, make it, dummy.
if os.path.exists(configpath + "prefix/") == False:
    os.mkdir(configpath + "prefix/")
#check for runner folder, if it doesnt exist, make it, idiot.
if os.path.exists(configpath + "runner/") == False:
    os.mkdir(configpath + "runner/")
#check for games config file, if it doesnt exist, make it, fool.
if os.path.exists(configpath + "games.txt") == False:
    gameconfig = open(configpath + "games.txt", 'w')
    gameconfig.write("")
    gameconfig.close()
    print("game config not found, created new one.")

'''
Non GUI functions ^^
'''



'''
GUI function stuffs
'''


#makes game button
def creategamebutton(height, title, hammerpath):
    #set icon for game
    titlelowered = title.casefold()
    if titlelowered == "garrysmod":
        gameicon = Image("photo", file="assets/buttonicons/games/garrysmod.png")
    elif titlelowered == "portal 2":
        gameicon = Image("photo", file="assets/buttonicons/games/portal2.png")
    elif titlelowered == "portal":
        gameicon = Image("photo", file="assets/buttonicons/games/portal.png")
    elif titlelowered == "counter-strike source":
        gameicon = Image("photo", file="assets/buttonicons/games/cstrike.png")
    elif titlelowered == "counter-strike global offensive":
        gameicon = Image("photo", file="assets/buttonicons/games/csgo.png")
    elif titlelowered == "day of defeat source":
        gameicon = Image("photo", file="assets/buttonicons/games/dod.png")
    elif titlelowered == "half-life 2":
        gameicon = Image("photo", file="assets/buttonicons/games/hl2.png")
    elif titlelowered == "sourcefilmmaker":
        gameicon = Image("photo", file="assets/buttonicons/games/sfm.png")
    elif titlelowered == "team fortress 2":
        gameicon = Image("photo", file="assets/buttonicons/games/tf2.png")
    elif titlelowered == "team fortress 2 classified":
        gameicon = Image("photo", file="assets/buttonicons/games/tf2classified.png")
    elif titlelowered == "half-life 1 source deathmatch":
        gameicon = Image("photo", file="assets/buttonicons/games/hl1mp.png")
    elif titlelowered == "half-life 2 deathmatch":
        gameicon = Image("photo", file="assets/buttonicons/games/hl2mp.png")
    else:
        gameicon = Image("photo", file="assets/buttonicons/sdk_hammer.png")
    gameicn = Label(optionsframe, bg="#3e4637", image=gameicon, anchor="e")
    gameicn.image = gameicon
    gameicn.grid(row=height, column=0, sticky="ew")

    #create functional button
    btn = Button(optionsframe, text = title , fg = "#d8ded3", command=lambda: launchhammer(hammerpath, title), bg='#3e4637',
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    btn.grid(row=height, column=1,sticky="ew")

def rendermainwindow():
    global optionsframe
    global root

    padding = Frame(root, bg="#4c5844", relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=0,sticky="w")

    '''
    Frame creation
    '''
    optionsframe = Frame(root, bg="#3e4637", relief='sunken', bd=1, highlightthickness=0)
    optionsframe.grid(row=1, column=1,sticky="we")
    optionsframe.grid_columnconfigure(0, minsize=23, weight=0)
    optionsframe.grid_columnconfigure(1, minsize=211, weight=1)
    '''
    frame creation ^^
    '''
    padding = Frame(root, bg="#4c5844", relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=2,sticky="e")

    linenum = 0
    #create game buttons based on game defs
    gameconfig = open(configpath + "games.txt", 'r')
    
    # lines to print (or not to print this list just kinda needs to be here regardless of how little it accomplishes
    specified_lines = [99]

    #editors title
    setuptext = Label(optionsframe, text = "HAMMER EDITORS", fg='#c4b550', bg='#3e4637', justify="left",font=("Tahoma", 7), anchor="sw", height=2,  highlightthickness=0)
    setuptext.grid(row=0, column=1, sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=1, column=0,sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=1, column=1,sticky="ew")

    # loop over lines in a file
    for pos, l_num in enumerate(gameconfig):
        # check if the line number is specified in the lines to read array. or not. IDK THERES AN ELSE TOO TO MAKE IT SO IT DOESNT MATTER I HATE THIS GAHH
        if pos in specified_lines:
            # this is a stupid way to do this but i copy pasted it from online and cant morph it into working any other way and it works i doutb anyones computer will ag from this if you dislike how 
            #messy it is im sorry
            currentgamedef = l_num
        else:
            currentgamedef = l_num
        print(json.loads(currentgamedef.replace("'", '"'))[0])
        creategamebutton(linenum + 3, json.loads(currentgamedef.replace("'", '"'))[0], json.loads(currentgamedef.replace("'", '"'))[1])
        linenum += 1
    gameconfig.close()

    
        
    '''
    GUI Stuffs
    '''

    #UTILITIES
    setuptext = Label(optionsframe, text = "UTILITIES", fg='#c4b550', bg='#3e4637', justify="left",font=("Tahoma", 7), anchor="sw", height=2, highlightthickness=0)
    setuptext.grid(row=linenum+4, column=1, sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+5, column=0,sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+5, column=1,sticky="ew")

    hammericon = Image("photo", file="assets/buttonicons/sdk_setup.png")
    setupicn = Label(optionsframe, bg="#3e4637", image=hammericon, anchor="e")
    setupicn.image = hammericon #the fact that you have to do this just to keep an image alive is extremely stupid dumb dumb stupid dumb stupid. stupid face
    setupicn.grid(row=linenum+6, column=0, sticky="ew")
    #set up button
    setupbtn = Button(optionsframe, text = "Set up Hammer", fg = "#d8ded3", command=lambda: setuphammer(), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    #reset button
    deleteicon = Image("photo", file="assets/buttonicons/sdk_reset.png")
    removeicn = Label(optionsframe, bg="#3e4637", image=deleteicon, anchor="e")
    removeicn.image = deleteicon #see above
    removeicn.grid(row=linenum+7, column=0, sticky="ew")
    resetbtn = Button(optionsframe, text = "Reset Hammer", fg = "#d8ded3", command=lambda: print("STUB!"), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    #delete button
    deleteicon = Image("photo", file="assets/buttonicons/sdk_delete.png")
    deleteicn = Label(optionsframe, bg="#3e4637", image=deleteicon, anchor="e")
    deleteicn.image = deleteicon
    deleteicn.grid(row=linenum+8, column=0, sticky="ew")
    deletebtn = Button(optionsframe, text = "Delete Hammer", fg = "#d8ded3", command=lambda: print("STUB!"), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)


    setupbtn.grid(row=linenum+6, column=1, sticky="ew")
    resetbtn.grid(row=linenum+7, column=1, sticky="ew")
    deletebtn.grid(row=linenum+8, column=1, sticky="ew")


    #CREDITS
    setuptext = Label(optionsframe, text = "CREDITS", fg='#c4b550', bg='#3e4637', justify="left",font=("Tahoma", 7), anchor="sw", height=2, highlightthickness=0)
    setuptext.grid(row=linenum+9, column=1, sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+10, column=0,sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+10, column=1,sticky="ew")

    endericon = Image("photo", file="assets/buttonicons/credit_end.png")
    crediticn = Label(optionsframe, bg="#3e4637", image=endericon, anchor="e")
    crediticn.image = endericon #see above
    crediticn.grid(row=linenum+11, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "EnderCatCore", fg = "#d8ded3", command=lambda: webbrowser.open("https://endercatcore.neocities.org",new=2, autoraise=True), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+11, column=1, sticky="ew")

    tommyicon = Image("photo", file="assets/buttonicons/credit_tam.png")
    crediticn = Label(optionsframe, bg="#3e4637", image=tommyicon, anchor="e")
    crediticn.image = tommyicon #see above
    crediticn.grid(row=linenum+12, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "Thomasluigi07", fg = "#d8ded3", command=lambda: webbrowser.open("https://thomasluigi07.com",new=2, autoraise=True), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+12, column=1, sticky="ew")

    dummy = Frame(root,bg='#4c5844',height=5)
    dummy.grid(sticky="w")

rendermainwindow()

#Execute Tkinter
root.mainloop()
