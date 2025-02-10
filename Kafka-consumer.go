package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gocql/gocql"
)

type MetricDetail struct {
	Total      string `json:"total"`
	Used       string `json:"used"`
	Percentage string `json:"percentage"`
}

type SystemMetric struct {
    ID          string             `json:"id"`
    DeviceType  string             `json:"device_type"`
    Timestamp   time.Time          `json:"timestamp"`
    CPUUsage    float64           `json:"cpu_usage"`
    MemoryUsage float64           `json:"memory_usage"`
    DiskUsage   float64           `json:"disk_usage"`
    NetworkIO   map[string]float64 `json:"network_io"`
    OSInfo      map[string]string  `json:"os_info"`
}

func main() {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "myGroup",
		"auto.offset.reset": "earliest",
	})

	if err != nil {
		log.Fatal("Failed to create consumer:", err)
	}

	defer c.Close()
	c.SubscribeTopics([]string{"system_metrics"}, nil)

	cluster := gocql.NewCluster("localhost")
	cluster.Keyspace = "metrics"
	cluster.Consistency = gocql.Quorum
	session, err := cluster.CreateSession()
	if err != nil {
		log.Fatal("Failed to connect to Cassandra:", err)
	}
	defer session.Close()

	for {
		msg, err := c.ReadMessage(-1)
		if err == nil {
			var metric SystemMetric

			if err := json.Unmarshal(msg.Value, &metric); err != nil {
				log.Printf("Error unmarshaling message: %v\n", err)
				continue
			}

			const customFormat = "2006-01-02T15:04:05.000000"
			parsedTime, err := time.Parse(customFormat, metric.Timestamp)
			if err != nil {
				log.Printf("Error parsing timestamp: %v\n", err)
				continue
			}

			metricID := gocql.TimeUUID()

			if err := session.Query(`INSERT INTO system_metrics (id, os_info, cpu_usage, disk_usage, memory_usage, network_io_recv, network_io_sent, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
				metricID, metric.OSInfo, metric.CPUUsage, metric.DiskUsage, metric.MemoryUsage, metric.NetworkIO, parsedTime).Exec(); err != nil {
				log.Println("Error inserting into Cassandra:", err)
			} else {
				fmt.Println("Metric inserted successfully")
			}
		} else {
			log.Printf("Consumer error: %v (%v)\n", err, msg)
		}
	}
}
