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
-fix hl2 missing dlls. they should be in binwin, detect if hl2 hammers being run, and paste tier0.dll and vstdlib.dll from binwin into bin. make sure to 
find a way to prompt user to set proton on setup for hl2.

-steam api is no longer an issue, but check and make sure other hammer editors havent been broken by the automatic install of plusplus tools, if they have, then turn off plusplus tools install for
specifically said games.

-fix display scaling for window. its usable rn but ugly

-tf2classified doesnt have any identifiable to windows files in its bin folder, installation process doesnt go further than proton set up. add button to continue maybe

-tf2classified requires a custom gameinfo. include that with program and copy it to tf2c maybe?

-bin is copied as binwin too quickly and misses important files on hdds. either add more file checks than hammerplusplus.exe, find a way to wait until its done, add a button, 
or brute force sleep(9999999)

-portal 1 doesnt work, crashes when run from binwin. find some way to merge the bin folders of native and windows or add a prompt forcing proton on portal 1 launch

-tell people to update hammer++, they copy to binwin

-portal 2 does not run from binwin. either paste all of binwin into native bin on hammer launch and hope it doesnt break, or prompt user to switch to proton before hammer launches.

-add scrollwheel to main window

-clean up code maybe idk i dont feeeeeeeeeeeeeelll like it /j

-add subwindows to cancel installation if there is no internet connection and things like wine 9 cant be installed

-HL2 wont compile at all. Can't find steam app user info error

-i dont imagine itll make a difference but testing on x11 should be done probably 

