import logging

logger = logging.getLogger("log_viewer")

def fetch_logs(ssh_client, log_path="/var/log/syslog", lines=50):
    """
    Fetch last 'lines' of logs from a given log file.
    Default is /var/log/syslog (for Ubuntu/Debian).
    For CentOS/RHEL, use /var/log/messages.
    """
    try:
        command = f"tail -n {lines} {log_path}"
        stdin, stdout, stderr = ssh_client.exec_command(command)

        errors = stderr.read().decode()
        if errors:
            logger.error("Error fetching logs: %s", errors)
            return f"Error: {errors}"

        return stdout.read().decode()
    except Exception as e:
        logger.error("Failed to fetch logs: %s", e)
        return f"Error: {e}"
