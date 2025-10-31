# Kafka Docker Setup Guide

A complete guide for setting up Apache Kafka using Docker Compose with KRaft mode (no Zookeeper required).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Working with Topics](#working-with-topics)
- [Testing Message Flow](#testing-message-flow)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Key Success Points](#key-success-points)
- [Connection Details](#connection-details)
- [Cleanup](#cleanup)
- [Architecture Notes](#architecture-notes)

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### 1. Create Docker Compose File

Create a file named `docker-compose.yml`:
```yaml
version: '3.8'
services:
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: kafka
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093,PLAINTEXT_HOST://0.0.0.0:29092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      CLUSTER_ID: z1IhO92KQeO7JkTnsPq4PA
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "kafka-topics", "--list", "--bootstrap-server", "kafka:9092"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2. Start Kafka
```bash
# Start the container
docker-compose up -d

# Check if container is running
docker ps

# Check logs to ensure Kafka started successfully
docker logs kafka
```

Wait 30-60 seconds for Kafka to be fully ready. Look for "Kafka Server started" in the logs.

### 3. Access Kafka Container
```bash
docker exec -it kafka bash
```

## Working with Topics

### Create a Topic
```bash
# Create a new topic
kafka-topics --create \
  --topic test-topic \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1

# List all topics
kafka-topics --list --bootstrap-server kafka:9092

# Describe topic details
kafka-topics --describe --topic test-topic --bootstrap-server kafka:9092
```

## Testing Message Flow

### Step 1: Start Consumer (Terminal 1)

**Important:** Always start the consumer BEFORE the producer.
```bash
# Inside the Kafka container
kafka-console-consumer \
  --topic test-topic \
  --bootstrap-server kafka:9092 \
  --from-beginning \
  --group test-group
```

You should see: `Processed a total of 0 messages`. The consumer will wait for incoming messages.

### Step 2: Start Producer (Terminal 2)

Open a new terminal and run:
```bash
# Access the container
docker exec -it kafka bash

# Start the producer
kafka-console-producer \
  --topic test-topic \
  --bootstrap-server kafka:9092
```

You'll see a prompt: `>`

### Step 3: Send Messages

In Terminal 2 (Producer), type messages and press Enter:
```
> Hello World
> This is message 2
> Testing Kafka
```

In Terminal 1 (Consumer), you should immediately see:
```
Hello World
This is message 2
Testing Kafka
```

## Verification

Check consumer group status:
```bash
kafka-consumer-groups \
  --bootstrap-server kafka:9092 \
  --group test-group \
  --describe
```

This displays partition assignments and consumer offsets.

## Troubleshooting

### Messages Not Appearing

1. **Check container health:**
```bash
   docker logs kafka
```

2. **Restart the container:**
```bash
   docker-compose down
   docker-compose up -d
   # Wait 60 seconds, then retry from Step 3
```

3. **Try a different topic:**
```bash
   # Create new debug topic
   kafka-topics --create \
     --topic debug-topic \
     --bootstrap-server kafka:9092 \
     --partitions 1 \
     --replication-factor 1

   # Start consumer
   kafka-console-consumer \
     --topic debug-topic \
     --bootstrap-server kafka:9092 \
     --from-beginning \
     --group debug-group

   # Start producer (in another terminal)
   kafka-console-producer \
     --topic debug-topic \
     --bootstrap-server kafka:9092
```

## Key Success Points

- ✅ Always start consumer BEFORE producer
- ✅ Use `--from-beginning` flag on consumer
- ✅ Use a consumer group with `--group` flag
- ✅ Wait for consumer to show "Processed a total of 0 messages"
- ✅ Both consumer and producer must use same `bootstrap-server: kafka:9092`
- ✅ Allow 30-60 seconds for Kafka to fully start

## Connection Details

- **Internal (container-to-container):** `kafka:9092`
- **External (host machine):** `localhost:29092`

## Cleanup
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Architecture Notes

This setup uses **KRaft mode** (Kafka Raft), which eliminates the need for Zookeeper. The Kafka broker also acts as its own controller, simplifying the deployment for development and testing environments.

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
