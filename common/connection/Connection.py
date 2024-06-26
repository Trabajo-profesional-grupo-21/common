import pika
from .WorkQueue import WorkQueue
from .ExchangeQueue import ExchangeQueue
import logging

class Connection:
    def __init__(self, host="rabbitmq", port=5672, virtual_host="/", user=None, password=None):
        try:

            credentials = None
            if user and password:
                credentials = pika.PlainCredentials(user, password)
                parameters = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials, heartbeat=1800)
            else:
                parameters = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, heartbeat=1800)

            # parameters = pika.ConnectionParameters(host, port=port, virtual_host=virtual_host, credentials=credentials, heartbeat=1800)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self._active_connection = True
            self._active_channel = False
        except Exception as e:
            logging.error(f'Error init connection. error: {e}')

    def Consumer(self, queue_name):
        return WorkQueue(self.channel, queue_name)

    def Producer(self, queue_name):
        return WorkQueue(self.channel, queue_name)

    def Publisher(self, exchange_name, exchange_type):
        return ExchangeQueue("pub", self.channel, exchange_name, exchange_type)

    def Subscriber(self, exchange_name, exchange_type, queue_name, routing_keys=None):
        return ExchangeQueue("sub", self.channel, exchange_name, exchange_type, queue_name, routing_keys)


    # def EofConsumer(self, output_exchange, output_queue, input_queue):
    #     return EofQueue(self.channel, output_exchange, output_queue, input_queue)

    def start_consuming(self):
        if self._active_channel:
            raise Exception("Channel Already Active Consuming other data")
        self._active_channel = True
        self.channel.start_consuming()


    def stop_consuming(self):
        if not self._active_channel:
            raise Exception("Already Stopped Channel")
        self.channel.stop_consuming()
        self._active_channel = False


    def stop_basic_consume(self, basic_id):
        self.channel.basic_cancel(consumer_tag=basic_id)


    def close(self):
        try:
            if self._active_channel:
                self._active_channel = False
                self.channel.stop_consuming()
            if not self._active_connection:
                raise Exception("Already Stopped")
            self._active_connection = False
            self.connection.close()
        except Exception as e:
            logging.error(f"Connection: error closing connection | error: {e}")