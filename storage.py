import json
import os
from datetime import datetime

class DataStore:
    def __init__(self, filename="usage_data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_data(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def update_usage(self, app_name, seconds=1):
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data:
            self.data[today] = {}
        
        if app_name not in self.data[today]:
            self.data[today][app_name] = 0
        
        self.data[today][app_name] += seconds
        self.save_data() # Auto-save on update for now, can optimize later

    def get_usage(self, date_str=None):
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        return self.data.get(date_str, {})
