# 

# **توثيق النظام: نظام تتبع استخدام الموارد**

## **نظرة عامة**

نظام تتبع استخدام الموارد مصمم لمراقبة وتسجيل مقاييس النظام عبر عدة خوادم أو أجهزة. يلتقط إحصائيات حيوية مثل استخدام الـ CPU، واستغلال الذاكرة، ونشاط القرص، وإدخال/إخراج الشبكة، مما يسهل تحليل الأداء الزمني الفعلي والتاريخي. يوضح هذا الوثيقة هيكلية النظام، مكوناته، وخطوات الإعداد خطوة بخطوة.

## **هيكلية النظام**

النظام يدمج عدة تقنيات، بما في ذلك Python، Go، Apache Airflow، Apache Kafka، وApache Cassandra، لجمع، معالجة، نقل، وتخزين مقاييس النظام بكفاءة.

![Alt text for image](https://raw.githubusercontent.com/ZeusDevEng/Resource-Utilization-Tracking/main/diagram%20illustrating%20the%20flow%20of%20data%20in%20a%20Resource%20Utilization%20Tracking%20System.webp)

### **المكونات:**

1. **وكلاء جمع المقاييس**:
    - **اللغة**: Python
    - **الغرض**: جمع مقاييس النظام.
    - **ليه Python**: مكتبة **`psutil`** في Python توفر طريقة مريحة ومتعددة المنصات للوصول إلى تفاصيل النظام، مما يجعلها مثالية لجمع المقاييس.
2. **جدولة المهام**:
    - **التقنية**: Apache Airflow
    - **الغرض**: جدولة وتنفيذ مهام جمع المقاييس.
    - **ليه Airflow**: Airflow يوفر خيارات جدولة قوية، مراقبة سهلة لتنفيذ المهام، وقابلية للتوسع، مما يجعله مناسبًا لتنظيم عملية جمع المقاييس.
3. **وسيط الرسائل**:
    - **التقنية**: Apache Kafka
    - **الغرض**: تخزين ونقل المقاييس المجمعة من المنتجين (الوكلاء) إلى المستهلكين.
    - **ليه Kafka**: Kafka ممتاز في التعامل مع بث البيانات الزمنية الفعلية بكميات كبيرة، مما يوفر طريقة موثوقة وقابلة للتوسع لإدارة تدفق البيانات.
4. **تخزين البيانات**:
    - **التقنية**: Apache Cassandra
    - **الغرض**: تخزين بيانات المقاييس للتحليل طويل الأمد.
    - **ليه Cassandra**: هيكلية Cassandra الموزعة توفر قابلية للتوسع وتوافر عالي، مما يجعلها مثالية لتخزين واستعلام البيانات الزمنية مثل مقاييس النظام.
5. **معالجة وتجميع البيانات**:
    - **اللغة**: Go
    - **الغرض**: استهلاك المقاييس من Kafka وإدخالها في Cassandra.
    - **ليه Go**: Go توفر دعم توازي فعال وتنفيذ سريع، مما يجعلها مناسبة لمعالجة تدفقات البيانات الكبيرة الحجم.

## **الإعداد خطوة بخطوة**

### **1. وكلاء جمع المقاييس**

- **الإعداد**:
    - تثبيت Python و****`psutil`*** على الخوادم/الأجهزة المستهدفة.
    - كتابة سكريبت Python باستخدام **`psutil`** لجمع مقاييس النظام.
- **مثال**:
    
    ```python
    import psutil
    
    def get_system_metrics():
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
        }
    
    ```
    

### **2. Apache Airflow للجدولة**

- **الإعداد**:
    - تثبيت Airflow على خادم مركزي.
    - تعريف DAG لتنفيذ سكريبت جمع المقاييس البرمجي بشكل دوري.
- **مثال**:
    
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
        # هنا اتصل بسكريبت جمع المقاييس البرمجي
    
    task = PythonOperator(
        task_id='collect_and_send_metrics',
        python_callable=collect_metrics,
        dag=dag,
    )
    
    ```
    

### **3. Apache Kafka لنقل البيانات**

- **الإعداد**:
    - تثبيت وبدء Kafka وZookeeper.
    - إنشاء موضوع Kafka لنقل بيانات المقاييس.
- **مثال**:
    
    ```bash
    kafka-topics.sh --create --topic system_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    
    ```
    

### **4. Apache Cassandra لتخزين البيانات**

- **الإعداد**:
    - تثبيت Cassandra.
    - إنشاء فضاء مفاتيح وجدول لتخزين المقاييس.
- **مثال**:
    
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
    

### **5. تطبيق Go لمعالجة البيانات**

- **الإعداد**:
    - تثبيت Go.
    - كتابة تطبيق Go يستخدم واجهة استهلاك Kafka لقراءة رسائل المقاييس وإدخالها في Cassandra.
- **مثال**:
    
    ```go
    package main
    
    import (
        "github.com/gocql/gocql"
        "github.com/confluentinc/confluent-kafka-go/kafka"
    )
    
    func main() {
        // إعداد استهلاك Kafka
        // إعداد جلسة Cassandra
        // استهلاك الرسائل وإدخالها في Cassandra
    }
    
    ```
    

## **الاستخدام**

### **جمع المقاييس**

وكلاء جمع المقاييس هم سكريبتات Python موزعة على عدة خوادم أو أجهزة. هذه السكريبتات تجمع مقاييس النظام الرئيسية مثل استخدام الـ CPU، استغلال الذاكرة، نشاط القرص، وإدخال/إخراج الشبكة.

**مثال**: جمع نسبة استخدام الـ CPU.

```python
import psutil

def collect_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

```

يمكن جدولة هذه الوظيفة لتعمل بفترات منتظمة باستخدام Apache Airflow لمراقبة استخدام الـ CPU للنظام باستمرار.

**الجدولة باستخدام Apache Airflow**

Apache Airflow يجدول وينفذ مهام جمع المقاييس. يتم تعريف DAG (Directed Acyclic Graph) في Airflow ليدعو سكريبتات جمع المقاييس بشكل دوري.

**مثال**: تعريف DAG في Airflow لجمع المقاييس كل 5 دقائق.

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
    description='DAG لجمع مقاييس النظام',
    schedule_interval=timedelta(minutes=5),
)

def task_collect_metrics():
    # مكان لمنطق جمع المقاييس
    print("جمع المقاييس...")

collect_metrics_operator = PythonOperator(
    task_id='collect_metrics',
    python_callable=task_collect_metrics,
    dag=dag,
)

```

**نقل البيانات باستخدام Apache Kafka**

ترسل المقاييس المجمعة إلى موضوع Kafka، الذي يعمل كطابور قوي وقابل للتوسع يخزن البيانات قبل معالجتها وتخزينها.

**مثال**: جزء من سكريبت Python لإرسال المقاييس إلى Kafka.

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

### **تخزين البيانات في Apache Cassandra**

Apache Cassandra يخزن بيانات المقاييس للتحليل طويل الأمد. تم تصميمه للتعامل مع حجم كبير من البيانات عبر العديد من الخوادم العادية، موفرًا توافرية عالية بدون نقطة فشل واحدة.

**مثال**: مخطط جدول Cassandra لتخزين مقاييس النظام.

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

### **معالجة وتجميع البيانات باستخدام Go**

تطبيق Go يعمل كمستهلك Kafka، يعالج ويخزن بيانات المقاييس الواردة في Cassandra.

**مثال**: جزء من Go لاستهلاك المقاييس من Kafka وإدخالها في Cassandra.

```go
package main

import (
    "github.com/gocql/gocql"
    "github.com/confluentinc/confluent-kafka-go/kafka"
    "encoding/json"
)

func main() {
    // إعداد مستهلك Kafka (مختصر للإيجاز)

    // إعداد جلسة Cassandra (مختصر للإيجاز)

    for {
        msg, err := consumer.ReadMessage(-1)
        if err == nil {
            var metric map[string]float64
            json.Unmarshal(msg.Value, &metric)

            // إدخال المقياس في Cassandra (رمز وهمي)
            // session.Query(`INSERT INTO system_metrics (...) VALUES (...)`, ...).Exec()
        }
    }
}

```

### **سيناريوهات الاستخدام**

- **مراقبة الأداء**: تتبع الأداء النظامي باستمرار عبر عدة خوادم، تحديد الاتجاهات والنقاط الضعيفة المحتملة.
- **التخطيط السعة**: تحليل البيانات التاريخية لاتخاذ قرارات مستنيرة بشأن زيادة أو تقليل الموارد.
- **التنبيه**: تنفيذ منطق لتفعيل التنبيهات بناءً على عتبات محددة، مثل تجاوز استخدام الـ CPU لـ 90% لفترة ممتدة.
