import argparse
import os
import time
import psutil
import resource
import multiprocessing
from producer import produce_to_kafka
from consumer import convert_to_columnar
import ctypes

def main():
    parser = argparse.ArgumentParser(description='Convert JSON logs to columnar files using Apache Kafka with multiprocessing.')
    parser.add_argument('input_file', type=str, help='Path to the input log file')
    parser.add_argument('output_directory', type=str, help='Path to the output directory for column files')

    args = parser.parse_args()

    def record_ram_usage(max_ram_usage):
        process = psutil.Process(os.getpid())
        while True:
            mem_info = process.memory_info()
            current_ram_usage = mem_info.rss / (1024 * 1024)  # RAM usage in MB
            max_ram_usage.value = max(max_ram_usage.value, current_ram_usage)
            time.sleep(1)

    max_ram_usage = multiprocessing.Value(ctypes.c_float, 0)  # Shared variable to store max RAM usage

    # Start a thread to record RAM usage
    ram_usage_process = multiprocessing.Process(target=record_ram_usage, args=(max_ram_usage,))
    ram_usage_process.start()

    start_time = time.time()  # Record the start time

    # Create Kafka producer to send data to Kafka topic
    input_file = args.input_file
    topic_name = 'log_topic'
    kafka_server = 'localhost:9092'

    # Create Kafka consumer to process log data from Kafka topic
    output_directory = args.output_directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Use multiprocessing to parallelize the producer and consumer tasks
    consumer_process = multiprocessing.Process(target=convert_to_columnar, args=(output_directory, topic_name, kafka_server))
    producer_process = multiprocessing.Process(target=produce_to_kafka, args=(input_file, topic_name, kafka_server))

    consumer_process.start()
    producer_process.start()

    consumer_process.join()
    producer_process.join()

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time

    # Terminate the RAM usage monitoring thread
    ram_usage_process.terminate()

    print(f"Conversion took {elapsed_time:.2f} seconds")
    print(f"Max. RAM Usage: {max_ram_usage.value:.2f} MB")

if __name__ == '__main__':
    main()
