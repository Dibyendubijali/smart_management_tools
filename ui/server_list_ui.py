import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox
)

SERVER_STORE_PATH = Path("features/server_registration/server_store.json")

class ServerListUI(QWidget):
    """
    UI for listing, adding, and removing servers.
    Reads/writes from server_store.json
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server List")

        layout = QVBoxLayout()

        # Server list display
        self.server_list = QListWidget()
        layout.addWidget(QLabel("Registered Servers:"))
        layout.addWidget(self.server_list)

        # Add server inputs
        form_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP Address")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password (optional)")
        form_layout.addWidget(self.ip_input)
        form_layout.addWidget(self.user_input)
        form_layout.addWidget(self.pass_input)

        layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add Server")
        self.remove_btn = QPushButton("🗑️ Remove Server")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Load servers initially
        self.load_servers()

        # Connect signals
        self.add_btn.clicked.connect(self.add_server)
        self.remove_btn.clicked.connect(self.remove_server)

    def load_servers(self):
        """Load servers from JSON file."""
        self.server_list.clear()
        if SERVER_STORE_PATH.exists():
            data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))
            for server in data.get("servers", []):
                self.server_list.addItem(f"{server['ip']} ({server['username']})")

    def add_server(self):
        """Add a server to JSON file."""
        ip = self.ip_input.text().strip()
        user = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not ip or not user:
            QMessageBox.warning(self, "Error", "IP and Username are required!")
            return

        data = {}
        if SERVER_STORE_PATH.exists():
            data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))

        if "servers" not in data:
            data["servers"] = []

        data["servers"].append({
            "ip": ip,
            "port": 22,
            "username": user,
            "password": password
        })

        SERVER_STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        QMessageBox.information(self, "Success", f"Server {ip} added!")
        self.load_servers()

    def remove_server(self):
        """Remove selected server from JSON file."""
        selected = self.server_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Select a server to remove!")
            return

        data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))
        removed = data["servers"].pop(selected)
        SERVER_STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

        QMessageBox.information(self, "Removed", f"Server {removed['ip']} removed.")
        self.load_servers()
