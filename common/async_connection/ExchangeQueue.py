import logging
import aiormq

PUBLISHER = "pub"
SUBSCRIBER = "sub"

class ExchangeQueue():
    def __init__(self, type, channel, exchange_name, exchange_type, queue_name=None, routing_keys=None):
        try:
            self.type = type
            self.channel = channel
            self.exchange_name = exchange_name
            self.exchange_type = exchange_type
            self.user_callback = None
            self.routing_keys = routing_keys
            self.queue_name = queue_name
        except Exception as e:
            logging.error(f"Exchange Queue: Error creating queue {e}")

    async def init(self):
        try:
            await self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
            if type == SUBSCRIBER:
                if self.exchange_type == "topic" and self.routing_keys is None:
                    raise Exception("You Need A Topic To Be Subscribed To")
                self.queue_name = await self._declare_queue(self.exchange_name, self.queue_name)

        except Exception as e:
            logging.error(f"Exchange Queue: Error creating queue {e}")


    async def _declare_queue(self, exchange_name, queue_name):
        if not queue_name:
            result = await self.channel.queue_declare(queue='', durable=False)
            queue_name = result.queue
        else:
            await self.channel.queue_declare(queue=queue_name, durable=True)

        if self.exchange_type == "topic":
            for routing_key in self.routing_keys:
                await self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        else:
            await self.channel.queue_bind(exchange=exchange_name, queue=queue_name)
            
        return queue_name

    async def receive(self, callback, prefetch_count=1):
        try:
            self.user_callback = callback
            await self.channel.basic_qos(prefetch_count=prefetch_count)
            await self.channel.basic_consume(queue=self.queue_name, consumer_callback=self._callback)
        except Exception as e:
            logging.error(f"Work Exchange: Error receiving message -> {e}")
        
    async def _callback(self, message: aiormq.abc.DeliveredMessage):
        try:
            self.user_callback(message.body, message.delivery_tag)
        except Exception as e:
            logging.error(f"Exchange Queue: Error on callback -> {e}")

    async def ack(self, ack_element):
        try:
            if isinstance(ack_element, list):
                await self.channel.basic_ack(delivery_tag=ack_element[-1], multiple=True)
            elif isinstance(ack_element, int):
                await self.channel.basic_ack(delivery_tag=ack_element)
            else:
                raise Exception(f"Not Valid ACK Element {ack_element}")
        except Exception as e:
            logging.error(f"Work Queue: Error sending ack {e}")

    async def nack(self, ack_element):
        try:
            if isinstance(ack_element, list):
                await self.channel.basic_nack(delivery_tag=ack_element[-1], multiple=True)
            elif isinstance(ack_element, int):
                await self.channel.basic_nack(delivery_tag=ack_element)
            else:
                raise Exception(f"Not Valid ACK Element {ack_element}")                
        except Exception as e:
            logging.error(f"Work Queue: Error sending nack {e}")

    async def resend_bind_queue(self, message):
        try:
            if self.type == PUBLISHER:
                return
            await self.channel.basic_publish(exchange="",
                        routing_key=self.queue_name,
                        body=message,
                        properties=aiormq.spec.Basic.Properties(delivery_mode=1))
        except Exception as e:
            logging.error(f"Exchange Queue: Error resending message to binded queue {e}")

    async def send(self, message, routing_key=''):
        try:
            await self.channel.basic_publish(exchange=self.exchange_name,
                        routing_key=routing_key,
                        body=message,
                        properties=aiormq.spec.Basic.Properties(delivery_mode=1))
        except Exception as e:
            logging.error(f"Exchange Queue: Error sending message {e}")
