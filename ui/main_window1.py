from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from ui.server_list_ui import ServerListUI  # Real Server UI
from ui.terminal_ui1 import TerminalUI        # Real Terminal UI
from features.server_monitoring.resource_graph import ResourceGraph
from features.server_monitoring.cpu_memory_disk import get_resource_usage


class MainWindow(QMainWindow):
    """
    Main application window.
    Provides navigation between features using a sidebar.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Management Tools")
        self.resize(1000, 600)

        # Central layout (horizontal split)
        main_layout = QHBoxLayout()

        # ---------- Sidebar ----------
        sidebar = QVBoxLayout()
        self.server_list_btn = QPushButton("📋 Server List")
        self.terminal_btn = QPushButton("💻 Terminal")
        self.monitor_btn = QPushButton("📊 Monitoring")
        self.logs_btn = QPushButton("📑 Logs")
        self.shell_btn = QPushButton("⚙️ Shell Exec")

        sidebar.addWidget(self.server_list_btn)
        sidebar.addWidget(self.terminal_btn)
        sidebar.addWidget(self.monitor_btn)
        sidebar.addWidget(self.logs_btn)
        sidebar.addWidget(self.shell_btn)
        sidebar.addStretch(1)

        # ---------- Content Area (dynamic) ----------
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        # Add sidebar and content area to main layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.content_area, 4)

        # Set main layout into the window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect buttons to views
        self.server_list_btn.clicked.connect(self.show_server_list)
        self.terminal_btn.clicked.connect(self.show_terminal)
        self.monitor_btn.clicked.connect(self.show_monitoring)
        self.logs_btn.clicked.connect(self.show_logs)
        self.shell_btn.clicked.connect(self.show_shell_exec)

        # Show welcome screen on startup
        self.show_welcome_message()

    # ---------- Helper to clear content ----------
    def clear_content_area(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # ---------- Views ----------
    def show_welcome_message(self):
        self.clear_content_area()
        from PyQt5.QtWidgets import QLabel
        label = QLabel("Welcome to Smart Management Tools!\nUse the sidebar to navigate.")
        label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(label)

    def show_server_list(self):
        self.clear_content_area()
        server_ui = ServerListUI()
        self.content_layout.addWidget(server_ui)

    def show_terminal(self):
        self.clear_content_area()
        terminal_ui = TerminalUI()  # ✅ Load actual terminal UI
        self.content_layout.addWidget(terminal_ui)
        #from PyQt5.QtWidgets import QLabel
        #label = QLabel("💻 Terminal UI will appear here.")
        #self.content_layout.addWidget(label)

    def show_monitoring(self):
        self.clear_content_area()

        # ✅ Add the resource graph widget below the label
        from features.server_monitoring.resource_graph import ResourceGraph
        from features.server_monitoring.cpu_memory_disk import get_resource_usage
        # Import the active SSH client
        from features.ssh_access.ssh_connect1 import get_active_ssh_client

        ssh_client = get_active_ssh_client()

        if not ssh_client:
            from PyQt5.QtWidgets import QLabel
            label = QLabel("⚠️ No active SSH connection. Open Terminal first.")
            label.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(label)
            return

        # ✅ Show server info label at top
        from PyQt5.QtWidgets import QLabel
        try:
            ip = ssh_client.get_transport().getpeername()[0]
            label = QLabel(f"📡 Monitoring active server: {ip}")
            label.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(label)
        except Exception:
            pass  # In case transport or peername fails

        # Add the resource graph widget to show live usage
        monitor_widget = ResourceGraph(fetch_callback=lambda: get_resource_usage(ssh_client))
        self.content_layout.addWidget(monitor_widget)



    def show_logs(self):
        self.clear_content_area()
        from PyQt5.QtWidgets import QLabel
        label = QLabel("📑 Log viewer will appear here.")
        self.content_layout.addWidget(label)

    def show_shell_exec(self):
        self.clear_content_area()
        from PyQt5.QtWidgets import QLabel
        label = QLabel("⚙️ Shell executor will go here.")
        self.content_layout.addWidget(label)


# Export function
def get_main_window():
    return MainWindow()
