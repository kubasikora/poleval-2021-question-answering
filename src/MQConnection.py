import pika
import logging
from time import sleep
from typing import Callable

class MQConnection:
    logger = logging.getLogger("MQConnection")
    
    def __init__(self) -> None:
        self.connection = None
        self.url = None

    def connect(self, url: str) -> None:
        reconnectCounter = 0
        while reconnectCounter < 10:
            try:
                if self.url is not None:
                    self.stop()
                self.connection = pika.BlockingConnection(parameters=pika.URLParameters(url))
                self.url        = url
                self.channel    = self.connection.channel()
                break
            except:
                MQConnection.logger.info(f"Reconnecting to {url}")
                sleep(10)
                reconnectCounter += 1
        MQConnection.logger.info(f"Connected to {self.url}")

    def stop(self) -> None:
        self.connection.close()
        MQConnection.logger.info("Stopped connection")

    def register(self, queue: str, callback: Callable) -> None:
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        MQConnection.logger.info(f"Registered consumer to queue {queue}")

    def spin(self) -> None:
        MQConnection.logger.info("Waiting for messages")
        self.channel.start_consuming()
