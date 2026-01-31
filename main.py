import sys
from PyQt6.QtWidgets import QApplication
from tracker import WindowTracker, TrackerWorker
from storage import DataStore
from gui import DashboardWindow, SystemTray
from utils import resource_path

def main():
    print("Starting Application Usage Tracker...")
    app = QApplication(sys.argv)
    
    tracker = WindowTracker()
    storage = DataStore()
    
    # Start background worker
    worker = TrackerWorker(tracker, storage)
    # worker.usage_updated.connect(lambda name, date, sec: print(f"Tracked: {name}"))
    worker.start()

    # Initialize System Tray
    app.setQuitOnLastWindowClosed(False)
    
    # Pass storage to window for data access
    window = DashboardWindow(storage)
    
    icon_path = resource_path("icon.png")
    tray = SystemTray(app, window, icon_path)
    
    print("Tracker running. Check System Tray.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
