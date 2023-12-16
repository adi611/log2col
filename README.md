# Log to Columnar Converter

Python-based CLI tool to convert log data to column files.

## Pre-requisites

Make sure Apache Kafka is installed on your system. If not, you can follow the given [link](https://www.confluent.io/blog/set-up-and-run-kafka-on-windows-linux-wsl-2/) to do so.  

### Start Kafka environment

You can follow this [link](https://kafka.apache.org/quickstart) for instructions on starting the Kafka environment. In summary:  

Run the following commands in order to start all services in the correct order:

```
# Start the ZooKeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open another terminal session and run:

```
# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties
```

### Create Kafka topic

```
bin/kafka-topics.sh --create --topic log_topic --bootstrap-server localhost:9092
```
Make sure the topic name is `log_topic`

### Install `kafka-python`

```
pip install kafka-python
```

## Usage

### Using the CLI tool

To run the CLI tool, you can execute it from the command line like this:

```
python log_to_columns.py "input.log" output_columns
```

Replace `input.log` with the path to your input log file, and `output_columns` with the desired output directory.

### Using the Streamlit web app

First, ensure you have Streamlit installed. You can install it via pip:

```
pip install streamlit
```

Run the Streamlit app using the following command in the project directory:

```
streamlit run streamlit_app.py
```

This will start a local development server and open a web page with the Streamlit interface. Users can interact with the UI to perform log-to-column conversion.

### Stop Kafka

When you’re done with the conversion, follow these steps to exit the Kafka environment:

1. Stop the consumer and producer clients with Ctrl+C
2. Stop the Kafka Server with Ctrl+C
3. Run the following command to clean up:

```
rm -rf /tmp/kafka-logs /tmp/zookeeper /tmp/kraft-combined-logs
```# log2col
