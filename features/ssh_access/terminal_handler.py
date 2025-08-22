import logging
from PyQt5.QtCore import QThread, pyqtSignal

logger = logging.getLogger("terminal_handler")

class TerminalWorker(QThread):
    """
    A worker thread that runs a command over SSH and streams the output.
    Emits output lines via signal for live display in the GUI terminal.
    """
    output_ready = pyqtSignal(str)

    def __init__(self, ssh_client, command: str):
        super().__init__()
        self.ssh_client = ssh_client
        self.command = command

    def run(self):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(self.command)
            for line in iter(stdout.readline, ""):
                if line:
                    self.output_ready.emit(line.strip())
            err = stderr.read().decode()
            if err:
                self.output_ready.emit(f"[ERROR] {err}")
        except Exception as e:
            logger.error("Error executing command in terminal: %s", e)
            self.output_ready.emit(f"[ERROR] {e}")
