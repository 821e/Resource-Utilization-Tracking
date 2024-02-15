# **System Documentation: Resource Utilization Tracking System**

## **Overview**

The Resource Utilization Tracking System is designed to monitor and record system metrics across multiple servers or devices. It captures vital statistics such as CPU usage, memory utilization, disk activity, and network I/O, facilitating real-time and historical performance analysis. This document outlines the architecture, components, and step-by-step setup of the system.

## **System Architecture**

The system integrates several technologies, including Python, Go, Apache Airflow, Apache Kafka, and Apache Cassandra, to collect, process, transmit, and store system metrics efficiently.

### **Components:**

1. **Metric Collection Agents**:
    - **Language**: Python
    - **Purpose**: Collect system metrics.
    - **Why Python**: Python's **`psutil`** library provides a convenient and cross-platform way to access system details, making it ideal for gathering metrics.
2. **Task Scheduler**:
    - **Technology**: Apache Airflow
    - **Purpose**: Schedule and execute the metric collection tasks.
    - **Why Airflow**: Airflow offers robust scheduling options, easy monitoring of task execution, and scalability, making it suitable for orchestrating the metric collection process.
3. **Message Broker**:
    - **Technology**: Apache Kafka
    - **Purpose**: Buffer and transmit the collected metrics from producers (agents) to consumers.
    - **Why Kafka**: Kafka excels at handling high-throughput, real-time data streaming, providing a reliable and scalable way to manage data flow.
4. **Data Storage**:
    - **Technology**: Apache Cassandra
    - **Purpose**: Store the metrics data for long-term analysis.
    - **Why Cassandra**: Cassandra's distributed architecture offers scalability and high availability, making it ideal for storing and querying time-series data like system metrics.
5. **Data Processing and Aggregation**:
    - **Language**: Go
    - **Purpose**: Consume metrics from Kafka and insert them into Cassandra.
    - **Why Go**: Go provides efficient concurrency support and fast execution, making it suitable for processing high-volume data streams.

## **Step-by-Step Setup**

### **1. Metric Collection Agents**

- **Setup**:
    - Install Python and **`psutil`** on the target servers/devices.
    - Write a Python script using **`psutil`** to gather system metrics.
- **Example**:
    
    ```python
    import psutil
    
    def get_system_metrics():
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
        }
    ```
    

### **2. Apache Airflow for Scheduling**

- **Setup**:
    - Install Airflow on a central server.
    - Define a DAG to periodically execute the metric collection Python script.
- **Example**:
    
    ```python
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime, timedelta
    
    default_args = {
        'owner': 'airflow',
        'start_date': datetime(2024, 1, 1),
    }
    
    dag = DAG('metric_collection', default_args=default_args, schedule_interval=timedelta(minutes=5))
    
    def collect_metrics():
        # Call your Python metric collection script here
    
    task = PythonOperator(
        task_id='collect_and_send_metrics',
        python_callable=collect_metrics,
        dag=dag,
    )
    ```
    

### **3. Apache Kafka for Data Transmission**

- **Setup**:
    - Install and start Kafka and Zookeeper.
    - Create a Kafka topic for metrics data transmission.
- **Example**:
    
    ```bash
    kafka-topics.sh --create --topic system_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
    

### **4. Apache Cassandra for Data Storage**

- **Setup**:
    - Install Cassandra.
    - Create a keyspace and table for storing metrics.
- **Example**:
    
    ```sql
    CREATE KEYSPACE metrics WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
    CREATE TABLE metrics.system_metrics (
        id UUID PRIMARY KEY,
        timestamp TIMESTAMP,
        cpu_usage DOUBLE,
        memory_usage DOUBLE,
        disk_usage DOUBLE
    );
    ```
    

### **5. Go Application for Data Processing**

- **Setup**:
    - Install Go.
    - Write a Go application that uses the Kafka consumer API to read metrics messages and insert them into Cassandra.
- **Example**:
    
    ```go
    package main
    
    import (
        "github.com/gocql/gocql"
        "github.com/confluentinc/confluent-kafka-go/kafka"
    )
    
    func main() {
        // Kafka consumer setup
        // Cassandra session setup
        // Consume messages and insert into Cassandra
    }
    ```
    

## **Usage**

- **Metric Collection**: Configured to run periodically via Airflow, the Python script