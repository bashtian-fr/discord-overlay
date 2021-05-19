# Discord-overlay

A Discord PyQT5 app that provide a discord overlay over the windows.

<img src="/docs/demo.png" alt="Demo - visible frame" height="200px" />
<img src="/docs/only_speakers.png" alt="Demo - only_speakers" height="200px" />

# Features
- stays on top
- click throu
- can hide window frame
- show only speakers/or all present in chanel
- resizeable

# Options
- `--debug` enabled debug logs

# Install/Run

It is a standalone app (aka portable). There is not installation. \
Note: The release may appear big in size, this is because it embed all DLLs and the Python interpret to run it properly.

- Prerequisites
  - Ubuntu: install `sudo apt-get install libxcb-xinerama0`
  - Windows: install `Microsoft Visual C++ Redistributable`
    - Windows may see the application as threat. Click 'More info' then 'Run anyway' (windows10).
- Download a [release](https://github.com/bashtian-fr/discord-overlay/releases/) according to your system or build it.
- Run the downloaded release.
- Discord will ask you to authorize ![Streamkit](https://discord.com/streamkit) to access your discord messages and channels. ![Streamkit](https://discord.com/streamkit) is the official discord app to manage apis/rpc.


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

The executable will be created in dist/ folder

# Credits
Part of the connector is based on the one of Trigg's: https://github.com/trigg/Discover/blob/master/discover_overlay/discord_connector.py
