import logging

logger = logging.getLogger("shell_command")

def execute_command(ssh_client, command: str):
    """
    Execute a shell command on the remote server via SSH.
    Returns stdout and stderr output as strings.
    """
    try:
        logger.info("Executing command: %s", command)
        stdin, stdout, stderr = ssh_client.exec_command(command)

        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        if errors:
            logger.warning("Command returned error: %s", errors)
            return output, errors
        return output, None
    except Exception as e:
        logger.error("Failed to execute command: %s", e)
        return None, str(e)
