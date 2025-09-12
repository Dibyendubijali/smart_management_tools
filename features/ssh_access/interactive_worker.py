import logging
logging.basicConfig(level=logging.DEBUG)
from PyQt5.QtCore import QThread, pyqtSignal
import time
import logging
import select

logger = logging.getLogger("interactive_ssh_worker")


class InteractiveSSHWorker(QThread):
    data_received = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, ssh_client):
        super().__init__()
        self.ssh_client = ssh_client
        self.channel = None
        self.running = True
        self.input_buffer = []  # ✅ Queue for commands

    def run(self):
        try:
            self.channel = self.ssh_client.invoke_shell(term='xterm')
            self.channel.settimeout(0.0)

            self.data_received.emit("[✅ Connected: Interactive Shell Started]\n")
            logger.info("SSH interactive shell started.")

            while self.running:
                # ✅ Check if there’s data ready to read
                if self.channel and self.channel.recv_ready():
                    rl, _, _ = select.select([self.channel], [], [], 0.1)
                    if rl:
                        output = self.channel.recv(4096).decode("utf-8", errors="ignore")
                        logger.debug(f"[Received] {output.strip()}")
                        self.data_received.emit(output)

                # ✅ Check if there's any command to send
                if self.input_buffer:
                    cmd = self.input_buffer.pop(0)
                    logger.info(f"[Sending command] {cmd}")
                    self.channel.send(cmd + '\n')

                time.sleep(0.05)  # Small sleep to prevent high CPU usage

        except Exception as e:
            logger.exception("SSHWorker failed")
            self.error.emit(f"❌ SSH Shell Error: {e}")

    def send_command(self, command: str):
        logger.debug(f"[Queueing command] {command}")
        self.input_buffer.append(command)

    def stop(self):
        self.running = False
        if self.channel:
            try:
                self.channel.close()
            except Exception:
                pass
        if self.ssh_client:
            try:
                self.ssh_client.close()
            except Exception:
                pass
