![Linux Hammer Launcher](./assetssrc/hammerlauncher_logo_darkmode.png)

A launcher and installer for Hammer++ *(and vanilla Hammer)* on Linux, for many different Source Engine games.


## Prerequisites
- Wine *(while LHL automatically installs Wine 9, Wine is still required on your system for it to work properly)*
- Winetricks

You can install Wine & Winetricks on Debian-based distros by running these comamnds:
```
sudo apt update
sudo apt install wine winetricks
```

Please note that immutable distros (such as SteamOS and Bazzite) will most likely **not** work with Linux Hammer Launcher. You can try, but don't be suprised if it won't launch or run correctly. 

## Game support list
| Game | Works with Hammer++? | Launches game on compile? | Launches map on compile? |
| Half-Life 2 | Yes | Yes | Yes |
| Half-Life 2: Episode 1 | Yes | Yes | No | 
| Half-Life 2: Episode 2 | Yes | Yes | No |
| Half-Life 2: Deathmatch | Yes | Yes | No |
| Half-Life: Deathmatch Source | Yes | Yes | No |
| Team Fortress 2 | Yes | Yes | No |
| Portal | Yes | Yes | Yes |
| Portal 2 | Yes | Yes | Yes |
| Garry's Mod **(x86-64 branch *****ONLY*****)** | Yes | Yes | Yes |
| Day of Defeat: Source | Yes | Yes | No |
| Left 4 Dead | **NO** | No | No |
| Left 4 Dead 2 | Yes | Yes | Yes |
| Counter-Strike: Source | Yes | Yes | No |
| Black Mesa | **NO** | No | No |

Any games that do **NOT** support Hammer++ MUST have the "Use vanilla Hammer in setup" option enabled or else it will not work.

If a game is not listed here, you can still try setting up Hammer/Hammer++ for it.
Don't be suprised if Hammer/Hammer++ does not run though.

## Running Linux Hammer Launcher
- Go to [Releases](https://github.com/EnderCatCore/linuxhammerlauncher/releases/latest) and download the latest zip, and extract the zip anywhere.
- Give the Linux Hammer Launcher binary executable permissions, then open it to start the launcher.

If you can't change executable permissions using your file manager, try running this command in the LHL folder.

```
chmod +x ./Linux\ Hammer\ Launcher
```

## Cloning LHL from source
If you can't run Linux Hammer Launcher's binary version for any reason, or you want to modifiy LHL... you can run it from source.

### Prerequisites
Debian-based distros:
```
sudo apt update
sudo apt install git wine winetricks python3 python3-tk python3-requests python3-pip
pip install crossfiledialog
```

### Running LHL from source
```
git clone https://github.com/EnderCatCore/linuxhammerlauncher.git
cd linuxhammerlauncher
python3 ./hammer_launcher.py
```

## Using Linux Hammer Launcher
Upon launching LHL, you'll be greeted with the main menu.

**BEFORE SETTING UP ANY GAME, YOU MUST LAUNCH IT ON STEAM AT LEAST ONCE FIRST! USING FRESH INSTALLS OF GAMES CAN CAUSE ISSUES.**
You can set up a Hammer install by pressing the "Set up Hammer" button.
You will then be prompted to enter the game directory of the game you want to make maps for. You can do this by hitting the "Browse" button. If the "Browse" button doesn't work, you can copy and paste the path to the game into the textbox instead.
If you're not already using Proton for a game, you'll need to enable Proton for that game **temporarily** in Steam. This is so required files for Hammer to work is available.
To do that, right-click on the game in the game list, select **Properties**, choose **Compatability** in the popup dialog, enable the checkbox for forcing Steam Play, and set the dropdown to any Proton version.
Once you do so, close the popup and click on **Update**. Linux Hammer Launcher will automatically continue when it detects the needed files.
**NOTE:** If you're setting up Portal 2, Left 4 Dead or Left 4 Dead 2, you'll be also required to download the authoring tools for that game. You can download and install the authoring tools for your game in Steam by searching for it in your library. 

If you're using a supported game, all setup from this point should be automatic. Hammer++ will auto launch itself at some points to help set itself up. Once it's done, you can
