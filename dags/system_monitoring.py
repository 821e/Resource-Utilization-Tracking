from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psutil
import platform
from airflow.utils.dates import days_ago
import logging


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

def monitor_system():
    """Function to log system metrics, adapted for Airflow task with improved logging."""
    logging.info(f"Operating System: {get_os_info()}")
    logging.info(f"\nCPU Usage: {get_cpu_usage()}%")
    memory_usage = get_memory_usage()
    logging.info(f"Memory Usage: {memory_usage['used']} / {memory_usage['total']} ({memory_usage['percentage']})")
    disk_usage = get_disk_usage()
    logging.info(f"Disk Usage: {disk_usage['used']} / {disk_usage['total']} ({disk_usage['percentage']})")
    network_io = get_network_io()
    logging.info(f"Network I/O: Sent {network_io['bytes_sent']}, Received {network_io['bytes_recv']}")

# Use a context manager to define the DAG
with DAG(
    'system_monitoring',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': days_ago(1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='A simple DAG to monitor system metrics',
    schedule_interval=timedelta(minutes=5),  # Adjust to your preferred interval
    catchup=False,  # Prevents backfilling
) as dag:

    monitor_task = PythonOperator(
        task_id='monitor_system_metrics',
        python_callable=monitor_system,
    )