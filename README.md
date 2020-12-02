# Discord-overlay

A Discord PyQT5 app that provide a discord overlay over the windows.

![alt text](/docs/demo.png?raw=true  "Demo - visible frame")
![alt text](/docs/withoutframe.png?raw=true  "Demo - without frame")

# Usage

- download a [release](https://github.com/bashtian-fr/discord-overlay/releases/) according to your system or build it.
- for ubuntu you will need to install `sudo apt-get install libxcb-xinerama0`
- run the downloaded release, warning Windows may see the application as threat. Click 'More info' then 'Run anyway' (windows10).
- discord will ask you to authorize ![Streamkit](https://discord.com/streamkit) to access your discord messages and channels. ![Streamkit](https://discord.com/streamkit) is the official discord app to manage apis/rpc.
- start the overlay, the frame will be visible, you can hide it using the icon: ![alt text](/docs/toggle_button.png?raw=true  "hide")
- You can also toggle the frame using the systray menu: ![alt text](/docs/systray_menu.png?raw=true  "systray")
- you can resize the frame with the corner button (it is not saved upon restarts): ![alt text](/docs/resize.png?raw=true  "systray")
- drag the window using the red frame title.
- by default the frame will be positioned at x:0, y:0 (top-left corner). Moving it does not save the position. You need to replace it/resize it everytime you start the overlay.

# build

## Windows & Linux/Macos

1. install python and git:
- https://www.python.org/downloads/
- https://git-scm.com/downloads

2. create a virtualenv
`python3 -m venv .pyvenv3`

3. Source the venv
- windows:
`.pyvenv\Scripts\Activate`
- Linux/Macos:
`./.pyvenv/bin/activate`

4. clone the sources
`git clone https://github.com/bashtian-fr/discord-overlay.git`

4. install the build deps
`pip install .`

5. Build the static files
`pyrcc5 -o do/resources/rc.py do/resources/src.qrc`

6. Build an executable
`pip install pyinstaller`
`pyinstaller --icon do/statics/images/icon.ico -n discord-overlay --onefile --windowed do/scripts/entrypoint.py`

The executable will be create in dist/ folder

# Credits
Part of the connector is based on the one of Trigg's: https://github.com/trigg/Discover/blob/master/discover_overlay/discord_connector.py
