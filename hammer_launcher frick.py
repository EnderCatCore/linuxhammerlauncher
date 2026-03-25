from tkinter import *  
import time
import os
import requests
from threading import Thread







settinguphammer = 0

'''
GUI function stuffs
'''


#makes game button
def creategamebutton(height, frame):
    btn = Button(frame, text = "Garry's Mod" , fg = "white", command=lambda: launchhammer(game),width=30, height=0, bg='#3e4637', 
    activebackground='#4c5844', highlightbackground = "#282e22",activeforeground='white')
    btn.grid(row=height, column=0)

 
'''
window creation
'''
# create root window
root = Tk()
def mainwindow():

    # root window title and dimension
    root.title("Linux Hammer Launcher")
    # Set geometry (widthxheight)
    root.geometry('268x400')
    # Set resizability (widthxheight)
    root.resizable(False, False)
    # Change the background color using configure
    root.configure(bg='#4c5844')
    # adding a grid why isit called lbl i forgot where i pasted this from oh god
    lbl = Label(root)
    lbl.grid()
    
    '''
    Frame creation
    '''
    optionsframe = Frame(root, bg="#3e4637", width=268, height=320, relief='raised', bd=0)
    optionsframe.grid(row=0, column=0)
    optionsframe.grid_propagate(False)
    '''
    frame creation ^^
    '''

    
    #temp code
    tempnum = 0
    for i in range(1):
        creategamebutton(tempnum + 3, optionsframe)
        tempnum += 1

    #set up button
    setupbtn = Button(optionsframe, text = "Set up a Game" , fg = "white", command=lambda: setuphammer(),width=30, height=0, bg='#3e4637', \
    activebackground='#4c5844', highlightbackground = "#282e22",activeforeground='white')
    
    setupbtn.grid(row=1, column=0)
    
#execute main window by default
mainwindow()
'''
window creation ^^
'''
def subwindow():
    root.geometry('225x125')
    lbl = Label(root, text = "Setting up Wine. Please wait... \n This might take a while.")
    lbl.grid()

'''
sub window creation
'''
subwinkill = 0


'''
Non GUI functions
'''

# close window when program is launched
def closelauncher():
    root.destroy()
    



# start correct game
game = "gmod";
def launchhammer(game):
    if game == "gmod":
        closelauncher()
        os.system('WINEPREFIX="' + configpath + 'prefix/" ' + configpath + 'runner/wine-9.0.1/bin/wine ' + '/home/artshinea/.steam/steam/steamapps/common/GarrysMod/bin/win64/hammerplusplus.exe')
        root.quit()

def clicked():
    print("clicked!")
    


#set config folder
configpath = os.path.expanduser('~') + "/.config/linuxhammerlauncher/"


#create paths if they dont exist


#state and print
def stateandprint(string):
    global statustext
    global currentstatus
    statustext.config(text = currentstatus)
    print(string)
    currentstatus = string

'''
set up hammer wineprefix, set statuses along the way
'''


def setuphammer():
    global settinguphammer
    global root
    
    if settinguphammer == 0:
        settinguphammer = 1
        
        
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
        

            



'''
Non GUI functions ^^
'''














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





#Execute Tkinter
root.mainloop()
