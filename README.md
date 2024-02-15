# **System Documentation: Resource Utilization Tracking System**

## **Overview**

The Resource Utilization Tracking System is designed to monitor and record system metrics across multiple servers or devices. It captures vital statistics such as CPU usage, memory utilization, disk activity, and network I/O, facilitating real-time and historical performance analysis. This document outlines the architecture, components, and step-by-step setup of the system.

## **System Architecture**

The system integrates several technologies, including Python, Go, Apache Airflow, Apache Kafka, and Apache Cassandra, to collect, process, transmit, and store system metrics efficiently.

![DALL·E 2024-02-15 12.19.40 - Create a simple diagram illustrating the flow of data in a Resource Utilization Tracking System. The diagram should include the following components_ .webp](https://prod-files-secure.s3.us-west-2.amazonaws.com/8762a7f1-fcbc-41bc-9cd6-92ade6c47e8d/c5ece942-4325-44f7-ab14-fc2e0e234fb9/DALLE_2024-02-15_12.19.40_-_Create_a_simple_diagram_illustrating_the_flow_of_data_in_a_Resource_Utilization_Tracking_System._The_diagram_should_include_the_following_components__.webp)

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

### **Metric Collection**

The metric collection agents are Python scripts deployed on various servers or devices. These scripts gather key system metrics such as CPU usage, memory utilization, disk activity, and network I/O.

**Example**: Collecting CPU usage percentage.

```python
import psutil

def collect_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage
```

This function can be scheduled to run at regular intervals using Apache Airflow to continuously monitor the system's CPU usage.

**Scheduling with Apache Airflow**

Apache Airflow schedules and executes the metric collection tasks. An Airflow DAG (Directed Acyclic Graph) is defined to periodically call the metric collection scripts.

**Example**: Defining an Airflow DAG to collect metrics every 5 minutes.

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'collect_system_metrics',
    default_args=default_args,
    description='DAG to collect system metrics',
    schedule_interval=timedelta(minutes=5),
)

def task_collect_metrics():
    # Placeholder for metric collection logic
    print("Collecting metrics...")

collect_metrics_operator = PythonOperator(
    task_id='collect_metrics',
    python_callable=task_collect_metrics,
    dag=dag,
)
```

**Data Transmission with Apache Kafka**

The collected metrics are sent to a Kafka topic, serving as a robust, scalable queue that buffers the data before it's processed and stored.

**Example**: Python script snippet to send metrics to Kafka.

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def send_metrics_to_kafka(metrics):
    producer.send('system_metrics', metrics)
    producer.flush()

metrics = {"cpu_usage": collect_cpu_usage()}
send_metrics_to_kafka(metrics)
```

### **Data Storage in Apache Cassandra**

Apache Cassandra stores the metrics data for long-term analysis. It's designed to handle large volumes of data across many commodity servers, providing high availability with no single point of failure.

**Example**: Cassandra table schema for storing system metrics.

```sql
CREATE TABLE system_metrics (
    id uuid PRIMARY KEY,
    timestamp timestamp,
    cpu_usage double,
    memory_usage double,
    disk_usage double,
    network_io_recv double,
    network_io_sent double
);
```

### **Data Processing and Aggregation with Go**

A Go application acts as a Kafka consumer, processing and storing the incoming metrics data into Cassandra.

**Example**: Go snippet to consume metrics from Kafka and insert into Cassandra.

```go
package main

import (
    "github.com/gocql/gocql"
    "github.com/confluentinc/confluent-kafka-go/kafka"
    "encoding/json"
)

func main() {
    // Kafka consumer setup (omitted for brevity)

    // Cassandra session setup (omitted for brevity)

    for {
        msg, err := consumer.ReadMessage(-1)
        if err == nil {
            var metric map[string]float64
            json.Unmarshal(msg.Value, &metric)
            
            // Insert the metric into Cassandra (pseudo-code)
            // session.Query(`INSERT INTO system_metrics (...) VALUES (...)`, ...).Exec()
        }
    }
}
```

### **Usage Scenarios**

- **Performance Monitoring**: Continuously track system performance across multiple servers, identifying trends and potential bottlenecks.
- **Capacity Planning**: Analyze historical data to make informed decisions on scaling resources up or down.
- **Alerting**: Implement logic to trigger alerts based on specific thresholds, such as CPU usage exceeding 90% for an extended period.