#feature/ssh_access/ssh_connect.py
import paramiko
import logging

logger = logging.getLogger("ssh_connect")

# 🔁 Global variable to store the active SSH client
_active_ssh_client = None


def set_active_ssh_client(client):
    """
    Save a globally accessible SSH client instance.
    """
    global _active_ssh_client
    _active_ssh_client = client


def get_active_ssh_client():
    """
    Retrieve the active SSH client, if connected and still alive.
    """
    global _active_ssh_client
    if _active_ssh_client is not None:
        try:
            # ✅ Check if the client is still connected
            transport = _active_ssh_client.get_transport()
            if transport and transport.is_active():
                return _active_ssh_client
        except Exception:
            pass
    return None


def create_ssh_client(ip: str, port: int, username: str, password: str = "", key_file: str = None):
    """
    Create and return an SSH client connection using Paramiko.
    Supports password or key-based authentication.
    Returns a connected SSHClient object or None on failure.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if key_file:
            logger.info("Connecting to %s with SSH key", ip)
            pkey = paramiko.RSAKey.from_private_key_file(key_file)
            client.connect(ip, port=port, username=username, pkey=pkey, timeout=10)
        else:
            logger.info("Connecting to %s with password", ip)
            client.connect(ip, port=port, username=username, password=password, timeout=10)

        logger.info("SSH connection established to %s:%d", ip, port)

        # ✅ Save this client globally
        set_active_ssh_client(client)

        return client

    except Exception as e:
        logger.error("Failed to connect to %s:%d: %s", ip, port, e)
        return None
