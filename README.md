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

##Prerequisites
To run the source code, you need Python 3 installed along with the following libraries:
```bash
pip install -r requirements.txt
