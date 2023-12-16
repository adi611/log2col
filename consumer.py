from kafka import KafkaConsumer
import json
import os

def convert_to_columnar(output_directory, topic_name, kafka_server):
    # Create a dictionary to store column data
    columns = {}

    consumer = KafkaConsumer(
        topic_name,
        group_id=None,
        auto_offset_reset='earliest',
        bootstrap_servers=kafka_server,
        value_deserializer=lambda x: x.decode('utf-8'),
        consumer_timeout_ms=3000
    )

    for message in consumer:
        log_data = json.loads(message.value)
        # print(f"{log_data} from consumer")
        # Traverse the JSON data and extract values
        for column_name, value in flatten_dict(log_data).items():
            if column_name not in columns:
                # Open a new column file for writing
                column_file = open(os.path.join(output_directory, f'{column_name}.column'), 'a')
                columns[column_name] = column_file

            # Write the value to the respective column file
            columns[column_name].write(f"{value}\n")

def flatten_dict(d, parent_key='', separator='.'):
    items = {}
    for key, value in d.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key, separator=separator))
        else:
            items[new_key] = value
    return items

if __name__ == '__main__':
    output_directory = 'output_columns'
    topic_name = 'log_topic'
    kafka_server = 'localhost:9092'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    convert_to_columnar(output_directory, topic_name, kafka_server)
