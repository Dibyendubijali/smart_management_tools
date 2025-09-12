import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QEvent
from features.ssh_access.terminal_handler import TerminalHandler

class ShellReader(QThread):
    data_ready = pyqtSignal(str)

    def __init__(self, channel, terminal_handler):
        super().__init__()
        self.channel = channel
        self.terminal_handler = terminal_handler
        self._running = True

    def run(self):
        while self._running:
            if self.channel.recv_ready():
                try:
                    raw_data = self.channel.recv(4096).decode(errors='ignore')
                    self.terminal_handler.feed(raw_data)
                    display = self.terminal_handler.get_display()
                    self.data_ready.emit(display)
                except Exception:
                    pass

    def stop(self):
        self._running = False
        self.quit()
        self.wait()

class ShellExecUI(QWidget):
    def __init__(self, ssh_client):
        super().__init__()
        self.ssh_client = ssh_client
        self.channel = None
        self.reader_thread = None
        self.terminal_handler = TerminalHandler(width=120, height=30)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(False)
        self.terminal_output.setStyleSheet("background-color: black; color: white;")
        self.terminal_output.setFont(QFont("Courier New", 10))
        self.terminal_output.setCursorWidth(2)
        self.terminal_output.setWordWrapMode(False)

        layout.addWidget(self.terminal_output)
        self.setLayout(layout)
        self.terminal_output.installEventFilter(self)
        self.append_output("[✔] Connected: Interactive Shell Started\n")
        self.start_shell()

    def start_shell(self):
        if not self.ssh_client:
            self.append_output("[❌] No active SSH client.\n")
            return

        try:
            self.channel = self.ssh_client.invoke_shell(term='xterm', width=120, height=30)
            self.reader_thread = ShellReader(self.channel, self.terminal_handler)
            self.reader_thread.data_ready.connect(self.update_output)
            self.reader_thread.start()
        except Exception as e:
            self.append_output(f"[❌] Failed to start shell: {e}\n")

    def update_output(self, display_text):
        self.terminal_output.blockSignals(True)
        self.terminal_output.setPlainText(display_text)
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.blockSignals(False)

    def append_output(self, text):
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText(text)
        self.terminal_output.moveCursor(QTextCursor.End)

    def eventFilter(self, source, event):
        if source == self.terminal_output and event.type() == QEvent.KeyPress:
            if self.channel is None:
                return True

            key = event.key()

            if key == Qt.Key_Backspace:
                self.channel.send('\x7f')
            elif key in (Qt.Key_Return, Qt.Key_Enter):
                self.channel.send('\r')
            elif key == Qt.Key_Tab:
                self.channel.send('\t')
            elif key == Qt.Key_Left:
                self.channel.send('\x1b[D')
            elif key == Qt.Key_Right:
                self.channel.send('\x1b[C')
            elif key == Qt.Key_Up:
                self.channel.send('\x1b[A')
            elif key == Qt.Key_Down:
                self.channel.send('\x1b[B')
            elif key == Qt.Key_Escape:
                self.channel.send('\x1b')
            else:
                text = event.text()
                if text:
                    self.channel.send(text)

            return True

        return super().eventFilter(source, event)

    def closeEvent(self, event):
        if self.reader_thread:
            self.reader_thread.stop()
        if self.channel:
            self.channel.close()
        event.accept()
