from kafka import KafkaProducer

def produce_to_kafka(input_file, topic_name, kafka_server):
    producer = KafkaProducer(bootstrap_servers=kafka_server)

    with open(input_file, 'r') as f:
        for line in f:
            # print(f"{line} from producer")
            # Send each line of the log file as a message to the Kafka topic
            producer.send(topic_name, line.encode('utf-8'))
    
    producer.flush()
    producer.close()

if __name__ == '__main__':
    input_file = 'dummy.log'
    topic_name = 'log_topic'
    kafka_server = 'localhost:9092'

    produce_to_kafka(input_file, topic_name, kafka_server)
