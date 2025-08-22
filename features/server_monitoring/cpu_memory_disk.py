import logging

logger = logging.getLogger("cpu_memory_disk")

def get_resource_usage(ssh_client):
    """
    Get CPU, memory, and disk usage from the remote server via SSH.
    Returns a dictionary with usage stats.
    """
    try:
        usage = {}

        # CPU Usage
        stdin, stdout, _ = ssh_client.exec_command("top -bn1 | grep 'Cpu(s)'")
        cpu_line = stdout.read().decode()
        if cpu_line:
            cpu_usage = cpu_line.split(",")[0].split(":")[-1].strip()
            usage["cpu"] = cpu_usage

        # Memory Usage
        stdin, stdout, _ = ssh_client.exec_command("free -m")
        mem_lines = stdout.readlines()
        if len(mem_lines) > 1:
            mem_data = mem_lines[1].split()
            total, used = int(mem_data[1]), int(mem_data[2])
            usage["memory"] = round((used / total) * 100, 2)

        # Disk Usage
        stdin, stdout, _ = ssh_client.exec_command("df -h / | tail -1")
        disk_line = stdout.read().decode().split()
        if disk_line:
            usage["disk"] = disk_line[4]  # e.g., '40%'

        return usage
    except Exception as e:
        logger.error("Failed to fetch resource usage: %s", e)
        return {"cpu": None, "memory": None, "disk": None}
