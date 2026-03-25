from tkinter import *  
import os
import requests
import crossfiledialog
import time
import zipfile
import json


''' TODO and ISSUES
-fix hl2 missing dlls. they should be in binwin, detect if hl2 hammers being run, and paste tier0.dll and vstdlib.dll from binwin into bin. make sure to 
find a way to prompt user to set proton on setup for hl2.

-fix steam api steamfilesystem missing. installing vbspplusplus and such might help. potentially prompt users to install ++ compile programs for specific games that dont compile otherwise. 
if ++ compile programs dont fix it, add a button to main window to 'fix steam api', which will prompt them to install the windows version of steam to the prefix.

-fix display scaling for window. its usable rn but ugly

-tf2classified doesnt have any identifiable to windows files in its bin folder, installation process doesnt go further than proton set up. add button to continue maybe

-bin is copied as binwin too quickly and misses important files on hdds. either add more file checks than hammerplusplus.exe, find a way to wait until its done, add a button, 
or brute force sleep(9999999)

-portal 1 doesnt work, crashes when run from binwin. find some way to merge the bin folders of native and windows or add a prompt forcing proton on portal 1 launch

-tell people to update hammer++, they copy to binwin

-portal 2 does not run from binwin. either paste all of binwin into native bin on hammer launch and hope it doesnt break, or prompt user to switch to proton before hammer launches.

-add scrollwheel to main window

'''



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
    #root.geometry('268x400')
    # Set resizability (widthxheight)
    root.resizable(False, False)
    # Change the background color using configure
    root.configure(bg='#4c5844')
    # adding a grid why isit called lbl i forgot where i pasted this from oh god
    lbl = Label(root)
    lbl.grid()

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
            
    #wine set up window
    if subwintype == 'winesetup':
        #root.geometry('210x100')
        lbl = Label(root, text = "Setting up Wine. Please wait... \n This might take a while.", bg='#4c5844', fg='white')
        lbl.grid()
        statustext.config(text = "")
        root.update()
    #game directory chooser
    elif subwintype == 'gamedirectorypicker':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Please navigate to the folder for the \n game you want to map for.", bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='white')
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg='#4c5844', fg='white')
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        findgame()
    #game directory chooser if you frick it up
    elif subwintype == 'gamedirectorypickerinvalid':
        subwinpressable == 1
        #root.geometry('228x140')
        lbl = Label(root, text = "Could not find bin... \n Re-select the correct game folder.", bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='white')
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "Example: \nhomefolder/.steam/steam/\nsteamapps/common/GarrysMod/", bg='#4c5844', fg='white')
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        
        findgame()
        statustext.config(text = "")
        root.update()
        
    #proton set up window
    if subwintype == 'protonenable':
        #root.geometry('414x100')
        lbl = Label(root, text = "Windows bin folder not detected. \n Go into steam and enable Proton for this game before continuing. \n You can turn off Proton later. \n \n \
        This window should auto-detect Proton on its own.",
        bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        statustext.config(text = "")
        root.update()
        checkproton()
    #hammer++ set up window THE CORRECT USED ONE
    if subwintype == 'hammerenable':
        #root.geometry('600x140')
        lbl = Label(root, text = "Hammer++ not detected. download it at \n https://ficool2.github.io/HammerPlusPlus-Website/download.html \nand copy its bin folder into:\
         \n " + gamefolderpath + "bin/",
        bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        statustext.config(text = "")
        root.update()
        checkhammer()
    #hammer++ install window
    elif subwintype == 'hammerinstall':
        #root.geometry('430x140')
        lbl = Label(root, text = "Please download Hammer++ and select the downloaded archive for it. ", bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='white')
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "You can install Hammer++ here: \n https://ficool2.github.io/HammerPlusPlus-Website/download.html", bg='#4c5844', fg='white')
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        installhammer()
    #hammer++ install window if you freaked it up
    elif subwintype == 'hammerinstallinvalid':
        #root.geometry('423x140')
        lbl = Label(root, text = "Hammer++ executable not found. Did you select the correct \narchive? ", bg='#4c5844', fg='white')
        lbl.grid(row=0, column=0)
        lbl = Label(root, text = "------", bg='#4c5844', fg='white')
        lbl.grid(row=1, column=0)
        lbl = Label(root, text = "You can install Hammer++ here: \n https://ficool2.github.io/HammerPlusPlus-Website/download.html", bg='#4c5844', fg='white')
        lbl.grid(row=2, column=0)
        
        root.update()
        time.sleep(1)
        installhammer()
    #finishing up
    elif subwintype == 'finishingup':
        #root.geometry('260x130')
        lbl = Label(root, text = "Hammer++ for your game has \nset up. You can turn Proton off \nfor this game now. \nThe main window will open again now.", bg='#4c5844', fg='white')
        lbl.grid()
        statustext.config(text = "")
        root.update()
        time.sleep(7)
        
        




def rendertheframeagainfrick():
    global optionsframe
    global root
    
    print(root.grid_bbox(5, 4))
    '''
    Frame creation
    '''
    optionsframe = Frame(root, bg="#3e4637", width=268, height=325, relief='raised', bd=0)
    optionsframe.grid(row=0, column=0)
    optionsframe.grid_propagate(False)
    '''
    frame creation ^^
    '''

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
    print("ln -s '" + gamefolderfinder + "' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")
    os.system("ln -s '" + gamefolderfinder + "' '" + configpath + "prefix/drive_c/users/" + os.getlogin() + "/Favorites/'")

    #game specific stuff
    '''
    if game == "Team Fortress 2":
        if os.path.exists(gamefolderpath + "bin/hammerplusplus.exe") == False:
            os.system("cp '" + gamefolderfinder + 
    '''
    
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
        #copy bin folder as binwin in same directory if it does not exist
        print("game folder path is " + gamefolderpath)
        if os.path.exists(gamefolderpath + "binwin") == False:
            print("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
            os.system("cp -r '" + gamefolderpath + "bin/' '" + gamefolderpath + "binwin/'")
        
        
        #write new game definition to config file. check if file exists
        
                    
        gameconfig = open(configpath + "games.txt", "a")
        
        #hl2s bin folder location matters meaning you cant use binwin for it i guess????? it also just packages in both linux and windows stuff in both versions so??? doesnt matter??? i guess?????? just check for hl2????????
        if os.path.basename(gamefolderpath[:-1]) == "Half-Life 2":
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "bin/" + bintype + "/hammerplusplus.exe']" + "\n"
        else:
            gamedefinition = "['" + os.path.basename(gamefolderpath[:-1]) + "', '" + gamefolderpath + "binwin/" + bintype + "/hammerplusplus.exe']" + "\n"
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
        rendertheframeagainfrick()
        rendermainstuff()
        
#.config/linuxhammerlauncher/



#check for prefix folder, if it doesnt exist, make it, dummy.
if os.path.exists(configpath + "prefix/") == False:
    os.mkdir(configpath + "prefix/")
#check for runner folder, if it doesnt exist, make it dummy
if os.path.exists(configpath + "runner/") == False:
    os.mkdir(configpath + "runner/")
#check for games config file, if it doesnt exist, make it dummy
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
    btn = Button(optionsframe, text = title , fg = "white", command=lambda: launchhammer(hammerpath, title),width=30, height=0, bg='#3e4637', 
    activebackground='#4c5844', highlightbackground = "#282e22",activeforeground='white')
    btn.grid(row=height, column=0)





def rendermainstuff():
    global statustext
    linenum = 0
    #create game buttons based on game defs
    gameconfig = open(configpath + "games.txt", 'r')
    
    # lines to print (or not to print this list just kinda needs to be here regardless of how little it accomplishes
    specified_lines = [99]

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

        
        
    #set up button
    setupbtn = Button(optionsframe, text = "Set up a Game" , fg = "white", command=lambda: setuphammer(),width=30, height=0, bg='#3e4637', \
    activebackground='#4c5844', highlightbackground = "#282e22",activeforeground='#f5f5f5')
    
    setupbtn.grid(row=1, column=0)

    print (setupbtn.cget('activeforeground'))
    '''
    GUI Stuffs
    '''

    #Status Text
    currentstatus = "Welcome to Linux Hammer Launcher. \n \n Created by EnderCatCore"



    statustext = Label(root, text = currentstatus, fg='white', bg='#4c5844')
    statustext.grid()


    #Options Labels
    setuptext = Label(optionsframe, text = "Set Up Hammer", fg='white', bg='#3e4637')
    setuptext.grid(row=0)

    setuptext = Label(optionsframe, text = "Launch Hammer", fg='white', bg='#3e4637')
    setuptext.grid(row=2)











rendertheframeagainfrick()
rendermainstuff()

#Execute Tkinter
root.mainloop()
