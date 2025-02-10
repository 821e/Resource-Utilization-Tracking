import paramiko
import json

class RemoteCollector:
    def __init__(self, host, port, username, key_file=None, password=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_file:
            self.ssh.connect(host, port, username, key_filename=key_file)
        else:
            self.ssh.connect(host, port, username, password=password)

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode()

    def get_metrics(self):
        # Commands to get metrics on remote system
        commands = {
            'cpu': "python3 -c 'import psutil; print(psutil.cpu_percent())'",
            'memory': "python3 -c 'import psutil; print(psutil.virtual_memory().percent)'",
            'disk': "python3 -c 'import psutil; print(psutil.disk_usage(\"/\").percent)'"
        }
        
        metrics = {}
        for metric, command in commands.items():
            metrics[metric] = float(self.execute_command(command))
        return metrics

    def close(self):
        self.ssh.close()