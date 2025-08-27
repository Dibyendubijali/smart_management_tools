# features/process_logs/log_viewer.py
import logging

logger = logging.getLogger("log_viewer")

def fetch_logs(ssh_client, lines=50):
    log_paths = ["/var/log/syslog", "/var/log/messages"]  # Ubuntu ar CentOS er file
    for log_path in log_paths:
        try:
            command = f"tail -n {lines} {log_path}"
            stdin, stdout, stderr = ssh_client.exec_command(command)
            errors = stderr.read().decode()
            if not errors:
                return stdout.read().decode()
        except Exception:
            continue
    return "❌ Unable to fetch logs from known paths (/var/log/syslog, /var/log/messages)."
