import json
from pathlib import Path

SERVER_STORE_PATH = Path(__file__).resolve().parent / "server_store.json"


def remove_server(index: int) -> bool:
    """
    Remove a server by its index in the JSON file.
    Returns True if removed, False otherwise.
    """
    try:
        if not SERVER_STORE_PATH.exists():
            return False

        data = json.loads(SERVER_STORE_PATH.read_text(encoding="utf-8"))

        if "servers" not in data or index < 0 or index >= len(data["servers"]):
            return False

        removed = data["servers"].pop(index)
        SERVER_STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Removed server: {removed}")
        return True
    except Exception as e:
        print(f"Error removing server: {e}")
        return False
