# features/ssh_access/ssh_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
import paramiko
import time
from features.ssh_access.terminal_handler import TerminalHandler

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
        self.input_buffer = []
        self.terminal = TerminalHandler(width=120, height=30)

    def run(self):
        try:
            print(f"[DEBUG] Connecting to {self.ip} as {self.username}")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password, timeout=10)

            self.channel = self.client.invoke_shell(term='xterm', width=120, height=30)
            print("[DEBUG] SSH shell channel opened.")
            self.channel.settimeout(0.1)

            self.data_received.emit(f"[Connected to {self.ip}]\n")

            while self.running:
                if self.channel.recv_ready():
                    raw_data = self.channel.recv(4096).decode(errors='ignore')
                    self.terminal.feed(raw_data)

                    output = self.terminal.get_display()
                    self.data_received.emit(output)

                if self.input_buffer:
                    cmd = self.input_buffer.pop(0)
                    print(f"[DEBUG] Sending command: {cmd}")
                    self.channel.send(cmd + "\n")

                time.sleep(0.05)

        except Exception as e:
            self.error.emit(f"[ERROR] {str(e)}")
            print(f"[ERROR] SSHWorker failed: {e}")

    def send_command(self, command):
        self.input_buffer.append(command)

    def stop(self):
        self.running = False
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
