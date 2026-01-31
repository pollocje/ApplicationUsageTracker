import os
import sys
import winshell
from win32com.client import Dispatch

def create_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "Application Usage Tracker.lnk")
    target = os.path.abspath(os.path.join("dist", "ApplicationUsageTracker.exe"))
    wDir = os.path.abspath("dist")
    icon = os.path.abspath("icon.png")

    if not os.path.exists(target):
        print(f"Error: Target executable not found at {target}")
        print("Did you run build.py first?")
        return

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    if os.path.exists(icon):
        shortcut.IconLocation = icon
    shortcut.save()
    
    print(f"Shortcut created at: {path}")

if __name__ == "__main__":
    create_shortcut()
