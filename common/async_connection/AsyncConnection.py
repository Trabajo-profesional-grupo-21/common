import aiormq
from .WorkQueue import WorkQueue
from .ExchangeQueue import ExchangeQueue
import logging

class AsyncConnection:
    def __init__(self, host="rabbitmq", port=5672, virtual_host=None, user="guest", password="guest"):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.user = user
        self.password = password

        self.connection = None
        self.channel = None
        self._active_connection = False
        self._active_channel = False

    async def connect(self):
        try:
            connection_url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"
            if self.virtual_host:
                connection_url += self.virtual_host

            self.connection = await aiormq.connect(connection_url)
            self.channel = await self.connection.channel()

            self._active_connection = True
            self._active_channel = False
        except Exception as e:
            logging.error(f'Error init connection. error: {e}')
            raise e

    async def Publisher(self, exchange_name, exchange_type):
        return ExchangeQueue("pub", self.channel, exchange_name, exchange_type)
    
    async def Subscriber(self, exchange_name, exchange_type, queue_name, routing_keys=None):
        return ExchangeQueue("sub", self.channel, exchange_name, exchange_type, queue_name, routing_keys)


    # TODO: Make WorkQueue implementation async
      
    # async def Consumer(self, queue_name):
    #     return WorkQueue(self.channel, queue_name)

    # async def Producer(self, queue_name):
    #     return WorkQueue(self.channel, queue_name)

    # async def start_consuming(self):
    #     if self._active_channel:
    #         raise Exception("Channel Already Active Consuming other data")
    #     self._active_channel = True
    #     self.channel.start_consuming()


    # async def stop_consuming(self):
    #     if not self._active_channel:
    #         raise Exception("Already Stopped Channel")
    #     self.channel.stop_consuming()
    #     self._active_channel = False


    # async def stop_basic_consume(self, basic_id):
    #     self.channel.basic_cancel(consumer_tag=basic_id)


    # async def close(self):
    #     try:
    #         if self._active_channel:
    #             self._active_channel = False
    #             self.channel.stop_consuming()
    #         if not self._active_connection:
    #             raise Exception("Already Stopped")
    #         self._active_connection = False
    #         self.connection.close()
    #     except Exception as e:
    #         logging.error(f"Connection: error closing connection | error: {e}")