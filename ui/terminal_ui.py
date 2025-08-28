from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel, QHBoxLayout, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import paramiko, json, os, re

from features.ssh_access.ssh_connect import set_active_ssh_client

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

            set_active_ssh_client(self.client)

            while self.running:
                if self.channel.recv_ready():
                    data = self.channel.recv(1024).decode(errors='ignore')
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

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Font
        self.monospace_font = QFont("Consolas", 11)

        # ========== LEFT PANEL ==========
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(5, 5, 5, 5)
        self.left_panel.setLayout(self.left_layout)

        self.server_list_label = QLabel("Select a server:----")
        self.server_list_widget = QListWidget()
        self.left_layout.addWidget(self.server_list_label)
        self.left_layout.addWidget(self.server_list_widget)

        self.server_list_widget.itemClicked.connect(self.server_selected)

        # ========== RIGHT PANEL ==========
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(5, 5, 5, 5)
        self.right_panel.setLayout(self.right_layout)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(self.monospace_font)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command...")
        self.input_line.setFont(self.monospace_font)
        self.input_line.setEnabled(False)

        self.run_btn = QPushButton("▶ Run Command")
        self.run_btn.setEnabled(False)

        self.right_layout.addWidget(self.output_area)
        self.right_layout.addWidget(self.input_line)
        self.right_layout.addWidget(self.run_btn)

        # ========== Splitter (Resizable Panels) ==========
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

        # ========== Events ==========
        self.run_btn.clicked.connect(self.send_command)
        self.input_line.returnPressed.connect(self.send_command)

        # State
        self.worker = None
        self.active_server_ip = None
        self.servers = []

        self.load_servers()

    def load_servers(self):
        self.server_list_widget.clear()

        if not os.path.exists(SERVER_STORE):
            self.server_list_widget.addItem("No servers found.")
            return

        try:
            with open(SERVER_STORE, "r") as f:
                data = json.load(f)

            if isinstance(data, dict) and "servers" in data:
                self.servers = data["servers"]
            elif isinstance(data, list):
                self.servers = data
            else:
                self.server_list_widget.addItem("Invalid server data format.")
                return

            for srv in self.servers:
                ip = srv.get("ip")
                user = srv.get("username")
                if ip and user:
                    self.server_list_widget.addItem(f"{ip} ({user})")

        except Exception as e:
            self.server_list_widget.addItem(f"Error loading server store: {str(e)}")

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

        if self.worker and self.active_server_ip == ip:
            self.output_area.append("✅ Already connected to this server.\n")
            return

        self.output_area.clear()
        self.output_area.append(f"🔌 Connecting to {ip} as {username}...\n")

        # Stop previous worker
        if self.worker:
            self.worker.stop()
            self.worker.wait()

        # Start new SSH worker
        self.worker = SSHWorker(ip, username, password)
        self.worker.data_received.connect(self.append_output)
        self.worker.error.connect(self.show_error)
        self.worker.start()

        self.active_server_ip = ip
        self.run_btn.setEnabled(True)
        self.input_line.setEnabled(True)
        self.input_line.setFocus()

    def append_output(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_text = ansi_escape.sub('', text)

        cursor = self.output_area.textCursor()
        cursor.movePosition(cursor.End)
        self.output_area.setTextCursor(cursor)

        self.output_area.insertPlainText(clean_text)
        self.output_area.ensureCursorVisible()

    def send_command(self, cmd=None):
        if cmd is None:
            cmd = self.input_line.text().strip()
        if not cmd or not self.worker:
            return
        self.worker.send_command(cmd)
        self.input_line.clear()

    def show_error(self, msg):
        self.output_area.append(f"\n❌ {msg}\n")
        self.run_btn.setEnabled(False)
        self.input_line.setEnabled(False)

    def refresh_ssh_client(self):
        if self.worker and self.worker.client:
            set_active_ssh_client(self.worker.client)
        else:
            set_active_ssh_client(None)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_ssh_client()

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        event.accept()
