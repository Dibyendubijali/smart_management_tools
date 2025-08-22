import logging

logger = logging.getLogger("running_process")

def get_running_processes(ssh_client):
    """
    Fetch list of running processes from the remote server via SSH.
    Returns a list of dictionaries with PID, USER, CPU, MEM, and COMMAND.
    """
    try:
        stdin, stdout, _ = ssh_client.exec_command("ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -n 15")
        lines = stdout.readlines()
        processes = []

        for line in lines[1:]:  # Skip header
            parts = line.split(None, 4)
            if len(parts) == 5:
                pid, user, cpu, mem, command = parts
                processes.append({
                    "pid": pid,
                    "user": user,
                    "cpu": cpu,
                    "mem": mem,
                    "command": command.strip()
                })

        return processes
    except Exception as e:
        logger.error("Failed to fetch running processes: %s", e)
        return []
