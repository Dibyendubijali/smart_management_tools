import paramiko
import logging
from typing import Optional

logger = logging.getLogger("ssh_helper")

class SSHHelper:
    """
    A reusable helper for managing SSH connections.
    Supports password and private-key based authentication.
    """

    def __init__(self, hostname: str, port: int = 22, username: str = "", 
                 password: Optional[str] = None, key_file: Optional[str] = None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.client = None

    def connect(self) -> bool:
        """Establish SSH connection using Paramiko."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.key_file:
                logger.info("Connecting to %s using key %s", self.hostname, self.key_file)
                private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    pkey=private_key,
                    timeout=10
                )
            else:
                logger.info("Connecting to %s with password authentication", self.hostname)
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=10
                )

            logger.info("Connected successfully to %s", self.hostname)
            return True
        except Exception as e:
            logger.error("SSH connection failed for %s: %s", self.hostname, e)
            return False

    def run_command(self, command: str) -> str:
        """Run a command remotely and return its output."""
        if not self.client:
            raise RuntimeError("SSH client not connected")

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                logger.warning("Command error on %s: %s", self.hostname, error)
            return output if output else error
        except Exception as e:
            logger.exception("Failed to execute command %s on %s: %s", command, self.hostname, e)
            return f"Error executing command: {e}"

    def close(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed for %s", self.hostname)
            self.client = None
