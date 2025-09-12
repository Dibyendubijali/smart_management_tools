# features/ssh_access/terminal_handler.py

import pyte


class TerminalHandler:
    """
    Handles terminal screen emulation using pyte.
    Converts raw SSH output (with escape sequences) into clean, rendered text.
    """

    def __init__(self, width=120, height=30):
        self.screen = pyte.Screen(width, height)
        self.stream = pyte.Stream()
        self.stream.attach(self.screen)

    def feed(self, data: str):
        """Feed raw terminal output to the emulator."""
        self.stream.feed(data)

    def get_display(self) -> str:
        """Return the full current screen display as text."""
        return "\n".join(self.screen.display)

    def reset(self):
        """Reset the screen (e.g. on reconnect)."""
        self.screen.reset()


    def reset(self):
        """Reset the screen (e.g. on reconnect)."""
        self.screen.reset()
