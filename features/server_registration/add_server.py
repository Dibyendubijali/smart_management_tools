import json
from pathlib import Path

SERVER_STORE_PATH = Path(__file__).resolve().parent / "server_store.json"


def add_server(ip: str, username: str, password: str = "", port: int = 22) -> bool:
    """
    Add a new server to server_store.json.
    Returns True if successful, False otherwise.
    """
    try:
        # Ensure file exists
        if not SERVER_STORE_PATH.exists():
            SERVER_STORE_PATH.write_text(json.dumps({"servers": []}, indent=2), encoding="utf-8")

        data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))

        if "servers" not in data:
            data["servers"] = []

        # Check for duplicates
        for srv in data["servers"]:
            if srv["ip"] == ip and srv["username"] == username:
                return False  # already exists

        # Add new server
        data["servers"].append({
            "ip": ip,
            "port": port,
            "username": username,
            "password": password
        })

        SERVER_STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error adding server: {e}")
        return False
