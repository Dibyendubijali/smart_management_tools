import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox
)


# Import backend logic
from features.server_registration.add_server import add_server
from features.server_registration.remove_server import remove_server

#SERVER_STORE_PATH = Path("features/server_registration/server_store.json")
SERVER_STORE_PATH = Path(__file__).resolve().parent.parent / "features" / "server_registration" / "server_store.json"

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
            try:
                data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))
                servers = data.get("servers", [])
                for server in servers:
                    # Ensure server is a dict
                    if isinstance(server, dict):
                        ip = server.get("ip", "N/A")
                        user = server.get("username", "N/A")
                        self.server_list.addItem(f"{ip} ({user})")
                    else:
                        # Log or show error if server entry malformed
                        print(f"Error parsing server entry: expected dict but got {type(server)}")
                        self.server_list.addItem("⚠️ Error parsing server entry")
            except Exception as e:
                print(f"Failed to load servers: {e}")
                self.server_list.addItem("⚠️ Failed to load servers")
        else:
            self.server_list.addItem("No servers registered yet.")

    def add_server(self):
        """Add a server to JSON file."""
        ip = self.ip_input.text().strip()
        user = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not ip or not user:
            QMessageBox.warning(self, "Error", "IP and Username are required!")
            return

        success = add_server(ip, user, password)
        if not success:
            QMessageBox.warning(self, "Error", "Server already exists or failed to add.")
        else:
            QMessageBox.information(self, "Success", f"Server {ip} added!")
            self.ip_input.clear()
            self.user_input.clear()
            self.pass_input.clear()
            self.load_servers()

    def remove_server(self):
        """Trigger removing a server via backend function."""
        selected = self.server_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Select a server to remove!")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove the selected server?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        success = remove_server(selected)
        if success:
            QMessageBox.information(self, "Removed", "Server removed successfully.")
            self.load_servers()
        else:
            QMessageBox.warning(self, "Error", "Failed to remove server.")