import sys
from PyQt5.QtWidgets import QApplication
from ui.server_list_ui import ServerListUI

def main():
    app = QApplication(sys.argv)
    window = ServerListUI()   # Load your Server List UI
    window.show()             # Show the window
    sys.exit(app.exec_())     # Start the app loop

if __name__ == "__main__":
    main()
