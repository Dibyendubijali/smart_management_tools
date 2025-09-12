# features/remote_shell/shell_command.py
import logging

logger = logging.getLogger("shell_command")

def execute_command(ssh_client, command: str):
    """
    Execute a shell command on the remote server via SSH using a PTY and TERM environment.
    Returns stdout and stderr output as strings.
    """
    import time

    try:
        logger.info("Executing command with PTY: %s", command)
        transport = ssh_client.get_transport()
        if not transport or not transport.is_active():
            return None, "SSH transport is inactive."

        session = transport.open_session()
        session.get_pty(term='xterm')  # 🔧 Allocate a PTY
        session.exec_command(command)

        time.sleep(1.0)  # ⏳ Let command produce output

        stdout = session.recv(65535).decode(errors="ignore")
        stderr = session.recv_stderr(65535).decode(errors="ignore")

        if stderr:
            logger.warning("Command error output: %s", stderr)
            return stdout, stderr

        return stdout, None

    except Exception as e:
        logger.error("Failed to execute command: %s", e)
        return None, str(e)