'''

# vguititlebar = 1
optionsframe = None
root = None
hammericon = None
deleteicon = None



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
        #    print("Disabling custom title bar...")
        #    vguititlebar = 0
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

    #if vguititlebar == 1:
    #    # no title bar for you!
    #    root.wm_attributes('-type', 'splash')
    #    titlebar= Frame(root,bg='#4c5844')
    #    titlebar.grid(sticky="w")
    #    faketitle = Label(titlebar, text = "Linux Hammer Launcher", fg='white', bg='#4c5844', font=("Tahoma", 9))
    #    faketitle.pack(pady=5, padx=2, anchor="w",fill="x")

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
        gamefolderpath = crossfiledialog.choose_folder()
        print(gamefolderpath)
        if not gamefolderpath.endswith("/"):
            gamefolderpath = gamefolderpath + "/"
        if gamefolderpath == "/":
            subwindow('gamedirectorypickerinvalid')
        elif os.path.exists(gamefolderpath + "bin/") == False:
            subwindow('gamedirectorypickerinvalid')
        elif os.path.exists(gamefolderpath + "bin/") == True:
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
    if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
        time.sleep(1)
        subwindow('protonenable')
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


'''subwindow creation'''
def subwindow(subwintype):
    global gamefolderpath
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
        
    #proton set up window
    if subwintype == 'protonenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Windows bin folder not detected. \n Go into steam and enable Proton for this game before continuing. \n You can turn off Proton later. \n \n \
        This window should auto-detect Proton on its own.",
        bg='#4c5844', fg='#d8ded3', font=("Tahoma", 9))
        lbl.grid(row=0, column=0)
        root.update()
        checkproton()
    #hammer++ set up window THE CORRECT USED ONE
    if subwintype == 'hammerenable':
        #root.geometry('600x140')
        lbl = Label(root, text = "Hammer++ not detected. download it at \n https://ficool2.github.io/HammerPlusPlus-Website/download.html \nand copy its bin folder into:\
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
    print("length of directory is " + str(len(os.path.basename(gamefolderfinder[:-1]))))
    print("directory up one is " + gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])])
    #set favorites in wineprefix to games map folder
    gamefolderfinder = gamefolderfinder[:-19]
    print(gamefolderfinder + " HAMMER TEXT REMOVED!")
    while os.path.basename(gamefolderfinder) != title:
        print(os.path.basename(gamefolderfinder) == title)
        gamefolderfinder = gamefolderfinder[:int(str(len(os.path.basename(gamefolderfinder)) / -1)[:-2])][:-1]
        print(gamefolderfinder + " found!")
    print(gamefolderfinder + " found!")
    print(os.getlogin())
    
    #create mapsrc folder for game
    if os.path.exists(gamefolderfinder + "/mapsrc/") == False:
        os.mkdir(gamefolderfinder + "/mapsrc/")
    #add mapsrc folder for game to favorites
    print(configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps")
    if os.path.exists(configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps") == False:
        print("ln -s '" + gamefolderfinder + "/mapsrc/' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")
        os.system("ln -s '" + gamefolderfinder + "/mapsrc/' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")
    #rename to game maps
    print("mv '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/mapsrc' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps'")
    os.system("mv '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/mapsrc' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/" + title + " maps'")

    #game specific stuff
    #game specific stuff will go here, like launching portal 2 hammer after copying binwin to default bin
    
    #launch wine9 with hammer using correct prefix
    print('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    os.system('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '"' + game + '"')
    root.quit()

def clicked():
    print("clicked!")
    


#set config folder
configpath = os.path.expanduser('~') + "/.config/linuxhammerlauncher/"


#create paths if they dont exist


#state and print
def stateandprint(string):
    #this frick is crapped
    print(string)

#edit hammer config/settings
def hammerconfig(binfolder):
    print("using binfolder "  + binfolder)
    combi3paths = gamefolderpath + binfolder + bintype
    if binfolder == "binwin/":
        #copy bin folder as binwin in same directory if it does not exist. auto delete if it already exists (though this might mess up user data. open dialog to ask user?)
        if os.path.exists(gamefolderpath + "binwin") == True:
            print("BINWIN ALREADY EXISTS! deleting...")
            os.system("rm -r '" + gamefolderpath + "binwin/'")
        print("game folder path is " + gamefolderpath)
        if os.path.exists(gamefolderpath + "binwin") == False:
            print("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
            os.system("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
        #update settings.ini for people who already have used hammerplusplus before

        if os.path.exists(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini") == True:
            with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'r') as file:
                data = file.read()
                data = data.replace("\\bin\\", "\\binwin\\")
            with open(combi3paths + "/hammerplusplus/hammerplusplus_settings.ini", 'w') as file:
                file.write(data)


    #gameconfig & settings generation
    timeout_time = 10

    #create a .sh file to run, timeout doesnt like WINEPREFIX= being there.
    bashfile = open(configpath + "temprunhammerbash.sh", "w")
    print("'WINEPREFIX="' + configpath + prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + '/hammerplusplus.exe"')
    bashfile.write('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine "' + combi3paths + '/hammerplusplus.exe"')
    bashfile.close()
    os.system("chmod +x " + configpath + "temprunhammerbash.sh")

    #keep starting hammer for increasing amounts of time until gameconfig is generated
    while os.path.isfile(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt") == False:
        print("timeout " + str(timeout_time) + " " + configpath + "temprunhammerbash.sh")
        os.system("timeout " + str(timeout_time) + " " + configpath + "temprunhammerbash.sh")
        timeout_time += 5
        root.update()

    os.remove(configpath + "temprunhammerbash.sh")

    subwindow("editingconfigs")

    #edit gameconfig for hammer
    print("modifiying gameconfig for "  + binfolder)
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
    #binwin
    with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r') as file:
        data = file.read()
        data = data.replace("\\bin\\", "\\binwin\\")
    with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
        file.write(data)

    #check for steam. if find steam make bat!! if not. too bad. fool
    steampath = os.popen("which steam").read()
    if os.path.exists(steampath[:-1]) == True:
        print("found steam!")
        #detect appid
        with open(gamefolderpath + "steam_appid.txt", 'r') as appidfile:
            print(gamefolderpath + "steam_appid.txt")
            game_appid = str(appidfile.read())[:-2]
            print("appid is " + game_appid)

        #create run game bat
        print(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat")
        batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
        batfile.write('@echo off\nstart /unix ' + steampath[:-1] +' steam://rungameid/' + str(game_appid) + '//"%3 %4"\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
        batfile.close()
    else:
        print("could not find steam. flatpak moment!")
        #create run game bat (dummy version)
        print(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat")
        batfile = open(gamefolderpath + binfolder + "linuxhammerlauncher_rungame.bat", 'w')
        batfile.write('@echo off\n\necho:\necho "Thanks for using Linux Hammer Launcher! ^c^"')
        batfile.close()

    #create win version of gamefolderpath
    gamefolderwindowified = "Z:" + gamefolderpath.replace("/", "\\")
    binfolderwindowified = binfolder.replace("/","\\")
    print(gamefolderwindowified)
    print(binfolderwindowified)
    #set launch game to bat in config
    with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines[14] = '				"GameExe"		"' + gamefolderwindowified + binfolderwindowified + 'linuxhammerlauncher_rungame.bat"\n'
    with open(combi3paths + "/hammerplusplus/hammerplusplus_gameconfig.txt", 'w') as file:
        file.writelines(lines)

'''
set up hammer wineprefix, set statuses along the way
'''

def setuphammer():
    global settinguphammer
    global root
    global gamefolderpath
    global gameconfig
    
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
        
        #check if proton is enabled, if not, prompt user to enable proton before continuing.
        if os.path.exists(gamefolderpath + "bin/hammer.exe") == False:
            subwindow('protonenable')
        #check for hammerplusplus, if not there, open file picker for hammer++ zip.
        subwindow('hammerenable')
    
        #install plusplus tools
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
        print("cd " + configpath + " && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "tools_plusplus/'* '" + gamefolderpath + "bin/" + bintype + "/'")
        os.system("cd " + configpath + " && unzip tools_plusplus.zip" + " && " + "cp '" + configpath + "tools_plusplus/'* '" + gamefolderpath + "bin/" + bintype + "/'")
        print("removing temp tools++ files...")
        os.remove(configpath + "tools_plusplus.zip")
        os.remove(configpath + "tools_plusplus/bspzipplusplus.exe")
        os.remove(configpath + "tools_plusplus/vbspplusplus.exe")
        os.remove(configpath + "tools_plusplus/vradplusplus.exe")
        os.remove(configpath + "tools_plusplus/vvisplusplus.exe")
        os.remove(configpath + "tools_plusplus/toolsplusplus.fgd")
        os.rmdir(configpath + "tools_plusplus/")

        #write new game definition to config file. check if file exists
        gameconfig = open(configpath + "games.txt", "a")
        
        
        #hl2s bin folder location matters meaning you cant use binwin for it i guess????? it also just packages in both linux and windows stuff in both versions so??? doesnt matter??? i guess?????? just check for hl2????????
        if os.path.basename(gamefolderpath[:-1]) == "Half-Life 2":
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/hammerplusplus.exe']" + "\n"
            hammerconfig("bin/")
        else:
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "binwin/" + bintype + "/hammerplusplus.exe']" + "\n"
            hammerconfig("binwin/")
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
    optionsframe = Frame(root, bg="#3e4637", relief='sunken', bd=0, highlightthickness=0)
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

    hammericon = Image("photo", file="assets/sdk_hammer.png")
    setupicn = Label(optionsframe, bg="#3e4637", image=hammericon, anchor="e")
    setupicn.image = hammericon #the fact that you have to do this just to keep an image alive is extremely stupid dumb dumb stupid dumb stupid. stupid face
    setupicn.grid(row=linenum+6, column=0, sticky="ew")
    #set up button
    setupbtn = Button(optionsframe, text = "Set up Hammer", fg = "#d8ded3", command=lambda: setuphammer(), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    #reset button
    #deleteicon = Image("photo", file="assets/sdk_delete.png")
    #removeicn = Label(optionsframe, bg="#3e4637", image=deleteicon, anchor="e")
    #removeicn.image = deleteicon #see above
    #removeicn.grid(row=linenum+7, column=0, sticky="ew")
    resetbtn = Button(optionsframe, text = "Reset Hammer", fg = "#d8ded3", command=lambda: print("STUB!"), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    #remove button
    #reseticon = Image("photo", file="assets/sdk_delete.png")
    #reseticn = Label(optionsframe, bg="#3e4637", image=deleteicon, anchor="e")
    #reseticn.image = deleteicon #see above
    #reseticn.grid(row=linenum+8, column=0, sticky="ew")
    removebtn = Button(optionsframe, text = "Delete Hammer", fg = "#d8ded3", command=lambda: print("STUB!"), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)

    setupbtn.grid(row=linenum+6, column=1, sticky="ew")
    resetbtn.grid(row=linenum+7, column=1, sticky="ew")
    removebtn.grid(row=linenum+8, column=1, sticky="ew")

    #CREDITS
    setuptext = Label(optionsframe, text = "CREDITS", fg='#c4b550', bg='#3e4637', justify="left",font=("Tahoma", 7), anchor="sw", height=2, highlightthickness=0)
    setuptext.grid(row=linenum+9, column=1, sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+10, column=0,sticky="ew")
    divider = Frame(optionsframe,bg='#282e22',height=2)
    divider.grid(row=linenum+10, column=1,sticky="ew")

    #endericon = Image("photo", file="assets/credit_end.png")
    #crediticn = Label(optionsframe, bg="#3e4637", image=endericon, anchor="e")
    #crediticn.image = endericon #see above
    #crediticn.grid(row=linenum+11, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "EnderCatCore", fg = "#d8ded3", command=lambda: webbrowser.open("https://endercatcore.neocities.org",new=2, autoraise=True), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+11, column=1, sticky="ew")

    #tommyicon = Image("photo", file="assets/credit_tam.png")
    #crediticn = Label(optionsframe, bg="#3e4637", image=tommyicon, anchor="e")
    #crediticn.image = tommyicon #see above
    #crediticn.grid(row=linenum+12, column=0, sticky="ew")
    creditbtn = Button(optionsframe, text = "Thomasluigi07", fg = "#d8ded3", command=lambda: webbrowser.open("https://thomasluigi07.com",new=2, autoraise=True), bg='#3e4637', \
    activebackground='#968731', highlightbackground = "#968731",activeforeground='white', relief="flat", font=("Tahoma", 9), borderwidth=0, anchor="w", highlightthickness=0)
    creditbtn.grid(row=linenum+12, column=1, sticky="ew")

    dummy = Frame(root,bg='#4c5844',height=5)
    dummy.grid(sticky="w")

rendermainwindow()

#Execute Tkinter
root.mainloop()
