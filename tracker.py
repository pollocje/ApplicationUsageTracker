import win32gui
import win32process
import psutil
import time
from PyQt6.QtCore import QThread, pyqtSignal

class WindowTracker:
    def __init__(self):
        pass

    def get_active_window_info(self):
        """
        Returns a tuple (process_name, window_title) of the active window.
        Returns (None, None) if it fails or if there is no active window.
        """
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None, None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid <= 0:
                return None, None

            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return None, None

            window_title = win32gui.GetWindowText(hwnd)
            
            return process_name, window_title

        except Exception as e:
            # print(f"Error tracking window: {e}")
            return None, None

class TrackerWorker(QThread):
    usage_updated = pyqtSignal(str, str, int) # app_name, date, seconds

    def __init__(self, tracker, storage):
        super().__init__()
        self.tracker = tracker
        self.storage = storage
        self.running = True

    def run(self):
        while self.running:
            process_name, window_title = self.tracker.get_active_window_info()
            if process_name:
                # Simple logic: if we found an app, add 1 second
                # In a real app, we might want to be more precise with timing
                self.storage.update_usage(process_name, 1)
                self.usage_updated.emit(process_name, "today", 1) # "today" is a placeholder, logic handled in storage
            
            time.sleep(1)

    def stop(self):
        self.running = False
        self.wait()
