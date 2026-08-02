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

Please note that immutable distros (such as SteamOS and Bazzite) will most likely **not** work with LHL. You can try, but don't be suprised if it won't launch or run correctly. 

## Supported Games
- Half Life: 2
- Half Life 2: Episode 1
- Half Life 2: Episode 2
- Half-Life 2: Deathmatch
- Half-Life: Deathmatch Source
- Team Fortress 2
- Portal
- Portal 2
- Garry's Mod **(x86-64 branch** ***MUST*** **be enabled)**
- Day of Defeat: Source
- Left 4 Dead **(with the vanilla Hammer option enabled during setup)**
- Left 4 Dead 2
- Counter-Strike: Source
- Black Mesa **(with the vanilla Hammer option enabled during setup)**

If a game is not listed here, you can still try setting up Hammer/Hammer++ for it.
Don't be suprised if Hammer/Hammer++ does not run though.

## Running LHL
- Go to [Releases](https://github.com/EnderCatCore/linuxhammerlauncher/releases/latest) and download the latest zip, and extract the zip anywhere.
- Give the Linux Hammer Launcher binary executable permissions, then open it to start the launcher.

If you can't change executable permissions using your file manager, try running this command in the LHL folder.

```
chmod +x ./Linux\ Hammer\ Launcher
```

## Cloning LHL from source
If you can't run LHL's binary version for any reason, or you want to modifiy LHL, you can run it from source.

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

## Using LHL
click on set up hammer to do things wowwwwww. then it will add the game. then do this and that and whatever this is a placeholder

