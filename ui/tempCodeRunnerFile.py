from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import paramiko
import json
import os

SERVER_STORE = "features/server_registration/server_store.json"

class SSHWorker(QThread):
    data_received = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, ip, username, password):
        super().__init__()
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None
        self.channel = None
        self.running = True

    def run(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password)
            self.channel = self.client.invoke_shell()
            self.channel.settimeout(0.5)

            while self.running:
                if self.channel.recv_ready():
                    data = self.channel.recv(1024).decode()
                    self.data_received.emit(data)

        except Exception as e:
            self.error.emit(f"Connection error: {str(e)}")

    def send_command(self, cmd):
        if self.channel:
            self.channel.send(cmd + "\n")

    def stop(self):
        self.running = False
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()


class TerminalUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal Access")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Server list
        self.server_list_label = QLabel("Select a server:")
        self.server_list_widget = QListWidget()
        self.server_list_widget.itemClicked.connect(self.server_selected)

        self.layout.addWidget(self.server_list_label)
        self.layout.addWidget(self.server_list_widget)

        # Terminal output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        # Command input and button
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command...")
        self.run_btn = QPushButton("▶ Run Command")

        self.run_btn.setEnabled(False)
        self.input_line.setEnabled(False)

        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.run_btn)

        # Signals
        self.run_btn.clicked.connect(self.send_command)
        self.input_line.returnPressed.connect(self.send_command)

        self.worker = None
        self.servers = []
        self.load_servers()

    def load_servers(self):
        self.server_list_widget.clear()

        if not os.path.exists(SERVER_STORE):
            self.server_list_widget.addItem("No servers found.")
            return

        with open(SERVER_STORE, "r") as f:
            data = json.load(f)

        # Support for dict- or list-based structure
        if isinstance(data, dict):
            self.servers = list(data.values())
        elif isinstance(data, list):
            self.servers = data
        else:
            self.server_list_widget.addItem("Invalid server data format.")
            return

        for srv in self.servers:
            try:
                ip = srv.get("ip", "Unknown IP")
                user = srv.get("username", "Unknown User")
                self.server_list_widget.addItem(f"{ip} ({user})")
            except Exception as e:
                self.server_list_widget.addItem("⚠️ Error parsing server entry")

    def server_selected(self, item):
        index = self.server_list_widget.currentRow()
        if index < 0 or index >= len(self.servers):
            self.output_area.append("⚠️ Invalid server selection.")
            return

        server = self.servers[index]

        ip = server.get("ip")
        username = server.get("username")
        password = server.get("password", "")

        if not ip or not username:
            self.output_area.append("❌ Missing IP or Username.")
            return

        self.output_area.clear()
        self.output_area.append(f"Connecting to {ip} as {username}...\n")

        # Stop old session
        if self.worker:
            self.worker.stop()
            self.worker.wait()

        # Start new session
        self.worker = SSHWorker(ip, username, password)
        self.worker.data_received.connect(self.append_output)
        self.worker.error.connect(self.show_error)
        self.worker.start()

        self.run_btn.setEnabled(True)
        self.input_line.setEnabled(True)
        self.input_line.setFocus()

    def append_output(self, text):
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.output_area.insertPlainText(text)

    def send_command(self):
        cmd = self.input_line.text().strip()
        if not cmd or not self.worker:
            return
        self.worker.send_command(cmd)
        self.input_line.clear()

    def show_error(self, msg):
        self.output_area.append(f"\n❌ {msg}\n")
        self.run_btn.setEnabled(False)
        self.input_line.setEnabled(False)

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        event.accept()
