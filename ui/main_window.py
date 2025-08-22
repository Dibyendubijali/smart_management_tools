from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget
)
from PyQt5.QtCore import Qt
from ui.server_list_ui import ServerListUI  # Import your server UI here

class MainWindow(QMainWindow):
    """
    Main application window.
    Provides navigation between features using a sidebar.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Management Tools")
        self.resize(1000, 600)

        # Central layout
        main_layout = QHBoxLayout()

        # Sidebar (navigation menu)
        sidebar = QVBoxLayout()
        self.server_list_btn = QPushButton("📋 Server List")
        self.terminal_btn = QPushButton("💻 Terminal")
        self.monitor_btn = QPushButton("📊 Monitoring")
        self.logs_btn = QPushButton("📑 Logs")
        self.shell_btn = QPushButton("⚙️ Shell Exec")

        # Connect buttons to functions
        self.server_list_btn.clicked.connect(self.show_server_list)
        self.terminal_btn.clicked.connect(self.show_terminal)
        self.monitor_btn.clicked.connect(self.show_monitoring)
        self.logs_btn.clicked.connect(self.show_logs)
        self.shell_btn.clicked.connect(self.show_shell_exec)

        # Add buttons to sidebar
        sidebar.addWidget(self.server_list_btn)
        sidebar.addWidget(self.terminal_btn)
        sidebar.addWidget(self.monitor_btn)
        sidebar.addWidget(self.logs_btn)
        sidebar.addWidget(self.shell_btn)
        sidebar.addStretch(1)

        # Content area (placeholder until UIs are implemented)
        self.content_area = QListWidget()
        self.content_area.addItem("Welcome to Smart Management Tools!")
        self.content_area.addItem("Use the sidebar to navigate.")
        
        # Content area as QWidget container
       # self.content_area = QWidget()
        #self.content_layout = QVBoxLayout()
        #self.content_area.setLayout(self.content_layout)

        # Combine layouts
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.content_area, 4)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Default view
       # self.show_welcome_message()

   # def clear_content_area(self):
        # Remove all widgets from content_layout
       # while self.content_layout.count():
       #     child = self.content_layout.takeAt(0)
       #     if child.widget():
       #         child.widget().deleteLater()

    #def show_welcome_message(self):
     #   self.clear_content_area()
      #  from PyQt5.QtWidgets import QLabel
      #  label = QLabel("Welcome to Smart Management Tools!\nUse the sidebar to navigate.")
       # label.setAlignment(Qt.AlignCenter)
        #self.content_layout.addWidget(label)

    # Button click functions
    def show_server_list(self):
        self.content_area.clear()
        self.content_area.addItem("📋 Registered Servers")
        self.content_area.addItem("List of servers will be shown here.")

    def show_terminal(self):
        self.content_area.clear()
        self.content_area.addItem("💻 Terminal Access")
        self.content_area.addItem("Terminal UI will appear here.")

    def show_monitoring(self):
        self.content_area.clear()
        self.content_area.addItem("📊 Server Monitoring")
        self.content_area.addItem("CPU, Memory, Disk graphs go here.")

    def show_logs(self):
        self.content_area.clear()
        self.content_area.addItem("📑 Log Viewer")
        self.content_area.addItem("Logs from /var/log/syslog or messages.")

    def show_shell_exec(self):
        self.content_area.clear()
        self.content_area.addItem("⚙️ Remote Shell")
        self.content_area.addItem("Enter command to run remotely.")

# Export function
def get_main_window():
    return MainWindow()
