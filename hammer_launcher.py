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
import random


''' TODO and ISSUES

-fix sfm support. something, andi genuinely do not know WHAT. broke support for it. even going to earlier commits doesnt fix it when it did work then.

-stop binwin from being made or kept around when it doesnt need to be for games like hl2 (maybe snag the dlls from toolsplusplus if theyre compatible??)

-why are plusplus tools not configged for l4d2 i will kill

-"use maps instead of mapsrc" doesnt work for every game? so far the games to not work with it are tf2classified and half life 1 source deathmatch, for some reason??? theres no correlation?

-dxvk cache keeps showing up in root source folder thing?? 

-delete everything option. removes hammer++ from all games and removes the bat that launches games. delete wineprefix too (BUT FOR THE LOVE OF GOD CLEAR OUT SYMLINKS FIRST SEPERATELY OR HELL WILL BREAK LOOSE)

-progress bar for downloads/setting up wine. if we cant track progress for things just do the thing like in windows where theres a progress bar but it just moves constnatly instead of being an actual percentage thingie (use images for it??)

-make urls in setup clickable/buttons.

-is the sourcesdk_content bug still there?? please god no.

'''
#--------

''' games to add support to
half life source (might be easy if we snag the gameinfo? im guessing we can reuse hl1mp stuff but not sure)
'''
# freak
print("if youre opening this in the terminal because something went wrong, im sorry.")


#check deps
def checkdependencies():
    #check if winetricks is installed
    print(os.popen("whereis winetricks").read())
    if os.popen("whereis winetricks").read() == "winetricks:\n":
        print("WINETRICKSNOTFOUND")
        subwindow("winetricksnotfound")

#fallback settings, set these, then apply settings.ini, that way if settings.ini is freaked and doesnt have a value the program doesnt frickigng die
state_htype = False
state_disablehppupdates = False
state_theme = 0
state_usemapsrc = True

# random number for tamas icon.
# why? i cant decide on a single variant to use!!! too BAD
tamarand = str(random.randint(0, 3))
print(tamarand)

#vguititlebar = 1

#set config folder
homefolder = os.path.expanduser("~")
print("user is " + os.getlogin())
configpath = homefolder + "/.config/linuxhammerlauncher/"


# this is a function so temp is still recreated after deletion. and no code reusing idk
def cleantemp():
    if os.path.exists(configpath + "temp/") == True:
        print("cleaning temp folder...")
        os.system("cd " + configpath + " && rm -r temp/")
    os.mkdir(configpath + "temp/")

#CONFIG FILE/FOLDER CREATION
#CONFIG FILE/FOLDER CREATION
#CONFIG FILE/FOLDER CREATION

#check for .config, if it doesn't exists. Make it. MAKE IT. WHY DOESN'T IT EXIST.
if os.path.exists(homefolder + "/.config/") == False:
    os.mkdir(homefolder + "/.config/")
# look!!!!!!!!!!! hamer launcher :3
if os.path.exists(configpath) == False:
    os.mkdir(configpath)
#check for prefix folder, if it doesnt exist, make it, dummy.
if os.path.exists(configpath + "prefix/") == False:
    os.mkdir(configpath + "prefix/")
#check for runner folder, if it doesnt exist, make it, idiot.
if os.path.exists(configpath + "runner/") == False:
    os.mkdir(configpath + "runner/")
#check for tmp folder. if it exists. KILL IT. then make it (again), nincompoop.
cleantemp()
#check for games config file, if it doesnt exist, make it, buffoon.
if os.path.exists(configpath + "games.txt") == False:
    gameconfig = open(configpath + "games.txt", 'w')
    gameconfig.write("")
    gameconfig.close()
    print("game config not found, created new one.")
#check for games config file, if it doesnt exist, make it, imbecile.
if os.path.exists(configpath + "settings.ini") == False:
    settingsini = open(configpath + "settings.ini", 'w')
    settingsini.write('[LHL Settings]\nstate_htype = False\nstate_disablehppupdates = False\nstate_theme = 0\nstate_usemapsrc = True')
    settingsini.close()
    print("settings ini not found, created new one.")

#SETTINGS READING AND WRITING
#SETTINGS READING AND WRITING
#SETTINGS READING AND WRITING

#write vars to settingsini function
def writetosettings():
    print("PLEASE WRITE")
    settingsini = open(configpath + "settings.ini", 'w')
    settingsini.write('[LHL Settings]\n' + \
    'state_htype = ' + str(state_htype) + '\n'\
    'state_disablehppupdates = ' + str(state_disablehppupdates) + '\n'\
    'state_theme = ' + str(state_theme) + '\n'\
    'state_usemapsrc = ' + str(state_usemapsrc) + '\n'\
    )
    settingsini.close()

#set vars to values in settingsini function
def loadsettings():
    global state_htype
    global state_disablehppupdates
    global state_theme
    global state_usemapsrc
    
    print("hello? this thing working???")
    #no it isnt sory :(

    with open(configpath + "settings.ini","r") as inifile:
        configlines = inifile.read().split("\n")
    
    
    for i,line in enumerate(configlines):
        if "state_htype = " in line: #find and load htype
            print("Setting HType is:")
            print(line[line.find(" = ") + 3:])
            if line[line.find(" = ") + 3:] == "True":
                state_htype = True
            elif line[line.find(" = ") + 3:] == "False":
                state_htype = False
        if "state_disablehppupdates = " in line: #find and load H++ update setting
            print("Setting HPPUpdate is:")
            print(line[line.find(" = ") + 3:])
            if line[line.find(" = ") + 3:] == "True":
                state_disablehppupdates = True
            elif line[line.find(" = ") + 3:] == "False":
                state_disablehppupdates = False
        if "state_theme = " in line: #find and load theme setting
            print("Setting Theme is:")
            print(line[line.find(" = ") + 3:])
            state_theme = int(line[line.find(" = ") + 3:])
        if "state_usemapsrc = " in line: #find and load map folder setting
            print("Setting MapSrc is:")
            print(line[line.find(" = ") + 3:])
            if line[line.find(" = ") + 3:] == "True":
                state_usemapsrc = True
            elif line[line.find(" = ") + 3:] == "False":
                state_usemapsrc = False
            

loadsettings()





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

settinguphammer = 0


#add theme defs/names here
themenames = ["VGUI", "SFM"]
print(themenames[state_theme].lower())


def updatetheme():
    global themenames
    global state_theme
    global colors_background
    global colors_framebackground
    global colors_highlight
    global colors_primarytext
    global colors_secondarytext
    global colors_tertiarytext
    global colors_headertext
    global style_frameborder
    global style_showdividers
    global style_showicons
    global style_font
    global style_headerfont
    global style_headerfontstyle
    global style_fontsize
    global style_headerfontsize
    global style_smallfontsize
    global style_forceheadercaps
    global style_bannerposition
    global style_bannerimage
    global style_graphicspath
    
    
    #add theme configs here
    
    print("UPDATING THEME")
    if themenames[state_theme].lower() == "vgui":
        colors_background = "#4c5844"
        colors_framebackground = "#3e4637"
        colors_highlight = "#968731"
        colors_primarytext = "#d8ded3"
        colors_secondarytext = "#c3b550"
        colors_tertiarytext = "#99a48e"
        colors_headertext = "#c4b550"
        style_frameborder = "sunken"
        style_showdividers = True
        style_showicons = True
        style_font = "Tahoma"
        style_headerfont = "Ubuntu"
        style_headerfontstyle = ""
        style_fontsize = 9
        style_headerfontsize = 7
        style_smallfontsize = 7
        style_forceheadercaps = True
        style_bannerposition = "bottom"
        style_bannerimage = "/assets/banner/hammerlauncher_banner.png"
        style_graphicspath = "/assets/graphics/"
        
    elif themenames[state_theme].lower() == "eyesore":
        colors_background = "yellow"
        colors_framebackground = "red"
        colors_highlight = "blue"
        colors_primarytext = "green"
        colors_secondarytext = "black"
        colors_tertiarytext = "black"
        colors_headertext = "lime"
        style_frameborder = "flat"
        style_showdividers = False
        style_showicons = True
        style_font = "Roboto Condensed"
        style_headerfont = "DejaVu Sans"
        style_headerfontstyle = "bold"
        style_fontsize = 12
        style_headerfontsize = 15
        style_smallfontsize = 3
        style_forceheadercaps = False
        style_bannerposition = "top"
        style_bannerimage = "/assets/banner/hammerlauncher_banner.png"
        style_graphicspath = "/assets/graphics/"
        
    elif themenames[state_theme].lower() == "sfm":
        colors_background = "black"
        colors_framebackground = "black"
        colors_highlight = "black"
        colors_primarytext = "#cfcfcf"
        colors_secondarytext = "#606060"
        colors_tertiarytext = "#4d4d4d"
        colors_headertext = "#5f5f5f"
        style_frameborder = "flat"
        style_showdividers = False
        style_showicons = False
        style_font = "DejaVu Sans"
        style_headerfont = "DejaVu Sans"
        style_headerfontstyle = "bold"
        style_fontsize = 9
        style_headerfontsize = 14
        style_smallfontsize = 7
        style_forceheadercaps = False
        style_bannerposition = "top"
        style_bannerimage = "/assets/banner/hammerlauncher_banner_sfm.png"
        style_graphicspath = "/assets/graphics/sfm/"

