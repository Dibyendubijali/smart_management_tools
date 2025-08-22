from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class TerminalUI(QWidget):
    """
    Simple terminal-like interface for SSH sessions.
    This will later integrate with ssh_helper and terminal_handler.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal Access")

        layout = QVBoxLayout()

        # Output display
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        # Input field
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command...")
        layout.addWidget(self.input_line)

        # Execute button
        self.run_btn = QPushButton("▶ Run Command")
        layout.addWidget(self.run_btn)

        # Connect signals
        self.run_btn.clicked.connect(self.execute_command)
        self.input_line.returnPressed.connect(self.execute_command)

        self.setLayout(layout)

    def execute_command(self):
        """Placeholder for running commands (to be linked with SSH later)."""
        cmd = self.input_line.text().strip()
        if not cmd:
            return

        # For now, just echo back
        self.output_area.append(f"$ {cmd}")
        self.output_area.append(f"(Executed placeholder for: {cmd})\n")

        self.input_line.clear()
