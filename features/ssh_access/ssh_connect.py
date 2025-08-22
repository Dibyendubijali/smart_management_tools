import paramiko
import logging

logger = logging.getLogger("ssh_connect")

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
        return client
    except Exception as e:
        logger.error("Failed to connect to %s:%d: %s", ip, port, e)
        return None