updatetheme()
    
 
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
    root.tk.call('wm','iconphoto',root._w, Image("photo", file=os.path.dirname(__file__)+"/assets/icon.png"))
    # Change the background color using configure
    root.configure(bg=colors_background)

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
        

    titlebar= Frame(root,bg=colors_background,height=5)
    titlebar.grid(sticky="w")
    
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)





mainwindow()
'''
window creation ^^
'''

#toggle bool
def toggle_bool(value):
    return not value


#open file picker for game path
def findgame():
    global subwinpressable
    global freetocontinue
    global gamefolderpath
    global pathentrydir
    
    if subwinpressable == 1:
        subwinpressable = 0
        gamefolderpath = os.path.realpath(crossfiledialog.choose_folder()) + "/"
        print(gamefolderpath)
    pathentrydir=StringVar(value=gamefolderpath)
    subwindow("gamedirectorypicker")

def checkgamepath():
    global subwinpressable
    global freetocontinue
    global gamefolderpath
    global pathentrydir
    global backupgamefolderpath
    global backupgamename
    gamefolderpath = os.path.realpath(pathentrydir.get())
    print(gamefolderpath)
    backupgamename = "na"
    
    
    if not gamefolderpath.endswith("/"):
        gamefolderpath = gamefolderpath + "/"
        if gamefolderpath == "/":
            subwindow('gamedirectorypickerinvalid')

        if os.path.exists(gamefolderpath + "bin/") == False:
            if os.path.exists(gamefolderpath + "game/bin/") == False:
                subwindow('gamedirectorypickerinvalid')
            elif os.path.exists(gamefolderpath + "game/bin/") == True:
                print("eeeyup its sfm")
                gamefolderpath = gamefolderpath + "game/"
                
                gamename = os.path.basename(gamefolderpath[:-1]).casefold()
                backupgamefolderpath = gamefolderpath
                backupgamename = gamename
                
                subwindow('tfdirectorypicker')
                
                freetocontinue = 1
                
                
                
            else:
                subwindow('gamedirectorypickerinvalid')
        elif os.path.exists(gamefolderpath + "bin/") == True:
            freetocontinue = 1
            setuphammer_part2()
            
#open file picker for tf path
def findtf():
    global subwinpressable
    global freetocontinue
    global tffolderpath
    global pathentrydir
    global gamename 
    
    
    
    if subwinpressable == 1:
        subwinpressable = 0
        tffolderpath = os.path.realpath(crossfiledialog.choose_folder()) + "/"
        print(tffolderpath)
    pathentrydir=StringVar(value=tffolderpath)
    subwindow("tfdirectorypicker")
        

def checktfpath():
    global subwinpressable
    global freetocontinue
    global tffolderpath
    global pathentrydir
    global backupgamefolderpath
    global backupgamename
    tffolderpath = os.path.realpath(pathentrydir.get())
    
    
    print(tffolderpath)
    if not tffolderpath.endswith("/"):
        tffolderpath = tffolderpath + "/"
    if tffolderpath == "/":
        subwindow('tfdirectorypickerinvalid')
    elif os.path.exists(tffolderpath + "tf/") == False:
        subwindow('tfdirectorypickerinvalid')
    elif os.path.exists(tffolderpath + "tf/") == True:
        freetocontinue = 1
        setuphammer_part2()
    
            
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
    tier0 = ['half-life 2','portal 2','half-life 1 source deathmatch','left 4 dead','left 4 dead 2']
    if gamename in tier0:
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
    if gamename == "left 4 dead":
        if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
            time.sleep(1)
            subwindow('l4dsdkenable')
    if gamename == "left 4 dead 2":
        if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
            time.sleep(1)
            subwindow('l4d2sdkenable')
#check for hammer install
bintype = "undetected"
def checkhammer():
    global bintype
    global gamefolderpath
    
    if state_htype == False:
        if os.path.exists(gamefolderpath + "bin/win64/hammerplusplus.exe") == True:
            bintype = "win64"
        elif os.path.exists(gamefolderpath + "bin/x64/hammerplusplus.exe") == True:
            bintype = "x64"
        elif os.path.exists(gamefolderpath + "bin/hammerplusplus.exe") == True:
                bintype = "."
    if state_htype == True:
        print("HELLO??? WORK?")
        if os.path.exists(gamefolderpath + "bin/win64/hammer.exe") == True:
            bintype = "win64"
        elif os.path.exists(gamefolderpath + "bin/x64/hammer.exe") == True:
            bintype = "x64"
        elif os.path.exists(gamefolderpath + "bin/hammer.exe") == True:
            bintype = "."
    
    print("FRICK")
    if bintype == "undetected":
        time.sleep(1)
        subwindow('hammerenable')

def autohammer(updatefolder,updatename):
    global gamefolderpath
    global gamename

    print("AUTOHAMMER")

    try:
        print(gamename)
        print(gamefolderpath)
    except:
        print("gamename/gamefolderpath does not exist yet")

    if updatefolder and updatename:
        gamefolderpath = updatefolder+"/"
        gamename = updatename

    directory = "bin/"

    #update specific stuff
    if updatefolder and updatename:
        print(gamefolderpath)
        if os.path.exists(gamefolderpath + "/binwin/") == True:
            directory = "binwin/"

    print("using " + directory + " for automated install")

    #auto set up hammer++. wow
    tf2branch = ['team fortress 2','counter-strike source','half-life 1 source deathmatch','half-life 2 deathmatch','day of defeat source','game','sourcefilmmaker','team fortress 2 classified']
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

    try:
    
        if not frozenbuild:
            print("getting the latest hammer plus plsu verison WOWWWWWWWWWWWWWWWWWWW")
            hammerplusplusversiontxt = "https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/refs/heads/main/version.txt"
            response = requests.get(hammerplusplusversiontxt)
            if response.status_code == 200:
                version = response.text
            else:
                print("failed to get the latest hammer++ version!")
                return

        cleantemp()

        print("using hammer++ version "+version)

        hammerpluspluszip = "hammerplusplus_"+hammerplusplustype+"_build"+version

        hammerplusplusurl = "https://github.com/ficool2/HammerPlusPlus-Website/releases/download/"+version+"/"+hammerpluspluszip+".zip"

        file_Path = configpath + "temp/" + hammerpluspluszip+".zip"
        print("Downloading "+hammerpluspluszip)
        response = requests.get(hammerplusplusurl)
        if response.status_code == 200:
            with open(file_Path, 'wb') as file:
                file.write(response.content)
            print("downloaded hammer++ for "+hammerplusplustype)
            version = response.text
            print("copying hammerplusplus files to bin")
            print("cd " + configpath + "temp/ && unzip " + hammerpluspluszip + ".zip && " + "cp -rv --update=older '" + configpath + "temp/" + hammerpluspluszip + "/bin/'* '" + gamefolderpath + directory +"'")
            os.system("cd " + configpath + "temp/ && unzip "+ hammerpluspluszip + ".zip && " + "cp -rv --update=older '" + configpath + "temp/" + hammerpluspluszip + "/bin/'* '" + gamefolderpath + directory +"'")
        else:
            print("hammer++ zip FAILED to download. Too bad!")
    except:
        pass
    
    cleantemp()


'''subwindow creation'''
def subwindow(subwintype):
    global gamefolderpath
    global tffolderpath
    global gamename
    global backupgamefolderpath
    global backupgamename
    global subwinpressable
    global bintype
    global pathentrydir
    subwinpressable = 1
    


    for child in root.winfo_children(): 
        child.destroy()
    # i cant figure this out for the life of me
    #if vguititlebar == 1:
    #    root.wm_attributes('-type', 'dialog')

    root.update()

