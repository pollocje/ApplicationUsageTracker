from PyQt6.QtWidgets import (QMainWindow, QLabel, QSystemTrayIcon, QMenu, QWidget, 
                             QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
                             QComboBox, QProgressBar, QFrame)
from PyQt6.QtGui import QIcon, QAction, QColor, QPainter, QBrush
from PyQt6.QtCore import Qt, QTimer, QSize

class AppItemWidget(QWidget):
    def __init__(self, name, seconds, max_seconds):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.setMinimumHeight(45)
        
        # Top row: Name and Time
        top_row = QHBoxLayout()
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("font-weight: bold; color: #ffffff; font-size: 14px;")
        
        time_str = self.format_time(seconds)
        self.time_label = QLabel(time_str)
        self.time_label.setStyleSheet("color: #cccccc;")
        
        top_row.addWidget(self.name_label)
        top_row.addStretch()
        top_row.addWidget(self.time_label)
        
        # Bottom row: Progress Bar
        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setRange(0, max_seconds if max_seconds > 0 else 1)
        self.bar.setValue(seconds)
        self.bar.setFixedHeight(8)
        self.bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #404040;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """)
        
        layout.addLayout(top_row)
        layout.addWidget(self.bar)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}h {m}m"
        elif m > 0:
            return f"{m}m {s}s"
        else:
            return f"{s}s"

class DashboardWindow(QMainWindow):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self.setWindowTitle("Application Usage Tracker")
        self.resize(500, 600)
        
        # Main Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #2b2b2b;")
        
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Usage Dashboard")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Today", "All Time"]) # TODO: Add 30 Days logic later
        self.filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #404040;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox::drop-down { border: none; }
        """)
        self.filter_combo.currentIndexChanged.connect(self.refresh_data)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.filter_combo)
        
        main_layout.addLayout(header_layout)
        
        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: none;
                outline: none;
            }
            QListWidget::item {
                border-bottom: 1px solid #404040;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.list_widget)
        
        # Refresh Timer (Update UI every 5 seconds if open)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(5000)
        
        self.refresh_data()
        print("DashboardWindow initialized")

    def refresh_data(self):
        filter_mode = self.filter_combo.currentText()
        data = {}
        
        if filter_mode == "Today":
            data = self.storage.get_usage() # Defaults to today
        elif filter_mode == "All Time":
            # Aggregate all time
            all_data = self.storage.data
            for date_str, apps in all_data.items():
                for app, seconds in apps.items():
                    data[app] = data.get(app, 0) + seconds
        
        # Sort by usage (descending)
        sorted_apps = sorted(data.items(), key=lambda item: item[1], reverse=True)
        
        # Find max for bar scaling
        max_seconds = sorted_apps[0][1] if sorted_apps else 1
        
        self.list_widget.clear()
        for app_name, seconds in sorted_apps:
            item = QListWidgetItem(self.list_widget)
            widget = AppItemWidget(app_name, seconds, max_seconds)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

class SystemTray(QSystemTrayIcon):
    def __init__(self, app, window, icon_path):
        super().__init__()
        self.app = app
        self.window = window
        self.setIcon(QIcon(icon_path))
        self.setVisible(True)
        
        # Context Menu
        menu = QMenu()
        
        open_action = QAction("Open Dashboard", self)
        open_action.triggered.connect(self.show_dashboard)
        menu.addAction(open_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
        self.activated.connect(self.on_activated)
        print("SystemTray initialized")

    def show_dashboard(self):
        self.window.show()
        self.window.activateWindow()

    def quit_app(self):
        self.app.quit()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_dashboard()
