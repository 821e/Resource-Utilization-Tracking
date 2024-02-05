import psutil
import time
import platform  

def get_os_info():
    """Returns the name of the operating system."""
    return platform.system() + " " + platform.release()

def get_cpu_usage():
    """Returns the system's CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Returns the system's memory usage details, formatted for readability."""
    memory = psutil.virtual_memory()
    return {
        "total": f"{memory.total / (1024**3):.2f} GB",
        "used": f"{memory.used / (1024**3):.2f} GB",
        "percentage": f"{memory.percent}%"
    }

def get_disk_usage():
    """Returns the disk usage details for the root partition, formatted for readability."""
    disk = psutil.disk_usage('/')
    return {
        "total": f"{disk.total / (1024**3):.2f} GB",
        "used": f"{disk.used / (1024**3):.2f} GB",
        "percentage": f"{disk.percent}%"
    }

def get_network_io():
    """Returns bytes sent and received since boot, formatted for readability."""
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": f"{net_io.bytes_sent / (1024**2):.2f} MB",
        "bytes_recv": f"{net_io.bytes_recv / (1024**2):.2f} MB"
    }

def monitor_system(interval=5):
    """Continuously monitor and print system metrics at specified intervals."""
    print(f"Operating System: {get_os_info()}")
    while True:
        print(f"\nCPU Usage: {get_cpu_usage()}%")
        memory_usage = get_memory_usage()
        print(f"Memory Usage: {memory_usage['used']} / {memory_usage['total']} ({memory_usage['percentage']})")
        disk_usage = get_disk_usage()
        print(f"Disk Usage: {disk_usage['used']} / {disk_usage['total']} ({disk_usage['percentage']})")
        network_io = get_network_io()
        print(f"Network I/O: Sent {network_io['bytes_sent']}, Received {network_io['bytes_recv']}")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_system()
