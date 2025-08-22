import sys
import json
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.main_window import MainWindow
from ui.main_window import get_main_window



# -----------------------------
# Project Paths
# -----------------------------
ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
UI_DIR = ROOT / "ui"
FEATURES_DIR = ROOT / "features"
LOGS_DIR = ROOT / "logs"
SERVER_REG_DIR = FEATURES_DIR / "server_registration"
SERVER_STORE_PATH = SERVER_REG_DIR / "server_store.json"
APP_LOG_PATH = LOGS_DIR / "app.log"

# -----------------------------
# Ensure folders & files exist
# -----------------------------
def _ensure_scaffold():
    for p in [ASSETS_DIR, UI_DIR, FEATURES_DIR, LOGS_DIR, SERVER_REG_DIR]:
        p.mkdir(parents=True, exist_ok=True)

    if not SERVER_STORE_PATH.exists():
        SERVER_STORE_PATH.write_text(json.dumps({"servers": []}, indent=2))

    if not APP_LOG_PATH.exists():
        APP_LOG_PATH.touch()

_ensure_scaffold()

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(APP_LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("smart_management_tools")

# -----------------------------
# Attempt to load real MainWindow (from ui/main_window.py)
# Fallback to a temporary stub window until you add that file.
# -----------------------------
MainWindowClass = None
try:
    # You will add this file shortly
    from ui.main_window import MainWindow as RealMainWindow  # type: ignore
    MainWindowClass = RealMainWindow
except Exception as e:
    logger.warning("ui/main_window.py not found or failed to import. Using stub window. Details: %s", e)

    class MainWindow(QMainWindow):
        """Temporary placeholder until ui/main_window.py is implemented."""
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Smart Management Tools (Stub)")
            self.resize(900, 600)

    MainWindowClass = MainWindow


# -----------------------------
# Load servers helper (simple)
# Real helpers will live in utils/config_loader.py (coming next)
# -----------------------------
def load_servers() -> dict:
    try:
        data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))
        if "servers" not in data or not isinstance(data["servers"], list):
            raise ValueError("Malformed server_store.json: missing 'servers' list.")
        return data
    except Exception as exc:
        logger.exception("Failed to load servers: %s", exc)
        return {"servers": []}


def save_servers(data: dict) -> None:
    try:
        SERVER_STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as exc:
        logger.exception("Failed to save servers: %s", exc)


# -----------------------------
# Application bootstrap
# -----------------------------
def main():
    app = QApplication(sys.argv)

    # Basic sanity check for JSON store
    data = load_servers()
    logger.info("Loaded %d server(s) from %s", len(data.get("servers", [])), SERVER_STORE_PATH)

    window = MainWindowClass()
    window.show()

    # Friendly heads-up if running with the stub
    if window.windowTitle().endswith("(Stub)"):
        QMessageBox.information(
            window,
            "Welcome 👋",
            "You're running the skeleton app.\n\n"
            "Next, add the real UI file at:\nui/main_window.py\n\n"
            "Say 'next' and I'll send it (with README.md or utils next)."
        )

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
