from tracker import WindowTracker
import time

def test_tracking():
    tracker = WindowTracker()
    print("Tracking active window for 10 seconds...")
    for _ in range(10):
        name, title = tracker.get_active_window_info()
        print(f"App: {name}, Title: {title}")
        time.sleep(1)

if __name__ == "__main__":
    test_tracking()
