from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psutil
import platform
from airflow.utils.dates import days_ago
import logging
from kafka import KafkaProducer  # Corrected import
import json

# Correctly placed Kafka Producer Setup
def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )




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

def get_device_type():
    """Determine the type of device (VM, VPC, Physical, Cloud)"""
    try:
        # Check for common virtualization markers
        with open('/proc/cpuinfo') as f:
            cpuinfo = f.read()
        
        if os.path.exists('/.dockerenv'):
            return 'Container'
        elif os.path.exists('/sys/hypervisor/type'):
            with open('/sys/hypervisor/type') as f:
                hypervisor = f.read().strip()
            return f'VM-{hypervisor}'
        elif 'hypervisor' in cpuinfo.lower():
            return 'VM-Unknown'
        elif os.path.exists('/sys/class/dmi/id/product_uuid'):
            # Check for cloud provider specific metadata
            try:
                requests.get('http://169.254.169.254/latest/meta-data/', timeout=1)
                return 'AWS-Instance'
            except:
                try:
                    requests.get('http://metadata.google.internal', timeout=1)
                    return 'GCP-Instance'
                except:
                    return 'Physical-Machine'
        return 'Physical-Machine'
    except:
        return 'Unknown'

def monitor_system():
    """Function to collect system metrics and send them to Kafka."""
    producer = create_kafka_producer()
    topic_name = 'system_metrics'

    # Get device type
    device_type = get_device_type()

    # Collect metrics
    system_info = {
        "device_type": device_type,
        "os_info": get_os_info(),
        "cpu_usage": get_cpu_usage(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage(),
        "network_io": get_network_io(),
        "timestamp": datetime.now().isoformat()
    }

    # Send the data to Kafka
    try:
        producer.send(topic_name, system_info).get(timeout=10) 
        logging.info("System metrics sent to Kafka successfully.")
    except Exception as e:
        logging.error(f"Failed to send system metrics to Kafka: {e}")
    finally:
        producer.flush()
    # Log the action
    logging.info("System metrics sent to Kafka successfully.")

# Airflow DAG and Task Configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'system_monitoring_kafka',
    default_args=default_args,
    description='DAG for monitoring system metrics and sending them to Kafka',
    schedule_interval=timedelta(minutes=5), 
    catchup=False,
) as dag:

    monitor_task = PythonOperator(
        task_id='monitor_system_metrics',
        python_callable=monitor_system,
    )