#
    #winetrickscheck
    if subwintype == 'winetricksnotfound':
        lbl = Label(root, text = "WARNING: Winetricks is not installed!!\nPlease install winetricks for the launcher to function properly. \nOnce you have \
installed winetricks, restart the program.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Debian/Ubuntu winetricks install command: 'sudo apt install winetricks'\n\
Fedora winetricks install command: 'sudo dnf install winetricks'\n\
Arch Linux winetricks install command: 'sudo pacman -S winetricks'", \
        bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=3, column=0)
        lbl = Label(root, text = "If you believe this is a mistake and would wish to continue, you can\nclick 'Continue anyways'.", \
        bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=4, column=0)
        
        
        ''' idk how to aliggn this stealing from openpopup isnt working
        quitbutton = Button(root, text = "Quit", fg=colors_primarytext, command=lambda: environment.exit(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        quitbutton.grid(row=3, column=1, pady=30)
        '''
        
        continuebtn = Button(root, text = "Continue anyways", fg=colors_primarytext, command=lambda: startmainwindow(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        continuebtn.grid(row=5, column=0, pady=30)
        
        
        root.update()
    #wine set up window
    if subwintype == 'winesetup':
        #root.geometry('210x100')
        lbl = Label(root, text = "Setting up Wine. Please wait... \n This might take a while.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid()
        root.update()
    #hammer launch
    if subwintype == 'hammerlaunch':
        #root.geometry('210x100')
        lbl = Label(root, text = "Launching Hammer++...", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid()
        root.update()
    #hammer delete in progress
    if subwintype == 'deletinghammer':
        #root.geometry('210x100')
        lbl = Label(root, text = "Deleting this Hammer instance...", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid()
        root.update()
    #hammer delete finished
    if subwintype == 'finishdelete':
        #root.geometry('260x130')
        lbl = Label(root, text = "Successfully deleted Hammer for this instance.\nReturning to the main window...", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid()
        root.update()
        time.sleep(3)
    #game directory chooser
    elif subwintype == 'gamedirectorypicker':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Please navigate to the folder for the \n game you want to map for.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        
        pathentrydir=StringVar(value=gamefolderpath)
        print("Okay.")
        print(gamefolderpath)
        
        pathentry = Entry(root,textvariable=pathentrydir,font=(style_font, style_fontsize),width=1)
        pathentry.grid(row=3, column=0, sticky="ew")
        
        
        browsebtn = Button(root, text = "Browse", fg=colors_primarytext, command=lambda: findgame(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=4, column=0)
        
        lbl = Label(root, text = "", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=5, column=0)
        
        browsebtn = Button(root, text = "Continue", fg=colors_primarytext, command=lambda: [checkgamepath()], bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=6, column=0)
        
        root.update()
    #game directory chooser if you frick it up
    elif subwintype == 'gamedirectorypickerinvalid':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Could not find the bin folder... \n Please use a valid game folder.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        
        pathentrydir=StringVar(value=gamefolderpath)
        print("Okay.")
        print(gamefolderpath)
        
        pathentry = Entry(root,textvariable=pathentrydir,font=(style_font, style_fontsize),width=1)
        pathentry.grid(row=3, column=0, sticky="ew")
        
        
        browsebtn = Button(root, text = "Browse", fg=colors_primarytext, command=lambda: findgame(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=4, column=0)
        
        lbl = Label(root, text = "", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=5, column=0)
        
        browsebtn = Button(root, text = "Continue", fg=colors_primarytext, command=lambda: [checkgamepath()], bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=6, column=0)
        
        root.update()
        
    #tf2 directory chooser
    elif subwintype == 'tfdirectorypicker':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "SFM requires Team Fortress 2 to be installed for setup.\nPlease navigate to your Team Fortress 2 folder.\nNote SFM IS NOT SUPPORTED RIGHT NOW!! this probably wont work.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example:\nhomefolder/.steam/steam/\nsteamapps/common/Team Fortress 2/", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        
        pathentrydir=StringVar(value=tffolderpath)
        print("Okay.")
        print(tffolderpath)
        
        pathentry = Entry(root,textvariable=pathentrydir,font=(style_font, style_fontsize),width=1)
        pathentry.grid(row=3, column=0, sticky="ew")
        
        
        browsebtn = Button(root, text = "Browse", fg=colors_primarytext, command=lambda: findtf(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=4, column=0)
        
        lbl = Label(root, text = "", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=5, column=0)
        
        browsebtn = Button(root, text = "Continue", fg=colors_primarytext, command=lambda: [checktfpath()], bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=6, column=0)
        
        root.update()
    #tf directory chooser if you frick it up   
    elif subwintype == 'tfdirectorypickerinvalid':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Could not find TF2...\nSFM requires Team Fortress 2 to be installed for setup.\nPlease re-select your Team Fortress 2 folder.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example:\nhomefolder/.steam/steam/\nsteamapps/common/Team Fortress 2/", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        
        pathentrydir=StringVar(value=tffolderpath)
        print("Okay.")
        print(tffolderpath)
        
        pathentry = Entry(root,textvariable=pathentrydir,font=(style_font, style_fontsize),width=1)
        pathentry.grid(row=3, column=0, sticky="ew")
        
        
        browsebtn = Button(root, text = "Browse", fg=colors_primarytext, command=lambda: findtf(), bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=4, column=0)
        
        lbl = Label(root, text = "", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=5, column=0)
        
        browsebtn = Button(root, text = "Continue", fg=colors_primarytext, command=lambda: [checktfpath()], bg=colors_framebackground, \
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="center", highlightthickness=0)
        browsebtn.grid(row=6, column=0)
        
        root.update()
        
    #proton set up window
    if subwintype == 'protonenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Windows bin folder not detected.\nOpen Steam and enable Proton for this game before continuing.\nYou can turn off Proton later.\n\n \
        This window should auto-detect Proton on its own.",
        bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        root.update()
        checkproton()
        
    #P2SDK set up window for portal 2
    if subwintype == 'p2sdkenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Portal 2 Authoring Tools not detected.\nOpen Steam and install Portal 2 Authoring Tools before continuing.\n\nThis \
window should auto-detect Portal 2 Authoring Tools on its own.",
        bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        root.update()
        checksdk()
    if subwintype == 'l4dsdkenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Left 4 Dead Authoring Tools not detected.\nOpen Steam and install Left 4 Dead Authoring Tools before continuing.\n\nThis \
window should auto-detect Left 4 Dead Authoring Tools on its own.",
        bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        root.update()
        checksdk()
    if subwintype == 'l4d2sdkenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Left 4 Dead 2 Authoring Tools not detected.\nOpen Steam and install Left 4 Dead 2 Authoring Tools before continuing.\n\nThis \
window should auto-detect Left 4 Dead 2 Authoring Tools on its own.",
        bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        root.update()
        checksdk()
    #hammer++ set up window if it was automated
    if subwintype == 'hammerautomated':
        #root.geometry('600x140')
        lbl = Label(root, text = "Downloading Hammer++...", bg=colors_background, \
        fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Do not close this window!", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
        autohammer(None,None)
    #hammer++ set up window if it was updated
    if subwintype == 'hammerupdate':
        #root.geometry('600x140')
        lbl = Label(root, text = "Updating Hammer++...", bg=colors_background, \
        fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Do not close this window!", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
    #hammer++ set up window THE CORRECT USED ONE
    if subwintype == 'hammerenable':
        #root.geometry('600x140')
        #Put button here to open browser
        lbl = Label(root, text = "Hammer++ could not be automatically installed. Please download it at\nhttps://ficool2.github.io/HammerPlusPlus-Website/download.html\nand copy its bin folder into:\
        \n" + gamefolderpath + "bin/",
        bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        root.update()
        checkhammer()
    #hammer++ install window
    elif subwintype == 'hammerinstall':
        #root.geometry('430x140')
        lbl = Label(root, text = "Please download Hammer++ and select the downloaded archive for it.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        # Button here
        lbl = Label(root, text = "You can install Hammer++ here:\nhttps://ficool2.github.io/HammerPlusPlus-Website/download.html", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)

        root.update()
        time.sleep(1)
        installhammer()
    #hammer++ install window if you freaked it up
    elif subwintype == 'hammerinstallinvalid':
        #root.geometry('423x140')
        lbl = Label(root, text = "Hammer++ executable not found. Did you select the correct\narchive?", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        # Button here
        lbl = Label(root, text = "You can install Hammer++ here:\nhttps://ficool2.github.io/HammerPlusPlus-Website/download.html", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(1)
        installhammer()
    #installing tools plus plus
    elif subwintype == 'toolsplusplusinstall':
        #root.geometry('260x130')
        lbl = Label(root, text = "++ compile tools are being installed and set up...\nThese are required for certain games. Please wait.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Hammer++ will start and close on its own. This is normal.", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(7)
    elif subwintype == 'editingconfigs':
        #root.geometry('260x130')
        lbl = Label(root, text = "Configuring Hammer++...", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Do not close this window!", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(1)
    elif subwintype == 'waiting':
        #root.geometry('260x130')
        lbl = Label(root, text = "Setting up...\nPlease wait.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Hammer++ may start and close on its own. This is normal.", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
        lbl.grid(row=2, column=0)
        root.update()
        time.sleep(7)
    #finishing up
    elif subwintype == 'finishingup':
        #root.geometry('260x130')
        if state_htype == False:
            lbl = Label(root, text = "Hammer++ for your game has been\nset up. You can turn Proton off\nfor this game now.\nThe main window will open again now.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        elif state_htype == True:
            lbl = Label(root, text = "Hammer for your game has been\nset up. You can turn Proton off\nfor this game now.\nThe main window will open again now.", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg=colors_background, fg=colors_secondarytext, font=(style_font, style_fontsize))
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Thanks for using Linux Hammer Launcher! ^c^", bg=colors_background, fg=colors_tertiarytext, font=(style_font, style_fontsize))
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
def launchhammer(game, title, version, lineupdate):
    stateandprint("Set Wine Theme to None")
    with open(configpath + 'prefix/user.reg', 'r') as file:
        data = file.read()
        data = data.replace('"ThemeActive"="1"', '"ThemeActive"="0"')
    with open(configpath + 'prefix/user.reg', 'w') as file:
        file.write(data)
    
    gamefolderfinder = game
    titlelowered = title.casefold()
    subwindow('hammerlaunch')
    print("length of directory is " + str(len(os.path.basename(gamefolderfinder[:-1]))))
    print("directory up one is " + gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])])
    # find game folder
    if "hammerplusplus.exe" in game:
        gamefolderfinder = gamefolderfinder[:-19]
    if "hammer.exe" in game:
        gamefolderfinder = gamefolderfinder[:-11]
    print(gamefolderfinder + " HAMMER TEXT REMOVED!")
    while os.path.basename(gamefolderfinder) != title:
        print(os.path.basename(gamefolderfinder) == title)
        gamefolderfinder = gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])][:-1]
        print(gamefolderfinder + " found!")
    print(gamefolderfinder + " found!")
    print(os.getlogin())

    version = int(version)

    if version == 0:
        print("skipping update check because hammer++ updates are disabled for this game")
    elif state_disablehppupdates == True:
        print("skipping update check because updates are disabled for all games")
    elif "hammer.exe" in game:
        print("skipping update check because this is not hammer++")
    else:
        print("checking for updates...")
        latestversion = "0"
        try:
            hammerplusplusversiontxt = "https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/refs/heads/main/version.txt"
            response = requests.get(hammerplusplusversiontxt)
            if response.status_code == 200:
                latestversion = response.text
                latestversion = int(latestversion)
                if latestversion > version:
                    openpopup("Update Detected","An update is available for Hammer++! Would you like to install it?\nInstalled Version: "+str(version)+" Latest Version: "+str(latestversion),"Yes",True,"No",False)
                    if btnresult == True:
                        subwindow('hammerupdate')
                        autohammer(gamefolderfinder,titlelowered)
                        with open(configpath + "games.txt", 'r') as file:
                            lines = file.readlines()
                            
                        lines[lineupdate] = "['" + title + "', '" + game + "', '" + str(latestversion) + "']\n"
                        print("new games.txt entry should be:")
                        print("['" + title + "', '" + game + "', '" + str(latestversion) + "']\n")
                        
                        with open(configpath + "games.txt", 'w') as file:
                            file.writelines(lines)
                        
                else:
                    print("no new version of hammer++ found. skipping'")
            else:
                print("couldn't check for hammer++ updates!")
        except:
            pass

    #game specific commands
    #hl2 shares the same bin between versions excluding a small handful of files (for only some people??) for some reason, remove bin and create new one from binwin with said files
    delcopybins = ['half-life 2', 'left 4 dead']
    mergecopybins = ['portal', 'portal 2', 'half-life 1 source deathmatch', 'left 4 dead 2', 'black mesa']
    
    if titlelowered in delcopybins:
        if os.path.isdir(gamefolderfinder + "/bin/"):
            os.system("rm -r '" + gamefolderfinder + "/bin/'")
        print("cp -r '" + gamefolderfinder + "/binwin/' '" + gamefolderfinder + "/bin/'" )
        os.system("cp -r '" + gamefolderfinder + "/binwin/' '" + gamefolderfinder + "/bin/'" )
    elif titlelowered in mergecopybins:
        print("cp -r '" + gamefolderfinder + "/binwin/'* '" + gamefolderfinder + "/bin/'" )
        os.system("cp -r '" + gamefolderfinder + "/binwin/'* '" + gamefolderfinder + "/bin/'" )
    
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

    closelauncher()

    cleantemp()

    #launch wine9 with hammer using correct prefix
    print('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    os.system('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    root.quit()

def clicked():
    print("clicked!")
    





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
    global hammer_gameconfiglocation

    print("game folder path is " + gamefolderpath)

    print("using binfolder "  + binfolder)
    combi3paths = gamefolderpath + binfolder + bintype

    # auto delete binwin if it already exists (though this might mess up user data. open dialog to ask user?)
    if os.path.exists(gamefolderpath + "binwin") == True:
        print("BINWIN ALREADY EXISTS! deleting...")
        os.system("rm -r '" + gamefolderpath + "binwin/'")

    # make the binwin directory early. why? just in case binfolder is binwin. im not thinking at the moment and i'm really stpudiffsoifdsuaoifpifjfajhdskflkhajfds. this is literally just here for hl1mp
    os.mkdir(gamefolderpath + "binwin/")

    # create dummy bat
    batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
    batfile.write('@echo off\n\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
    batfile.close()

    #check for steam. if find steam make bat for game launching!! if not. too bad. fool
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
            batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
            batfile.write('@echo off\nstart /unix ' + steampath[:-1] +' steam://rungameid/' + str(game_appid) + '//"%3 %4"\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
            batfile.close()
        else:
            print("steam_appid missing from game directory!")
    else:
        print("could not find steam. flatpak moment!")

    #copy bin folder to binwin
    print("copying binwin")
    print(gamename)
    print("cp -r '" + gamefolderpath + "bin/.' '" + gamefolderpath + "binwin/'")
    if gamename == "game":
        print("doing sfm copy")
        os.system("cp -r '" + tffolderpath + "bin/.' '" + gamefolderpath + "binwin/'")
    else:
        os.system("cp -r '" + gamefolderpath + "bin/.' '" + gamefolderpath + "binwin/'")



    if state_htype == True:
        hammer_gameconfiglocation = "/GameConfig.txt"
        hammer_exelocation = "/hammer.exe"
    elif state_htype == False:
        hammer_exelocation = "/hammerplusplus.exe"
        hammer_gameconfiglocation = "/hammerplusplus/hammerplusplus_gameconfig.txt"
 
    #gameconfig & settings generation
    timeout_time = 10

    #create a .sh file to run, timeout doesnt like WINEPREFIX= being there.
    #i do not know why sfm is trying to use a bash file to run. i dont need to know why as long as this works. sfm has its gameconfig made from scratch there is zero reason for it to launch
    #hammer
    
    cleantemp()

    print(gamefolderpath + "IS IT SFM????")
    if gamename == "game":
        print("please for the love of god stop using the sh file you dont need it sfm. why are we even generating them like this anymore anyways we have a thing to make them from scratch now is there\
    any point in using such a jank system still whyd i make it like this")
        print("idk :3")
    else:
        bashfile = open(configpath + "/temp/temprunhammerbash.sh", "w")
        print("'WINEPREFIX="' + configpath + prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + hammer_exelocation + '"')
        bashfile.write('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + hammer_exelocation + '"')
        bashfile.close()
        os.system("chmod +x " + configpath + "/temp/temprunhammerbash.sh")
        #keep starting hammer for increasing amounts of time until gameconfig is generated
        #this whole system should probably be changed to just be a fallback option for when a game is run that we havent defined in the gameconfigmaker
        #while os.path.isfile(combi3paths + hammer_gameconfiglocation) == False:
        print("timeout " + str(timeout_time) + " " + configpath + "/temp/temprunhammerbash.sh")
        os.system("timeout " + str(timeout_time) + " " + configpath + "/temp/temprunhammerbash.sh")
        timeout_time += 5
        root.update()
        cleantemp()
    #all this should only frickig do when the file exists god
    if os.path.isfile(combi3paths + hammer_gameconfiglocation) == True:
        subwindow("editingconfigs")
        if plusplusconfig == True:
            #edit gameconfig for hammer
            print("modifiying gameconfig for "  + binfolder)
            print(combi3paths + hammer_gameconfiglocation)
            #vbsp
            with open(combi3paths + hammer_gameconfiglocation, 'r') as file:
                data = file.read()
                data = data.replace("\\vbsp.exe", "\\vbspplusplus.exe")
            with open(combi3paths + hammer_gameconfiglocation, 'w') as file:
                file.write(data)
            #vvis
            with open(combi3paths + hammer_gameconfiglocation, 'r') as file:
                data = file.read()
                data = data.replace("\\vvis.exe", "\\vvisplusplus.exe")
            with open(combi3paths + hammer_gameconfiglocation, 'w') as file:
                file.write(data)
            #vrad
            with open(combi3paths + hammer_gameconfiglocation, 'r') as file:
                data = file.read()
                data = data.replace("\\vrad.exe", "\\vradplusplus.exe")
            with open(combi3paths + hammer_gameconfiglocation, 'w') as file:
                file.write(data)
        #binwin, if HL2 or any other game that cant run from binwin, dont config this.
        if binfolder == "binwin/":
            with open(combi3paths + hammer_gameconfiglocation, 'r') as file:
                data = file.read()
                data = data.replace("\\bin\\", "\\binwin\\")
            with open(combi3paths + hammer_gameconfiglocation, 'w') as file:
                file.write(data)

            #update settings.ini for people who already have used hammerplusplus before
            if os.path.exists(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini") == True:
                with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'r') as file:
                    data = file.read()
                    data = data.replace("\\bin\\", "\\binwin\\")
                with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'w') as file:
                    file.write(data)

        #create win version of gamefolderpath
        gamefolderwindowified = "Z:" + os.path.realpath(gamefolderpath).replace("/", "\\")
        binfolderwindowified = binfolder.replace("/","\\")
        bintypewindowified = bintype.replace("/","\\")
        print("printing game folder windowified as real path")
        print(os.path.realpath(gamefolderwindowified))
        print(binfolderwindowified)
        
        
        
        #set map vmf directory in config. check for picky map locations per hammer and config (like portal 2)
        print("THE LINE NUMS TO REPLACE ARE:")
        linestoconfig = (find_gameexe_line_numbers(combi3paths + hammer_gameconfiglocation, '"MapDir"'))
        for i in range(len(linestoconfig)):
            with open(combi3paths + hammer_gameconfiglocation, 'r', encoding='utf-8') as gameconffile:
                lines = gameconffile.readlines()
            if gamename == "portal 2":
                lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\sdk_content\\maps"\n'
            elif gamename == "left 4 dead 2":
                lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\left4dead2\\maps"\n'
            else:
                if state_usemapsrc == True:
                    lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\mapsrc"\n'
                elif state_usemapsrc == False:
                    print("MapSRC disabled. Using vanilla path!")
                    with open(file=os.path.dirname(__file__)+"/assets/gamemappaths.txt") as mappathfile:
                        maplines = mappathfile.readlines()
                    correctmapline = "na"
                    for itwothesequel in range(len(maplines)):
                        if gamename + " : " in maplines[itwothesequel]:
                            print(maplines)
                            correctmapline = maplines[itwothesequel]
                            
                    if correctmapline == "na":
                        print(maplines)
                        print(gamename)
                        print("GAME MAPS FOLDER NOT CONFIGGED!! using MapSRC!")
                        lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + '\\mapsrc"\n'
                    else:
                        print('				"MapDir"		"' + gamefolderwindowified + correctmapline[len(gamename) + 3:] + '"')
                        print(linestoconfig)
                        lines[linestoconfig[i] - 1] = '				"MapDir"		"' + gamefolderwindowified + correctmapline[len(gamename) + 3:]
                            
                    
                    
            with open(combi3paths + hammer_gameconfiglocation, 'w') as gameconffile:
                gameconffile.writelines(lines)
                
                
        
        #set gameExe to .bat
        linestoconfig = (find_gameexe_line_numbers(combi3paths + hammer_gameconfiglocation, '"GameExe"'))
        for i in range(len(linestoconfig)):
            with open(combi3paths + hammer_gameconfiglocation, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            lines[linestoconfig[i] - 1] = '				"GameExe"		"' + gamefolderwindowified + "\\" + binfolderwindowified + 'linuxhammerlauncher_rungame.bat"\n'
            with open(combi3paths + hammer_gameconfiglocation, 'w') as file:  
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
    print("GUhX2")
    print(gamename)
    if state_htype == False:
        if gamename == "team fortress 2 classified":
            gameconfigmake("tf2c")
        if gamename == "half-life 1 source deathmatch":
            gameconfigmake("hl1mp")
        if gamename == "game":
            print("A SINGULAR 'GUH' SO I KNOW WHERE THIS IS")
            os.system("cp -rv --update=none '" + tffolderpath + "hl2/' '" + gamefolderpath + "'")
            print("cp -rv --update=none '" + tffolderpath + "hl2/' '" + gamefolderpath + "'")
            gameconfigmake("sfm")
        if gamename == "half-life 2 deathmatch":
            gameconfigmake("hl2mp")
            
    elif state_htype == True:
        if gamename == "left 4 dead":
            gameconfigmake("l4d")
            os.system("cp -r '" + gamefolderpath + "bin/GameConfig.txt' '" + gamefolderpath + "binwin/'")
        
            
    
    #create mapsrc folder for game
    print(os.path.basename(gamefolderpath[:-1]) + "UGH COME ON")
    print(gamefolderpath + "mapsrc/")
    #this stupid thing doesnt like ors it wont create the folder at all if they are there and i dont feel like setting up an if in list thing rn its 5am
    if gamefolderpath[:-1] == "Portal 2":
        pass
    else:
        if os.path.exists(gamefolderpath + "mapsrc/") == False:
            os.mkdir(gamefolderpath + "mapsrc/")

#create a gameconfig
def gameconfigmake(game):
    global bintypewindowified
    global gamefolderwindowified
    global gamefolderpath
    global gamename
    global combi3paths
    global binfolderwindowified
    global hammer_gameconfiglocation
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
    if game == "l4d":
        codename = "left4dead"
        fgdname = "left4dead"
        pluspluscomp = ""
        
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
    with open(combi3paths + hammer_gameconfiglocation, 'w') as hppgameconfigfile:
        hppgameconfigfile.write(hammerconfig)
        
    #set gameexe
    print("THE LINE NUMS TO REPLACE ARE:")
    linestoconfig = (find_gameexe_line_numbers(combi3paths + hammer_gameconfiglocation, '"GameExe"'))
    for i in range(len(linestoconfig)):
        with open(combi3paths + hammer_gameconfiglocation, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines[linestoconfig[i] - 1] = '				"GameExe"		"' + gamefolderwindowified + "\\" + binfolderwindowified + 'linuxhammerlauncher_rungame.bat"\n'
        with open(combi3paths + hammer_gameconfiglocation, 'w') as file:
            file.writelines(lines)
    




def downloadwine():
    file_Path = configpath + 'runner/wine-9.0.1.tar.zst'
    wine9url = "https://archive.archlinux.org/packages/w/wine/wine-9.0-1-x86_64.pkg.tar.zst"
    #check if wine9 exists in runner folder, if it does not them download from arch repo (will work on any distro i think??????)
    stateandprint("Checking if Wine 9 exists.")
    print(os.path.exists(configpath + "runner/wine-9.0.1/"))
    if os.path.exists(configpath + "runner/wine-9.0.1/") == False:
        #download wine9
        stateandprint("Downloading Wine 9.0.1")
        
        try:
            response = requests.get(wine9url)
            if response.status_code == 200:
                with open(file_Path, 'wb') as file:
                    file.write(response.content)
                stateandprint("Downloaded Wine 9.0.1!")
            else:
                stateandprint("Failed to download Wine 9. \n Check your internet connection?")
                openpopup("Failed to download Wine 9.","Failed to download Wine 9.\nTry checking your internet connection?",\
			"Retry download",True,"Exit to menu",False)
                if btnresult == True:
                    downloadwine()
                else:
                    startmainwindow()
        except:
            stateandprint("Failed to download Wine 9. +2 \n Check your internet connection?")
            openpopup("Failed to download Wine 9.","Failed to download Wine 9.\nTry checking your internet connection?",\
			"Retry download",True,"Exit to menu",False)
            if btnresult == True:
                downloadwine()
            else:
                startmainwindow()
                
    #extract wine9 targz
        stateandprint("Downloaded Wine 9.0.1! \nExtracting Wine...")
        os.system("cd " + configpath + "runner/" + " && tar --use-compress-program=unzstd -xvf " + configpath + "runner/wine-9.0.1.tar.zst")
        #rename extracted wine files from usr to wine-9.0.1
        stateandprint("Naming wine folder... \n Deleting downloaded archive...")
        os.system("mv " + configpath + "runner/usr/" + " " + configpath + "runner/wine-9.0.1/")
        #remove archive
        if os.path.exists(configpath + "runner/wine-9.0.1.tar.zst") == True:
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
    global backupgamename
    global gameconfig
    backupgamefolderpath = "na"
    gamefolderpath = ""
    tffolderpath = ""
    
    subwindow('winesetup')
    downloadwine()
    #remove links to homedir.. we should still hold off on having a delete prefix button because these are just what links winecfg listed, im not sure if more lie around 
    #the prefix still
    print('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Music"')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/AppData/Roaming/Microsoft/Windows/Templates"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/AppData/Roaming/Microsoft/Windows/Templates') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/AppData/Roaming/Microsoft/Windows/Templates')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Music"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Music') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Music')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Desktop"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Desktop') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Desktop')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Documents"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Documents') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Documents')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Downloads"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Downloads') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Downloads')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Pictures"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Pictures') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Pictures')
    os.system('unlink "' + configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Videos"')
    if os.path.exists(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Videos') == False:
        os.mkdir(configpath + 'prefix/drive_c/users/' + os.getlogin() + '/Videos')
    print("unlinked default symlinks in wineprefix user folder!")
    
    if settinguphammer == 0:
        settinguphammer = 1
        
            
        #install DXVK
        stateandprint("Installing DXVK")
        os.system('WINEPREFIX="' + configpath + 'prefix/" winetricks dxvk2030')
        stateandprint("Installed DXVK! unless it didnt")
    setuphammer_askgame()
        
        
        
def setuphammer_askgame():
    global tffolderpath
    global settinguphammer
    global root
    global gamefolderpath
    global gamename
    global backupgamefolderpath
    global backupgamename
    global gameconfig
    backupgamefolderpath = "na"

    #ask user for path to game
    freetocontinue = 0
    subwindow('gamedirectorypicker')
    
    
    
def setuphammer_part2():
    global tffolderpath
    global settinguphammer
    global root
    global gamefolderpath
    global gamename
    global backupgamefolderpath
    global backupgamename
    global gameconfig
    backupgamefolderpath = "na"

    os.system("echo this is echoed with os plugin")
    gamename = os.path.basename(gamefolderpath[:-1]).casefold()
    print("gamefolderpath namified is " + os.path.basename(gamefolderpath[:-1]).casefold())
    print("gamename is " + gamename)
    
    if gamename == "game":
        print("SFM IS USED")
        backupgamefolderpath = gamefolderpath
        backupgamename = gamename
    else:
        backupgamename = "na"

    # IMPORTANT REMINDER: "game" is SFM!!!!!!!!!!!!!!

    #check if sfm is being used and ask for tf2 install
    if gamename == "game":
        print(tffolderpath)
    elif gamename == "portal 2":
        #check if portal 2 is used, ask for enable proton and sdk
        subwindow('protonenable')
        subwindow('p2sdkenable')
    elif gamename == "left 4 dead":
        #check if l4d is used, ask for enable proton and sdk
        subwindow('protonenable')
        subwindow('l4dsdkenable')
    elif gamename == "left 4 dead 2":
        #check if l4d2 is used, ask for enable proton and sdk
        subwindow('protonenable')
        subwindow('l4d2sdkenable')
    else:
        #check if proton is enabled, if not, prompt user to enable proton before continuing. check hammer usually, but some game specific checks (like hl2 and tier0.dll) are needed
        subwindow('protonenable')

    #only install ++ hammer if hammer++ isnt disabled
    if state_htype == False:
        #check for hammerplusplus
        subwindow('hammerautomated')
    subwindow('hammerenable')
    subwindow('waiting')
    print("checking for hammer")

    # HL1MP does not have a built in gameinfo. why? no idea.
    if gamename == "half-life 1 source deathmatch":
        print("COPYING HL1MP TXT")
        print("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderpath + "hl2/gameinfo.txt'")
        os.system("cp '" + os.path.dirname(__file__) + "/assets/gameinfo/hl1mp.txt' '" + gamefolderpath + "hl2/gameinfo.txt'")
    
    #only install ++ tools if hammer++ isnt disabled
    if state_htype == False:
        #install plusplus tools, some games dont work for this
        noplusplus = ['portal 2', 'half-life 2', 'portal', 'garrysmod']
        if gamename not in noplusplus:
            try:
                subwindow("toolsplusplusinstall")
                
                file_Path = configpath + 'temp/tools_plusplus.zip'
                tools_plusplusurl = "https://github.com/ficool2/misc_tools/releases/download/v1/tools_plusplus.zip"
                
                print("Downloading Tools ++")
                response = requests.get(tools_plusplusurl)
                if response.status_code == 200:
                    with open(file_Path, 'wb') as file:
                        file.write(response.content)
                    stateandprint("Downloaded Tools++!")
                else:
                    stateandprint("Failed to download Tools++. \n Check your internet connection?")
                    openpopup(\
                    "Could Not Install Tools++","Tools++ could not be installed. \nThese are required for certain games like Team Fortress 2 to compile.\
\nMake sure to manually install them later if your game requires it.","Continue",True,"",False)
                if btnresult == True:
                    pass
            except:
                openpopup(\
                "Could Not Install Tools++","Tools++ could not be installed. \nThese are required for certain games like Team Fortress 2 to compile.\
\nMake sure to manually install them later if your game requires it.","Continue",True,"",False)
                if btnresult == True:
                    pass
            
            if btnresult != True:
                print("copying tools files to bin")
                print("cd " + configpath + "temp/ && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "temp/tools_plusplus/tools/'* '" + gamefolderpath + "bin/" + bintype + "/'")
                os.system("cd " + configpath + "temp/ && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "temp/tools_plusplus/tools/'* '" + gamefolderpath + "bin/" + bintype + "/'")
        else:
            subwindow("waiting")
            time.sleep(10)

    cleantemp()

    if backupgamename == "game":
        print("switching back to sfm paths")
        print(backupgamefolderpath)
        print(backupgamename)
        gamefolderpath = backupgamefolderpath
        gamename = backupgamename

    # it's probably better to do this when the launcher starts to check for duplicates for all games. But Whatever................ this works! kinda.
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
    
    try:
        version = "1"
        hammerplusplusversiontxt = "https://raw.githubusercontent.com/ficool2/HammerPlusPlus-Website/refs/heads/main/version.txt"
        response = requests.get(hammerplusplusversiontxt)
        if response.status_code == 200:
            version = response.text
    except:
        version = "8871"
        print("couldnt get version number from online")

    #game specific configuring.
    noupdate = ['csgo legacy','counter-strike global offensive']
    if gamename in noupdate:
        print("not autoupdating this hammer++")
        version = "0"
        
    if state_htype == False:
        hammerexe = "hammerplusplus.exe"
    elif state_htype == True:
        hammerexe = "hammer.exe"
        version = "1"
    
    
    

    print("backupgamefolderpath is")
    print(backupgamefolderpath)
    
    
    nobinwin = ['half-life 2','portal','portal 2', 'left 4 dead 2', 'black mesa' , 'left 4 dead']
    if gamename in nobinwin:
        gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/" + hammerexe + "', '"+version+"']" + "\n"
        if os.path.exists(gamefolderpath + "bin/GameConfig.txt") == True:
            os.remove(gamefolderpath + "bin/GameConfig.txt")
        hammerconfig("bin/", False) #second value is for whether or not to config ++ tools
        os.system("cp '" + gamefolderpath + "bin/hammerplusplus/hammerplusplus_gameconfig.txt' '" + gamefolderpath + "binwin/hammerplusplus/hammerplusplus_gameconfig.txt'")
    elif gamename == "half-life 1 source deathmatch":
        gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/" + hammerexe + "', '"+version+"']" + "\n"
        if os.path.exists(gamefolderpath + "bin/GameConfig.txt") == True:
            os.remove(gamefolderpath + "bin/GameConfig.txt")
        hammerconfig("bin/", True)
        os.system("cp '" + gamefolderpath + "bin/hammerplusplus/hammerplusplus_gameconfig.txt' '" + gamefolderpath + "binwin/hammerplusplus/hammerplusplus_gameconfig.txt'")
    elif gamename == "game":
        gamedefinition = "['SourceFilmmaker', '" + gamefolderpath + "binwin/" + bintype + "/" + hammerexe + "', '"+version+"']" + "\n"
        hammerconfig("binwin/", True)
    else:
        gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "binwin/" + bintype + "/" + hammerexe + "', '"+version+"']" + "\n"
        hammerconfig("binwin/", True)
    
    
        
    gameconfig.write(gamedefinition)
    print(gamedefinition)
    gameconfig.close() 
    
    cleantemp()
    
    #show finishing up window
    subwindow('finishingup')
    
    #make button clickable
    settinguphammer = 0
    #go back to main window
    startmainwindow()
        
#.config/linuxhammerlauncher/






'''
Non GUI functions ^^
'''




'''
GUI function stuffs
'''


#makes game button
def creategamebutton(height, title, hammerpath, version, mode):
    #set icon for game
    titlelowered = title.casefold()
    if style_showicons == True:
        gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/sdk_hammer.png")
        if titlelowered == "garrysmod":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/garrysmod.png")
        elif titlelowered == "left 4 dead 2":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/l4d2.png")
        elif titlelowered == "left 4 dead":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/l4d.png")
        elif titlelowered == "black mesa":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/bms.png")
        elif titlelowered == "portal 2":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/portal2.png")
        elif titlelowered == "portal":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/portal.png")
        elif titlelowered == "counter-strike source":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/cstrike.png")
        elif titlelowered == "counter-strike global offensive":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/csgo.png")
        elif titlelowered == "day of defeat source":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/dod.png")
        elif titlelowered == "half-life 2":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/hl2.png")
        elif titlelowered == "sourcefilmmaker":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/sfm.png")
        elif titlelowered == "team fortress 2":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/tf2.png")
        elif titlelowered == "team fortress 2 classified":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/tf2classified.png")
        elif titlelowered == "half-life 1 source deathmatch":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/hl1mp.png")
        elif titlelowered == "half-life 2 deathmatch":
            gameicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/games/hl2mp.png")
        gameicn = Label(optionsframe, bg=colors_framebackground, image=gameicon, anchor="e")
        gameicn.image = gameicon
        gameicn.grid(row=height, column=0, sticky="ew")

    if "hammer.exe" in hammerpath:
        print("VANILLA HAMMER DETECTED")
        htypeindicatoricon = Image("photo", file=os.path.dirname(__file__)+style_graphicspath+"hammertype_vanilla.png")
        htypeicn = Label(optionsframe, bg=colors_framebackground, image=htypeindicatoricon, anchor="e")
        htypeicn.image = htypeindicatoricon
        htypeicn.grid(row=height, column=0, sticky="ew")

    
    #create functional button
    gamesline = height - 3
    if mode == "run":
        btn = Button(optionsframe, text = title , fg=colors_primarytext, command=lambda: launchhammer(hammerpath, title, version, gamesline), bg=colors_framebackground,
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
        btn.grid(row=height, column=1,sticky="ew")
    elif mode == "del":
        btn = Button(optionsframe, text = title , fg=colors_primarytext, command=lambda: deletehammer(hammerpath, title, version, gamesline), bg=colors_framebackground,
        activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
        btn.grid(row=height, column=1,sticky="ew")
    
    
        


def startmainwindow():
    global root
    global optionsframe
    
    root.destroy()
    root = Tk()
    mainwindow()
    rendermainwindow()
    
    

launched = 0


def rendermainwindow():
    global optionsframe
    global root
    global launched
    
    launched += 1
    
    root.configure(bg=colors_background)

    padding = Frame(root, bg=colors_background, relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=0,sticky="w")

    '''
    Frame creation
    '''
    optionsframe = Frame(root, bg=colors_framebackground, relief=style_frameborder, bd=1, highlightthickness=0)
    optionsframe.grid(row=1, column=1,sticky="we")
    optionsframe.grid_columnconfigure(0, minsize=23, weight=0)
    optionsframe.grid_columnconfigure(1, minsize=211, weight=1)
    '''
    frame creation ^^
    '''
    padding = Frame(root, bg=colors_background, relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=2,sticky="e")

    linenum = 0
    #create game buttons based on game defs
    gameconfig = open(configpath + "games.txt", 'r')
    
    # lines to print (or not to print this list just kinda needs to be here regardless of how little it accomplishes
    specified_lines = [99]


    bannerimage = Image("photo", file=os.path.dirname(__file__)+style_bannerimage)
    bannerimg = Label(root, bg=colors_background, image=bannerimage, anchor="center")
    bannerimg.image = bannerimage
    if style_bannerposition == "bottom":
        bannerimg.grid(row=2, column=1, sticky="ew")
    elif style_bannerposition == "top":
        bannerimg.grid(row=0, column=1, sticky="ew")
    
    
    #editors title
    setuptext = Label(optionsframe, text = "HAMMER EDITORS", fg=colors_headertext, bg=colors_framebackground, justify="left",font=(style_headerfont, style_headerfontsize, style_headerfontstyle), anchor="sw", height=2,  highlightthickness=0)
    setuptext.grid(row=0, column=1, sticky="ew")
    
    if style_forceheadercaps == False:
        setuptext = setuptext.config(text = setuptext.cget("text").title())
    if style_showdividers == True:
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
        version = "0"
        try:
            version = json.loads(currentgamedef.replace("'", '"'))[2]
        except:
            print("DANGER! "+json.loads(currentgamedef.replace("'", '"'))[0]+" IS MISSING A VERSION NUMBER FOR HAMMER++! UPDATES HAVE BEEN DISABLED FOR THAT GAME.")
        creategamebutton(linenum + 3, json.loads(currentgamedef.replace("'", '"'))[0], json.loads(currentgamedef.replace("'", '"'))[1],version,"run")
        linenum += 1
    gameconfig.close()
    
    


        
    '''
    GUI Stuffs
    '''

    #UTILITIES
    
    setuptext = Label(optionsframe, text = "UTILITIES", fg=colors_headertext, bg=colors_framebackground, justify="left",font=(style_headerfont, style_headerfontsize, style_headerfontstyle), anchor="sw", height=2, highlightthickness=0)
    setuptext.grid(row=linenum+4, column=1, sticky="ew")
    
    if style_forceheadercaps == False:
        setuptext = setuptext.config(text = setuptext.cget("text").title())
    if style_showdividers == True:
        divider = Frame(optionsframe,bg='#282e22',height=2)
        divider.grid(row=linenum+5, column=0,sticky="ew")
        divider = Frame(optionsframe,bg='#282e22',height=2)
        divider.grid(row=linenum+5, column=1,sticky="ew")
    
    if style_showicons == True:
        hammericon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/sdk_setup.png")
        setupicn = Label(optionsframe, bg=colors_framebackground, image=hammericon, anchor="e")
        setupicn.image = hammericon #the fact that you have to do this just to keep an image alive is extremely stupid dumb dumb stupid dumb stupid. stupid face
        setupicn.grid(row=linenum+6, column=0, sticky="ew")
    #set up button
    setupbtn = Button(optionsframe, text = "Set up Hammer", fg=colors_primarytext, command=lambda: setuphammer(), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    #settings button
    if style_showicons == True:
        settingsicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/sdk_reset.png")
        settingsicn = Label(optionsframe, bg=colors_framebackground, image=settingsicon, anchor="e")
        settingsicn.image = settingsicon #see above
        settingsicn.grid(row=linenum+7, column=0, sticky="ew")
        


    settingsbtn = Button(optionsframe, text = "Settings", fg=colors_primarytext, command=lambda: startsettingswindow(), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    #delete button
    if style_showicons == True:
        deleteicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/sdk_delete.png")
        deleteicn = Label(optionsframe, bg=colors_framebackground, image=deleteicon, anchor="e")
        deleteicn.image = deleteicon
        deleteicn.grid(row=linenum+8, column=0, sticky="ew")
    deletebtn = Button(optionsframe, text = "Delete Hammer", fg=colors_primarytext, command=lambda: opendeletemodeconfirm(), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)

    
    setupbtn.grid(row=linenum+6, column=1, sticky="ew")
    settingsbtn.grid(row=linenum+7, column=1, sticky="ew")
    deletebtn.grid(row=linenum+8, column=1, sticky="ew")


    #CREDITS
    setuptext = Label(optionsframe, text = "CREDITS", fg=colors_headertext, bg=colors_framebackground, justify="left",font=(style_headerfont, style_headerfontsize, style_headerfontstyle), anchor="sw", height=2, highlightthickness=0)
    setuptext.grid(row=linenum+9, column=1, sticky="ew")
    
    if style_forceheadercaps == False:
        setuptext = setuptext.config(text = setuptext.cget("text").title())
    if style_showdividers == True:
        divider = Frame(optionsframe,bg='#282e22',height=2)
        divider.grid(row=linenum+10, column=0,sticky="ew")
        divider = Frame(optionsframe,bg='#282e22',height=2)
        divider.grid(row=linenum+10, column=1,sticky="ew")
    
    if style_showicons == True:
        endericon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/credit_end.png")
        crediticn = Label(optionsframe, bg=colors_framebackground, image=endericon, anchor="e")
        crediticn.image = endericon #see above
        crediticn.grid(row=linenum+11, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "EnderCatCore", fg=colors_primarytext, command=lambda: webbrowser.open("https://endercatcore.neocities.org",new=2, autoraise=True), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+11, column=1, sticky="ew")
    
    if style_showicons == True:
        tamasicon = Image("photo", file=os.path.dirname(__file__)+"/assets/buttonicons/credit_tam"+tamarand+".png")
        crediticn = Label(optionsframe, bg=colors_framebackground, image=tamasicon, anchor="e")
        crediticn.image = tamasicon #see above
        crediticn.grid(row=linenum+12, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "Tamasina", fg=colors_primarytext, command=lambda: webbrowser.open("https://tamasina.com",new=2, autoraise=True), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+12, column=1, sticky="ew")

    dummy = Frame(root,bg=colors_background,height=5)
    dummy.grid(sticky="w")
    
    if launched == 1:
        checkdependencies()

def opendeletemodeconfirm():
    openpopup("Delete Hammer","You are about to enter delete mode!!\nAre you sure you wish to continue?","Continue",True,"Cancel",False)
    if btnresult == True:
        startdeletewindow()
    else:
        pass


def startdeletewindow():
    global root
    global optionsframe
    
    root.destroy()
    root = Tk()
    mainwindow()
    renderdelwindow()


def renderdelwindow():
    global optionsframe
    global root

    
    root.configure(bg=colors_background)

    padding = Frame(root, bg=colors_background, relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=0,sticky="w")

    '''
    Frame creation
    '''
    optionsframe = Frame(root, bg=colors_framebackground, relief=style_frameborder, bd=1, highlightthickness=0)
    optionsframe.grid(row=1, column=1,sticky="we")
    optionsframe.grid_columnconfigure(0, minsize=23, weight=0)
    optionsframe.grid_columnconfigure(1, minsize=211, weight=1)
    '''
    frame creation ^^
    '''
    padding = Frame(root, bg=colors_background, relief='flat', bd=0, highlightthickness=0)
    padding.grid(row=1, column=2,sticky="e")

    linenum = 0
    #create game buttons based on game defs
    gameconfig = open(configpath + "games.txt", 'r')
    
    # lines to print (or not to print this list just kinda needs to be here regardless of how little it accomplishes
    specified_lines = [99]



    lbl = Label(root, text = "YOU ARE IN DELETE MODE!!!!!", bg=colors_background, fg=colors_primarytext, font=(style_font, style_fontsize))
    lbl.grid(row=2, column=1)
    settingsbackbtn = Button(root, text = "Exit Delete Mode", fg=colors_primarytext, command=lambda: startmainwindow(), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="w", highlightthickness=0)
    settingsbackbtn.grid(row=3, column=1, pady=10)
    

    
    #editors title
    setuptext = Label(optionsframe, text = "CHOOSE A HAMMER EDITOR TO DELETE", fg=colors_headertext, bg=colors_framebackground, justify="left",font=(style_headerfont, style_headerfontsize, style_headerfontstyle), anchor="sw", height=2,  highlightthickness=0)
    setuptext.grid(row=0, column=1, sticky="ew")
    
    if style_forceheadercaps == False:
        setuptext = setuptext.config(text = setuptext.cget("text").title())
    if style_showdividers == True:
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
        version = "0"
        try:
            version = json.loads(currentgamedef.replace("'", '"'))[2]
        except:
            print("DANGER! "+json.loads(currentgamedef.replace("'", '"'))[0]+" IS MISSING A VERSION NUMBER FOR HAMMER++! UPDATES HAVE BEEN DISABLED FOR THAT GAME.")
        creategamebutton(linenum + 3, json.loads(currentgamedef.replace("'", '"'))[0], json.loads(currentgamedef.replace("'", '"'))[1],version,"del")
        linenum += 1
    gameconfig.close()
    
    


        
    '''
    GUI Stuffs
    '''





def startsettingswindow():
    global root
    global optionsframe
    
    root.destroy()
    root = Tk()
    mainwindow()
    rendersettingswindow()



def rendersettingswindow():
    global optionsframe
    global root
    root.configure(bg=colors_framebackground)

    #use vanilla hammer
    hammertypeicon = Image("photo", file=os.path.dirname(__file__)+style_graphicspath+"tick_"+str(state_htype).lower()+".png")
    hammertypeicn = Label(root, bg=colors_framebackground, image=hammertypeicon, anchor="e")
    hammertypeicn.image = hammertypeicon
    hammertypebtn = Button(root, text = "Use vanilla Hammer in setup*", fg=colors_primarytext, command=lambda: togglesettingstate("htype"), bg=colors_framebackground, \
    activebackground=colors_framebackground, highlightbackground=colors_framebackground,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    hammertypebtn.grid(row=1, column=1, sticky="ew")
    hammertypeicn.grid(row=1, column=0, sticky="ew")
    
    #disable updates
    updatedisableicon = Image("photo", file=os.path.dirname(__file__)+style_graphicspath+"tick_"+str(state_disablehppupdates).lower()+".png")
    updatedisableicn = Label(root, bg=colors_framebackground, image=updatedisableicon, anchor="e")
    updatedisableicn.image = updatedisableicon
    updatedisablebtn = Button(root, text = "Disable Hammer++ auto updates", fg=colors_primarytext, command=lambda: togglesettingstate("disableupdates"), bg=colors_framebackground, \
    activebackground=colors_framebackground, highlightbackground=colors_framebackground,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    updatedisablebtn.grid(row=2, column=1, sticky="ew")
    updatedisableicn.grid(row=2, column=0, sticky="ew")
    
    
    #use mapsrc folder
    mapsrcuseicon = Image("photo", file=os.path.dirname(__file__)+style_graphicspath+"tick_"+str(state_usemapsrc).lower()+".png")
    mapsrcuseicn = Label(root, bg=colors_framebackground, image=mapsrcuseicon, anchor="e")
    mapsrcuseicn.image = mapsrcuseicon
    mapsrcusebtn = Button(root, text = "Use 'mapsrc' folder instead of 'maps' folder*", fg=colors_primarytext, command=lambda: togglesettingstate("mapsrcfolderuse"), bg=colors_framebackground, \
    activebackground=colors_framebackground, highlightbackground=colors_framebackground,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    mapsrcusebtn.grid(row=3, column=1, sticky="ew")
    mapsrcuseicn.grid(row=3, column=0, sticky="ew")
    
    
    #theme
    themenumicon = Image("photo", file=os.path.dirname(__file__)+"/assets/graphics/theme_"+themenames[state_theme].lower()+".png")
    themenumicn = Label(root, bg=colors_framebackground, image=themenumicon, anchor="e")
    themenumicn.image = themenumicon
    themenumbtn = Button(root, text = "Current Theme: " + themenames[state_theme], fg=colors_primarytext, command=lambda: togglesettingstate("themeswitch"), bg=colors_framebackground, \
    activebackground=colors_framebackground, highlightbackground=colors_framebackground,activeforeground='white', relief="flat", font=(style_font, style_fontsize), borderwidth=0, anchor="w", highlightthickness=0)
    themenumbtn.grid(row=4, column=1, sticky="ew")
    themenumicn.grid(row=4, column=0, sticky="ew")
    
    
    #alert
    lbl = Label(root, text = "Options followed by a '*' only apply during Hammer setup.", bg=colors_framebackground, fg=colors_tertiarytext, font=(style_font, style_fontsize))
    lbl.grid(row=10, column=1, sticky="w", pady=(7, 10))
    
    
    #back
    settingsbackbtn = Button(root, text = "Back", fg=colors_primarytext, command=lambda: startmainwindow(), bg=colors_framebackground, \
    activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="w", highlightthickness=0)
    settingsbackbtn.grid(row=11, column=1, sticky="w")
    

#setting tick toggle
def togglesettingstate(statetomodif):
    global state_htype
    global state_disablehppupdates
    global state_theme
    global state_usemapsrc
    
    if statetomodif == "htype":
        state_htype = toggle_bool(state_htype)
        print("HTYPE CHANGED: "+str(state_htype))
        rendersettingswindow()
    elif statetomodif == "disableupdates":
        state_disablehppupdates = toggle_bool(state_disablehppupdates)
        print("DISABLEUPDATES CHANGED: "+str(state_disablehppupdates))
        rendersettingswindow()
    elif statetomodif == "themeswitch":
        state_theme += 1
        if state_theme > len(themenames) - 1:
            state_theme = 0
        print("THEME CHANGED: "+str(themenames[state_theme].lower()))
        updatetheme()
        startsettingswindow()
    elif statetomodif == "mapsrcfolderuse":
        state_usemapsrc = toggle_bool(state_usemapsrc)
        print("USEMAPSRC CHANGED: "+str(state_usemapsrc))
        rendersettingswindow()
    writetosettings()

btnresult = None

def openpopup(dtitle,dtext,db1text,db1action,db2text,db2action):
    global btnresult
    global dialog
    btnresult = None
    print("DIALOG OPENED")
    dialog = Toplevel()
    dialog.focus()
    dialog.grab_set()
    dialog.title(dtitle)
    dialog.minsize(250,50)
    dialog.resizable(False, False)
    dialog.configure(bg=colors_framebackground)
    dialog.tk.call('wm','iconphoto',dialog._w, Image("photo", file=os.path.dirname(__file__)+"/assets/icon.png"))

    dialog.bell()

    padding = Frame(dialog,bg=colors_framebackground,height=10)
    padding.grid(row=0, column=0, sticky="ew")

    lbl = Label(dialog,text=dtext, bg=colors_framebackground, fg=colors_primarytext, justify="center", font=(style_font, style_fontsize))
    lbl.grid(row=1, column=0, sticky="ew")
    print(dtext)

    padding = Frame(dialog,bg=colors_framebackground,height=10)
    padding.grid(row=2, column=0, sticky="ew")

    if not db1text == "":
        btn1 = Button(dialog,text=db1text, fg=colors_primarytext, command=lambda: popupbtnhandler(db1action), bg=colors_framebackground, activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="w", highlightthickness=0)
        btn1.grid(row=3, column=0)
        print("added button 1")
    if not db2text == "":
        btn2 = Button(dialog,text=db2text, fg=colors_primarytext, command=lambda: popupbtnhandler(db2action), bg=colors_framebackground, activebackground=colors_highlight, highlightbackground=colors_highlight,activeforeground='white', font=(style_font, style_fontsize), borderwidth=1, anchor="w", highlightthickness=0)
        btn2.grid(row=3, column=1)
        print("added button 2")

    padding = Frame(dialog,bg=colors_framebackground,height=10)
    padding.grid(row=4, column=0, sticky="ew")

    dialog.wait_window()

def popupbtnhandler(res):
    global btnresult
    global dialog
    btnresult=res
    print("DIALOG CLOSED")
    dialog.destroy()
    root.update()



def deletehammer(game, title, version, lineupdate):
    global gamefolderfinder
    bintype = ""
    gamefolderfinder = game


    openpopup("Delete Hammer", "Are you sure you wish to delete this hammer instance?\nWARNING: this will delete Hammer++, everything in the\
    \n'binwin' folder, as well as all Hammer++ settings. Continue?", "Continue", True, "Cancel", False)
    
    
    
    if btnresult == True:
        subwindow("deletinghammer")
        print(game)
        print("length of directory is " + str(len(os.path.basename(gamefolderfinder[:-1]))))
        print("directory up one is " + gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])])
        # find game folder
        if "hammerplusplus.exe" in game:
            gamefolderfinder = gamefolderfinder[:-19]
        if "hammer.exe" in game:
            gamefolderfinder = gamefolderfinder[:-11]
        print(gamefolderfinder + " HAMMER TEXT REMOVED!")
        while os.path.basename(gamefolderfinder) != title:
            print(os.path.basename(gamefolderfinder) == title)
            gamefolderfinder = gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])][:-1]
            print(gamefolderfinder + " found!")
        print(gamefolderfinder + " found!")
        
        #remove binwin
        os.system('rm -r "' + gamefolderfinder + '/binwin/"')
        #get bintype
        print(gamefolderfinder + "/bin/win64/hammer.exe")
        if os.path.exists(gamefolderfinder + "/bin/win64/hammer.exe") == True:
            bintype = "win64"
        elif os.path.exists(gamefolderfinder + "/bin/x64/hammer.exe") == True:
            bintype = "x64"
        elif os.path.exists(gamefolderfinder + "/bin/hammer.exe") == True:
            bintype = "."
        print("bintype is " + bintype)
        
        #remove hammer++
        os.system('rm "' + gamefolderfinder + '/bin/' + bintype + '/hammerplusplus.exe"')
        #remove rungame
        os.system('rm "' + gamefolderfinder + '/bin/' + 'linuxhammerlauncher_rungame.bat"')
        #remove hammer++ folder
        os.system('rm -r "' + gamefolderfinder + '/bin/' + bintype + '/hammerplusplus/"')
        
        #remove entry from games.txt
        with open(configpath + "games.txt", 'r') as file:
            lines = file.readlines()
        
        lines.pop(lineupdate)
        
        with open(configpath + "games.txt", 'w') as file:
            file.writelines(lines)
        
        #return to main window
        subwindow("finishdelete")
        startmainwindow()
    else:
        pass




rendermainwindow()

#Execute Tkinter
root.mainloop()
