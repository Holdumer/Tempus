# Tempus
Minimalist screen time management for Windows.


#Python Process Monitor & Screen Time Blocker

A lightweight, customized desktop application built with Python that tracks application usage, enforces time limits, and features a real-time transparent overlay.

##Features
* CustomTkinter GUI: A sleek, dark-mode interface to add, remove, and manage tracked applications.
* Smart App Targeting: Select targets via native file browsing or manual entry.
* Real-Time Overlay: A transparent, click-through Heads-Up Display (HUD) that shows a live countdown of remaining time while you play.
* Automated Enforcement: Silently monitors processes in the background and forcefully terminates them when the daily time limit is reached.
* Persistent SQLite Database: securely tracks time across multiple sessions and resets daily.
* Self-Defense Mechanism: Built-in hardcoded blacklist prevents the blocker from tracking essential Windows tasks or terminating itself.

##Recomended way to use:
* Compile both Timer_GUI.py and Process_monitor.py into .exe file.
* Create a Process_monitor.exe - Shortcut and add it to the C:\Users\(Your user)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
* Configurate your app's time and data in the database through Timer_GUI

#DO NOT change the names of the .exe files in case you want everything to work correcrly (In case you want to don't forget to add a new name into the blacklist list in line 75 in the Timer_GUI.py before compiling it into .exe).

##Prerequisites
To run the source code, you need Python 3 installed along with the following libraries:
```bash
pip install -r requirements.txt
