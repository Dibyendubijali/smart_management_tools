from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTextEdit
)
from PyQt5.QtCore import Qt

from ui.server_list_ui import ServerListUI
from ui.terminal_ui import TerminalUI
from features.server_monitoring.resource_graph import ResourceGraph
from features.server_monitoring.cpu_memory_disk import get_resource_usage
from features.ssh_access.ssh_connect import get_active_ssh_client
from features.process_logs.log_viewer import fetch_logs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Management Tools")
        self.resize(1000, 600)

        main_layout = QHBoxLayout()

        # Sidebar
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

        # Main content area
        self.content_area = QStackedWidget()

        self.server_list_ui = ServerListUI()
        self.terminal_ui = TerminalUI()
        self.monitor_widget = QWidget()
        self.logs_ui = QTextEdit()
        self.logs_ui.setReadOnly(True)
        self.shell_exec_ui = QLabel("⚙️ Shell executor will go here.")
        self.shell_exec_ui.setAlignment(Qt.AlignCenter)

        self.content_area.addWidget(self.server_list_ui)
        self.content_area.addWidget(self.terminal_ui)
        self.content_area.addWidget(self.monitor_widget)
        self.content_area.addWidget(self.logs_ui)
        self.content_area.addWidget(self.shell_exec_ui)

        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.content_area, 4)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Button signals
        self.server_list_btn.clicked.connect(lambda: self.content_area.setCurrentWidget(self.server_list_ui))
        self.terminal_btn.clicked.connect(self.show_terminal)
        self.monitor_btn.clicked.connect(self.show_monitoring)
        self.logs_btn.clicked.connect(self.show_logs)
        self.shell_btn.clicked.connect(lambda: self.content_area.setCurrentWidget(self.shell_exec_ui))

        # Default page
        self.content_area.setCurrentWidget(self.server_list_ui)

    def show_terminal(self):
        # When terminal tab is opened, refresh active ssh client from terminal UI
        self.terminal_ui.refresh_ssh_client()
        self.content_area.setCurrentWidget(self.terminal_ui)

    def show_monitoring(self):
        ssh_client = get_active_ssh_client()

        # Clear previous monitor widget layout/widgets if any
        for i in reversed(range(self.monitor_widget.layout().count()) if self.monitor_widget.layout() else []):
            widget = self.monitor_widget.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

        layout = QVBoxLayout()
        self.monitor_widget.setLayout(layout)

        if not ssh_client or not ssh_client.get_transport() or not ssh_client.get_transport().is_active():
            label = QLabel("⚠️ No active SSH connection. Please open a Terminal connection first.")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        else:
            try:
                ip = ssh_client.get_transport().getpeername()[0]
                label = QLabel(f"📡 Monitoring active server: {ip}")
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

                monitor_graph = ResourceGraph(fetch_callback=lambda: get_resource_usage(ssh_client))
                layout.addWidget(monitor_graph)
            except Exception as e:
                label = QLabel(f"❌ Error getting monitoring data.\nTry reconnecting the terminal.\nError: {str(e)}")
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

        self.content_area.setCurrentWidget(self.monitor_widget)

    def show_logs(self):
        ssh_client = get_active_ssh_client()

        if not ssh_client or not ssh_client.get_transport() or not ssh_client.get_transport().is_active():
            self.logs_ui.setPlainText("⚠️ No active SSH connection. Please open a Terminal connection first.")
        else:
            try:
                logs = fetch_logs(ssh_client)
                self.logs_ui.setPlainText(logs.strip() if logs else "⚠️ No logs found.")
            except Exception:
                self.logs_ui.setPlainText("❌ Failed to fetch logs. SSH session may be closed.")

        self.content_area.setCurrentWidget(self.logs_ui)
